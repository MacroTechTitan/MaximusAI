---
name: maximus-devops-ship
description: "Ship code to production safely: CI/CD pipelines, Infrastructure as Code, progressive delivery, observability, SLOs, and rollback. Use when the user asks to 'deploy', 'set up CI/CD', 'ship to production', 'add monitoring', 'write a GitHub Action', 'add Terraform', 'set up canary', or when promoting a service from dev to prod. Covers GitHub Actions, Terraform / AWS CDK, Docker, Kubernetes, Vercel, and observability with Prometheus / Grafana / OpenTelemetry. Enforces IaC, progressive delivery, working rollback, SLOs with error budgets, and runbooks per alert."
metadata:
  pillar: deployment
  source: maximus
---

# Maximus — DevOps & Ship

Shipping is the act of putting work in front of users. Done well, it is uneventful — the deploy is one of dozens that week, the alert is silent, and the rollback button works. Done badly, it's the most expensive sentence in software: "the deploy went wrong." This skill is the discipline that makes the boring path the default. The horse hauls the harvest to market; the rider laid the road.

## When to use

- Setting up CI/CD for a project for the first time, or fixing what's there.
- Promoting a service from dev → staging → prod.
- The user says: "deploy", "ship", "release", "set up CI", "add monitoring", "Terraform", "GitHub Action", "Docker", "Kubernetes", "Vercel", "canary", "rollback", "SLO".
- An audit/compliance review needs evidence of deployment controls.

## The five pillars

1. **Infrastructure as Code (IaC)** — every piece of infra defined in version-controlled code (Terraform, CDK, Pulumi). Changes go through PR review like application code.
2. **CI/CD as the only path** — humans don't `scp` files or click around the cloud console for deploys. Builds, tests, and deploys are pipeline jobs.
3. **Progressive delivery** — new code reaches users gradually (canary, blue/green, percentage rollout). Bad changes blast a small radius before the rollback fires.
4. **Observability** — metrics, logs, and traces with SLOs and error budgets. You know within seconds when something is degrading; you know within minutes why.
5. **Working rollback** — every deploy can be reversed by a single, tested action. Untested rollbacks are folklore.

## Procedure

### 1. Pick the deployment model that fits the service

- **Static / Jamstack frontend** (React + Vite, Next, Astro): platform-native (Vercel, Netlify, Cloudflare Pages). PR → preview URL; merge → prod. Cheapest, simplest.
- **Long-running web service** (API, worker): containerized, deployed to a managed platform (Fly.io, Render, Railway, Google Cloud Run) or Kubernetes. Single process, horizontal scale.
- **Multi-service / stateful systems**: Kubernetes (EKS/GKE/AKS) — only when the complexity is justified by genuine multi-service needs. K8s is a power tool with a maintenance bill.
- **Serverless functions**: Vercel/AWS Lambda for spiky, low-ops workloads. Watch cold-starts for latency-sensitive paths.

Pick the simplest model that meets the requirements. The most expensive deployment platform is the one you operate poorly.

### 2. Write the CI/CD pipeline

GitHub Actions example structure for a typical app:

```yaml
name: ci
on: [push, pull_request]
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [checkout, setup-language, install, lint]
  typecheck:
    runs-on: ubuntu-latest
    steps: [checkout, setup-language, install, typecheck]
  test:
    runs-on: ubuntu-latest
    steps: [checkout, setup-language, install, unit + integration tests]
  build:
    needs: [lint, typecheck, test]
    runs-on: ubuntu-latest
    steps: [build artifact, push image / upload bundle]
  deploy-staging:
    if: github.ref == 'refs/heads/main'
    needs: [build]
    steps: [deploy to staging, run smoke tests, post status]
  deploy-prod:
    if: github.ref == 'refs/heads/main' && success()
    needs: [deploy-staging]
    environment: production  # protects with required reviewers
    steps: [progressive rollout, monitor SLO, finalize or rollback]
```

Key rules:
- **Fast PR jobs** (lint/typecheck/unit tests) gate merge. Slow nightly jobs run separately.
- **Build artifact once, deploy many times.** The bytes that staged are the bytes that go to prod.
- **Required reviewers on the prod environment** for protected services.
- **Secrets via the platform's secret store**, never in repo or workflow file.

### 3. Infrastructure as Code

Pick one tool and stick with it across the project. Terraform is the de facto cross-cloud default; AWS CDK / Pulumi if you want a real programming language.

Layout that scales:
```
infra/
  modules/        # reusable building blocks (network, db, queue, service)
  envs/
    staging/      # composes modules for staging
    production/   # composes modules for prod
  .github/workflows/terraform.yml
```

