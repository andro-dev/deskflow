# Deploy Deskflow on AWS (App Runner)

**Status:** this repository has not been deployed. There is no live URL to paste. If AWS credentials are missing on the machine, run Docker locally and use the steps below when an account is available.

App Runner is the smallest AWS option that stays easy to explain: you build a container, push it to ECR, and App Runner pulls it and exposes HTTPS. No cluster YAML. Elastic Beanstalk and ECS/Fargate also work; they are more moving parts for the same FastAPI process.

## What you need

- An AWS account and IAM permission to use **ECR** and **App Runner**
- AWS CLI v2 (`aws sts get-caller-identity` must succeed)
- Docker
- A region (example below: `us-east-1`)

Replace `123456789012` with your account id and `deskflow` with your ECR repository name if you change it.

## 1. Local sanity check (required even without AWS)

```bash
cd /home/andrew/projects/deskflow
docker build -t deskflow:local .
docker run --rm -p 8080:8080 deskflow:local
curl -sS http://127.0.0.1:8080/health
```

Expect JSON with `"status": "ok"`. Stop the container before pushing.

## 2. Create an ECR repository

```bash
aws ecr create-repository --repository-name deskflow --region us-east-1
```

If the repository already exists, continue.

## 3. Authenticate Docker and push

```bash
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
REPO="${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com/deskflow"

aws ecr get-login-password --region "$REGION" \
  | docker login --username AWS --password-stdin "${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com"

docker build -t deskflow:local .
docker tag deskflow:local "${REPO}:0.1.0"
docker tag deskflow:local "${REPO}:latest"
docker push "${REPO}:0.1.0"
docker push "${REPO}:latest"
```

## 4. Create the App Runner service

Console path: **App Runner → Create service → Container registry → Amazon ECR**.

- Image URI: `123456789012.dkr.ecr.us-east-1.amazonaws.com/deskflow:0.1.0`
- Port: `8080` (matches `PORT` in the Dockerfile)
- Health check: **HTTP**, path `/health`
- CPU/memory: 0.25 vCPU / 0.5 GB is enough for the MVP
- Environment: leave `DESKFLOW_LLM_*` unset unless you intentionally enable the overlay

Equivalent CLI sketch (fill the instance and access roles from your account):

```bash
ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1

aws apprunner create-service \
  --service-name deskflow \
  --region "$REGION" \
  --source-configuration '{
    "AuthenticationConfiguration": {
      "AccessRoleArn": "arn:aws:iam::'"${ACCOUNT}"':role/AppRunnerECRAccessRole"
    },
    "ImageRepository": {
      "ImageIdentifier": "'"${ACCOUNT}"'.dkr.ecr.'"${REGION}"'.amazonaws.com/deskflow:0.1.0",
      "ImageRepositoryType": "ECR",
      "ImageConfiguration": { "Port": "8080" }
    },
    "AutoDeploymentsEnabled": false
  }' \
  --instance-configuration '{"Cpu":"256","Memory":"512"}' \
  --health-check-configuration '{
    "Protocol":"HTTP",
    "Path":"/health",
    "Interval":10,
    "Timeout":5,
    "HealthyThreshold":1,
    "UnhealthyThreshold":5
  }'
```

App Runner needs an **access role** that can pull from ECR (`apprunner.amazonaws.com` trust, `AmazonEC2ContainerRegistryReadOnly` is the usual starting point). Create that role once in IAM if it does not exist.

## 5. Confirm the deploy

```bash
aws apprunner list-services --region us-east-1
curl -sS https://<app-runner-id>.us-east-1.awsapprunner.com/health
```

Only publish that hostname after `list-services` returns it. Do not commit a guessed URL.

## Cost and teardown

App Runner bills while the service exists. To stop spend:

```bash
aws apprunner pause-service --service-arn <arn> --region us-east-1
# or
aws apprunner delete-service --service-arn <arn> --region us-east-1
aws ecr delete-repository --repository-name deskflow --force --region us-east-1
```

## Why not the other AWS options (for this MVP)

| Option | Use when |
| --- | --- |
| **App Runner** | You want HTTPS + a container and can explain ECR + a health check |
| Elastic Beanstalk | You want AWS to build from source and already know EB platforms |
| ECS/Fargate | You need a cluster, load balancer, and task roles on purpose |

Deskflow does not need a VPC-heavy Fargate topology yet. If you later add private data stores, revisit ECS. Do not use GCP for this project.
