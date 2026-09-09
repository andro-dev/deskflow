"""Canonical skill names and aliases used by the heuristic extractor.

Keep this list boring and reviewable. It is the vocabulary the scorer can
defend in an interview, not a machine-learning embedding space.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    canonical: str
    aliases: tuple[str, ...]


SKILLS: tuple[Skill, ...] = (
    Skill("python", ("python", "py")),
    Skill("java", ("java",)),
    Skill("javascript", ("javascript", "ecmascript")),
    Skill("typescript", ("typescript", "ts")),
    Skill("go", ("golang", " go ")),
    Skill("sql", ("sql", "postgresql", "postgres", "mysql")),
    Skill("bash", ("bash", "shell scripting")),
    Skill("fastapi", ("fastapi", "fast api")),
    Skill("django", ("django",)),
    Skill("flask", ("flask",)),
    Skill("spring boot", ("spring boot", "springboot", "spring-boot")),
    Skill("pytest", ("pytest", "py.test")),
    Skill("junit", ("junit",)),
    Skill("playwright", ("playwright",)),
    Skill("selenium", ("selenium",)),
    Skill("cucumber", ("cucumber", "gherkin")),
    Skill("testng", ("testng",)),
    Skill("rest", ("rest", "restful", "rest api", "http api")),
    Skill("graphql", ("graphql",)),
    Skill("docker", ("docker", "containers", "containerization")),
    Skill("kubernetes", ("kubernetes", "k8s")),
    Skill("aws", ("aws", "amazon web services")),
    Skill("ecs", ("ecs", "fargate", "ecs/fargate")),
    Skill("lambda", ("aws lambda", "lambda")),
    Skill("s3", ("s3", "amazon s3")),
    Skill("app runner", ("app runner", "apprunner")),
    Skill("elastic beanstalk", ("elastic beanstalk", "beanstalk")),
    Skill("azure", ("azure", "microsoft azure")),
    Skill("gcp", ("gcp", "google cloud")),
    Skill("github actions", ("github actions", "github-actions", "gha")),
    Skill("jenkins", ("jenkins",)),
    Skill("gitlab ci", ("gitlab ci", "gitlab-ci")),
    Skill("ci/cd", ("ci/cd", "cicd", "continuous integration", "continuous delivery")),
    Skill("terraform", ("terraform",)),
    Skill("linux", ("linux", "unix")),
    Skill("git", ("git", "github", "gitlab")),
    Skill("pydantic", ("pydantic",)),
    Skill("httpx", ("httpx",)),
    Skill("api testing", ("api testing", "api tests", "contract testing")),
    Skill("observability", ("observability", "opentelemetry", "prometheus", "grafana")),
)


def all_canonical() -> list[str]:
    return [skill.canonical for skill in SKILLS]
