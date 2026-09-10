from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from deskflow.config import get_settings
from deskflow.proto import store
from deskflow.db.identity import (
    authenticate,
    list_role_rows,
    list_users,
    register_user,
    set_user_roles,
    user_by_id,
)
from deskflow.db.passwords import DEMO_PASSWORD
from deskflow.db.seed import sample_accounts

HERE = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(HERE / "templates"))
VIEW_COOKIE = "tekforce_view"
USER_COOKIE = "tekforce_user"
STAFF_ROLES = frozenset({"recruiter", "exec", "admin"})

router = APIRouter(tags=["prototype"])


def _persona(request: Request) -> str:
    raw = request.cookies.get(VIEW_COOKIE, "visitor")
    return raw if raw in store.ROLES else "visitor"


def _signed_in_user(request: Request) -> dict | None:
    raw = request.cookies.get(USER_COOKIE, "")
    if not raw:
        return None
    return user_by_id(raw)


def _ctx(request: Request, **extra: object) -> dict[str, object]:
    persona = _persona(request)
    account = _signed_in_user(request)
    return {
        "request": request,
        "persona": persona,
        "nav": store.NAV[persona],
        "roles": store.ROLES,
        "my_tekforce_href": store.my_tekforce_href(persona),
        "notice": request.query_params.get("notice"),
        "show_sample_logins": get_settings().show_sample_logins(),
        "signed_in_name": account["name"] if account else "",
        "verticals": store.VERTICALS(),
        "placement_types": store.PLACEMENT_TYPES(),
        "vertical_specialties": store.nav_specialties(),
        "show_desk_nav": persona in STAFF_ROLES,
        "can_assign_roles": persona in {"exec", "admin"},
        "signed_in_home": store.HOME_AFTER_LOGIN.get(persona, "/"),
        **extra,
    }


def _page(request: Request, name: str, **extra: object) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name=name,
        context=_ctx(request, **extra),
    )


def _go(path: str, notice: str | None = None) -> RedirectResponse:
    if notice:
        path = f"{path}?notice={quote(notice)}"
    return RedirectResponse(path, status_code=303)


@router.post("/view")
def set_view(as_: str = Form(..., alias="as"), next: str = Form("/")) -> RedirectResponse:
    persona = as_ if as_ in store.ROLES else "visitor"
    target = next if next.startswith("/") and not next.startswith("//") else "/"
    response = RedirectResponse(target, status_code=303)
    response.set_cookie(VIEW_COOKIE, persona, httponly=False, samesite="lax")
    return response


def _signed_in_home(persona: str) -> str:
    return store.HOME_AFTER_LOGIN.get(persona, "/")


@router.get("/my-tekforce", response_model=None)
def my_tekforce(request: Request) -> HTMLResponse | RedirectResponse:
    persona = _persona(request)
    if persona == "visitor":
        return _go("/my-tekforce/login")
    return _page(request, "my_tekforce.html", home=_signed_in_home(persona))


@router.get("/my-tekforce/login", response_model=None)
def login_form(request: Request) -> HTMLResponse | RedirectResponse:
    if _persona(request) != "visitor":
        return _go("/my-tekforce")
    accounts = sample_accounts() if get_settings().show_sample_logins() else []
    return _page(request, "login.html", accounts=accounts)


@router.post("/my-tekforce/login")
def login_submit(
    email: str = Form(""),
    password: str = Form(""),
    remember: str = Form(""),
) -> RedirectResponse:
    del remember
    account = authenticate(email, password)
    if account is None:
        return _go("/my-tekforce/login", "Unknown email or wrong password. Demo password is “sample”.")
    response = _go(_signed_in_home(account["role"]), f"Signed in as {account['name']} · sample only.")
    response.set_cookie(VIEW_COOKIE, account["role"], httponly=False, samesite="lax")
    response.set_cookie(USER_COOKIE, account["id"], httponly=False, samesite="lax")
    return response


@router.get("/my-tekforce/register", response_class=HTMLResponse)
def register_form(request: Request) -> HTMLResponse:
    return _page(request, "register.html")


@router.post("/my-tekforce/register")
def register_submit(
    role: str = Form("candidate"),
    email: str = Form(""),
    first_name: str = Form(""),
    last_name: str = Form(""),
    name: str = Form(""),
    password: str = Form(DEMO_PASSWORD),
) -> RedirectResponse:
    persona = role if role in ("candidate", "client") else "candidate"
    full_name = " ".join(part for part in (first_name.strip(), last_name.strip()) if part) or name.strip()
    created = register_user(email, full_name, persona, password or DEMO_PASSWORD)
    if created is None:
        return _go("/my-tekforce/register", "That email is already registered or the role is invalid.")
    response = _go(_signed_in_home(persona), "Registered in the prototype. Sample data only.")
    response.set_cookie(VIEW_COOKIE, persona, httponly=False, samesite="lax")
    response.set_cookie(USER_COOKIE, created["id"], httponly=False, samesite="lax")
    return response


@router.get("/my-tekforce/forgot", response_class=HTMLResponse)
def forgot_password(request: Request) -> HTMLResponse:
    return _page(request, "forgot.html")


@router.post("/my-tekforce/logout")
def logout() -> RedirectResponse:
    response = _go("/", "Signed out of My Tekforce.")
    response.set_cookie(VIEW_COOKIE, "visitor", httponly=False, samesite="lax")
    response.delete_cookie(USER_COOKIE)
    return response


