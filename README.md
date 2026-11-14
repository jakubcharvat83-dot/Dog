# STROJ GitOps — public templates only

This repository contains **reviewed, allowlisted infrastructure templates**.
It is connected to GitHub as `jakubcharvat83-dot/Dog`. It does **not** contain
STROJ V6/V7 source code, active Home Assistant packages, private datasets,
credentials, backups or live deployment configuration.

## Development workflow

Pull requests into `main` run a read-only GitHub Actions quality workflow:
[`.github/workflows/quality.yml`](.github/workflows/quality.yml).
The checks enforce an allowlist of tracked files, refuse common secret-bearing
content, test that the Datadog template is opt-in, and validate its Compose syntax
with a dummy key. **These checks do not test V7 software**: V7 must first move to a
separate private repository with its own CI, replay and staging tests.

See [CONTRIBUTING.md](CONTRIBUTING.md) and
[STROJ V7 workflow](docs/STROJ_V7_WORKFLOW.md).

## Optional Datadog telemetry (not deployed)

`datadog/compose.yaml` is an optional EU1 host-metrics template. It has no API key
and is not launched by CI. Running it requires a private API key, explicit operator
approval and a review of Docker socket access, data sent and billing.
See [`datadog/README.md`](datadog/README.md).
