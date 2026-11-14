# Contributing to STROJ

This is a **public GitOps template repository**, not the STROJ V6/V7 runtime source tree.
Do not commit HA tokens, Datadog credentials, host addresses, databases, unredacted logs,
private recordings, backups or live production HA configuration.

## Current change process

1. Create a GitHub issue or short design note with an explicit goal and acceptance criteria.
2. Create a branch. One feature or fix per pull request; never edit `main` directly.
3. Make a small change with reproducible checks. No code should be deployed from this repository automatically.
4. Run `python -m unittest discover -s tests -v` locally. For compose-template changes,
   also validate with a **dummy** `DD_API_KEY` using `docker compose ... config --quiet`.
5. Open a PR and review its diff and GitHub Actions results before merging. Keep `main` stable.
6. Document any user-visible changes and the exact rollback. Merge is not a production release.

## Separate private STROJ V7 software repository (next milestone)

Real V7 Python modules belong in a **private** repository with isolated packages for
sensor ingestion, domain math, forecast, policy, executor, observability and adapters.
The project must have typed schemas, pinned dependencies, format/lint/type checks,
unit/property tests, replay on sanitized recordings, simulated failure scenarios,
and release artifacts with version, checksum and rollback instructions.

Live hardware is controlled by **exactly one executor**. V6 remains authoritative until
reviewed shadow evidence, safety checks, explicit go/no-go and a manual pilot. Never
commit a workflow that deploys to N100 or sends HA service commands from PR CI.

See [V7 development lifecycle](docs/STROJ_V7_WORKFLOW.md).