Rules:
- `terraform plan` runs on every PR; output is posted as a PR comment.
- `terraform apply` runs only from `main` after PR merge, and only on the relevant environment.
- State is remote and locked (Terraform Cloud, S3+DynamoDB).
- Secrets reference a secret manager (AWS Secrets Manager, GCP Secret Manager, Doppler) — they are not stored in state in plaintext.

### 4. Progressive delivery and rollback

Pick a strategy that matches your platform:

- **Vercel / Netlify**: preview deploys per PR; promote to prod with a single click; instant rollback to a previous deploy.
- **Container platform**: percentage rollout (5% → 25% → 100%), with auto-rollback if error rate or latency exceeds thresholds.
- **Kubernetes**: rolling update with `maxSurge`/`maxUnavailable`; or Argo Rollouts / Flagger for canary + automated analysis.

**Test the rollback before you need it.** Once per quarter, do a deliberate rollback in staging to confirm the procedure still works.

Feature flags (LaunchDarkly, Unleash, or a homegrown table) are the cheapest progressive-delivery primitive: ship dark, enable per-customer, kill instantly without a redeploy. New risky paths land flagged off.

### 5. Observability

Three signals, in order of importance:

- **Metrics (RED for services, USE for resources)**: request Rate, Error rate, Duration; Utilization, Saturation, Errors. Prometheus + Grafana; or platform-native (Datadog, NewRelic, Honeycomb). Dashboards exist per service before the service ships.
- **Structured logs** with a correlation/request ID across services. JSON; centralized (ELK, Loki, Cloud Logging). No more `print` in production code.
- **Distributed tracing** via OpenTelemetry. Worth the integration cost the first time you debug a 9-service request path.

Instrument *before* you scale. Engineers who skip this regret it the first incident.

### 6. SLOs and error budgets

Define a Service Level Objective for each user-facing service. Standard starting point:

- **Availability**: 99.9% successful requests over 30 days.
- **Latency**: p95 < N ms (N depends on the surface — checkout 300ms, search 200ms, batch 5s).

The **error budget** is the remaining failure allowance. Burn rate alerts:
- Fast burn (consuming 10% of monthly budget in 1 hour) → page.
- Slow burn (consuming 10% of monthly budget in 6 hours) → ticket.

Tie ship velocity to budget: budget burned → release freeze on the affected service until budget recovers. This is how reliability becomes a feature with skin in the game, not a slogan.

### 7. Runbooks

Every page-able alert links to a runbook with:
- **What the alert means** in one sentence.
- **First 3 commands** to gather diagnostic state.
- **Common causes**, ordered by frequency.
- **Mitigation steps**, ordered by safety.
- **Escalation path** if mitigation fails.

An alert without a runbook is noise. Runbook lives in the repo (e.g., `runbooks/<alert-name>.md`).

## Platform-specific quick guides

- **Vercel** (your stack): connect git repo → set env vars in dashboard (Production / Preview / Development scoped) → preview URL per PR → merge to `main` deploys to prod → instant rollback button on the deployment page. Add `vercel.json` for headers, redirects, and serverless function config.
- **Replit Deployments**: target `cloudrun` in `.replit` for production; Replit Secrets for env; one-click deploy. Good for prototypes and internal tools; less so for high-availability prod.
- **GitHub Actions secrets**: use environments with required reviewers; rotate quarterly; never echo secrets in `run` blocks.

## Domain-specific notes

- **Web services**: HTTPS only; HSTS; CSP headers; secrets via secret manager; auth on every protected endpoint.
- **Fintech**: separate staging/prod Stripe accounts and keys; webhook endpoints HTTPS-only; production keys restricted to the minimum scope; audit logging of every deploy (`who deployed, when, which SHA`).
- **Scientific computing**: containerize the analysis environment; archive each release with Zenodo for DOI; pinned dependency lock travels with the deploy.
- **Multi-region / regulated**: data residency configured in IaC; failover tested; runbook covers regional outage.

## Gotchas

- **`scp` / console deploys** by humans — every manual deploy is a future incident. CI/CD only.
- **Secrets in env literals in the workflow file** — use the platform secret store. Rotate on suspicion.
- **No staging environment** — "prod is staging" is a confession, not a strategy.
- **Untested rollback** — drill it quarterly. The day you need it is the worst day to discover it doesn't work.
- **Alerts without runbooks** — train the on-call to ignore alerts.
- **SLO without budget enforcement** — vanity number. Tie ship velocity to budget or it does nothing.
- **One person who knows how the deploy works** — bus factor 1. Document the procedure; have someone else do the next release.
- **K8s for a 2-service app** — operating cost outweighs benefit. Use the simplest model that works.

## Output

A deployment plan (or PR) including: CI workflow file(s), IaC module additions, a progressive-rollout configuration, dashboards + alerts (with runbooks), and an SLO document. Final chat summary lists: target platform, pipeline jobs, IaC tool, rollout strategy, SLO targets, and the rollback command/click-path.