@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return _page(request, "home.html", verticals=store.VERTICALS())


@router.get("/jobs", response_class=HTMLResponse)
def job_board(request: Request, q: str = "") -> HTMLResponse:
    return _page(request, "jobs.html", jobs=store.public_jobs(q), job_query=q)


@router.get("/jobs/{job_id}", response_class=HTMLResponse)
def job_detail(request: Request, job_id: str) -> HTMLResponse:
    job = store.job_by_id(job_id)
    if job is None or job["status"] != "public":
        return _go("/jobs", "That job is not on the public board.")
    return _page(request, "job.html", job=job)


@router.get("/jobs/{job_id}/apply", response_class=HTMLResponse)
def apply_form(request: Request, job_id: str) -> HTMLResponse:
    job = store.job_by_id(job_id)
    if job is None or job["status"] != "public":
        return _go("/jobs", "That job is not on the public board.")
    return _page(request, "apply.html", job=job)


@router.post("/jobs/{job_id}/apply")
def apply_submit(
    job_id: str,
    name: str = Form("Alex Rivera"),
    headline: str = Form("Senior test engineer, Python automation"),
) -> RedirectResponse:
    row = store.apply(job_id, name.strip() or "Alex Rivera", headline.strip())
    if row is None:
        return _go("/jobs", "That job is not on the public board.")
    return _go("/applications", "Application recorded. Sample data only.")


@router.get("/applications", response_class=HTMLResponse)
def my_applications(request: Request) -> HTMLResponse:
    return _page(request, "applications.html", applications=store.candidate_applications())


@router.get("/hire", response_class=HTMLResponse)
def hire_form(request: Request) -> HTMLResponse:
    return _page(
        request,
        "hire.html",
        verticals=store.VERTICALS(),
        placement_types=store.PLACEMENT_TYPES(),
    )


@router.post("/hire")
def hire_submit(
    title: str = Form(...),
    vertical: str = Form(...),
    placement_type: str = Form(...),
    description: str = Form(""),
) -> RedirectResponse:
    job = store.draft_job(title.strip(), vertical, placement_type, description.strip())
    return _go("/me/jobs", f"Draft “{job['title']}” is waiting for Tekforce approval.")


@router.get("/desk/approve", response_class=HTMLResponse)
def approve_queue(request: Request) -> HTMLResponse:
    return _page(request, "approve.html", jobs=store.pending_jobs())


@router.post("/desk/approve/{job_id}")
def approve_job(job_id: str) -> RedirectResponse:
    job = store.approve(job_id)
    if job is None:
        return _go("/desk/approve", "No such draft.")
    return _go("/jobs", f"“{job['title']}” is on the public board.")


@router.get("/desk/jobs", response_class=HTMLResponse)
def desk_jobs(request: Request) -> HTMLResponse:
    return _page(request, "desk_jobs.html", jobs=store.jobs())


@router.get("/desk/jobs/{job_id}", response_class=HTMLResponse)
def desk_job(request: Request, job_id: str) -> HTMLResponse:
    job = store.job_by_id(job_id)
    if job is None:
        return _go("/desk/jobs", "No such job.")
    return _page(
        request,
        "desk_job.html",
        job=job,
        applications=store.applications(job_id),
        slate=store.slate_for(job_id),
    )


@router.post("/desk/jobs/{job_id}/slate")
async def desk_send_slate(request: Request, job_id: str) -> RedirectResponse:
    form = await request.form()
    ids = [str(value) for value in form.getlist("application_id")]
    job = store.send_slate(job_id, ids)
    if job is None:
        return _go("/desk/jobs", "No such job.")
    if not ids:
        return _go(f"/desk/jobs/{job_id}", "Select at least one person for the slate.")
    return _go(
        f"/desk/jobs/{job_id}",
        f"Slate sent to {job['account']}. Switch View as to Client, then open My jobs.",
    )


@router.get("/me/jobs", response_class=HTMLResponse)
def client_jobs(request: Request) -> HTMLResponse:
    return _page(request, "client_jobs.html", jobs=store.jobs())


@router.get("/me/jobs/{job_id}", response_class=HTMLResponse)
def client_job(request: Request, job_id: str) -> HTMLResponse:
    job = store.job_by_id(job_id)
    if job is None:
        return _go("/me/jobs", "No such job.")
    return _page(
        request,
        "client_job.html",
        job=job,
        slate=store.slate_for(job_id),
    )


def _can_assign_roles(persona: str) -> bool:
    return persona in {"exec", "admin"}


@router.get("/desk/users", response_model=None)
def desk_users(request: Request) -> HTMLResponse | RedirectResponse:
    if not _can_assign_roles(_persona(request)):
        return _go("/", "View as Exec or Admin to assign roles.")
    return _page(
        request,
        "users.html",
        users=list_users(),
        role_rows=list_role_rows(),
    )


@router.post("/desk/users/{user_id}")
async def desk_users_assign(request: Request, user_id: str) -> RedirectResponse:
    if not _can_assign_roles(_persona(request)):
        return _go("/", "View as Exec or Admin to assign roles.")
    form = await request.form()
    codes = [str(value) for value in form.getlist("role")]
    updated = set_user_roles(user_id, codes)
    if updated is None:
        return _go("/desk/users", "No such user.")
    return _go("/desk/users", f"Updated roles for {updated['email']}.")
