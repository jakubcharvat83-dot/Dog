## Why / linked issue

Describe the observed problem and expected outcome. Link the issue or design decision.

## Scope and safety

- [ ] No live Home Assistant configuration, personal records, secrets or tokens committed
- [ ] No actuator commands/deployments or production configuration changes in this PR
- [ ] Changes are limited to the documented public GitOps scaffolding

## Verification

- [ ] `python -m unittest discover -s tests -v`
- [ ] `DD_API_KEY=CI_PLACEHOLDER_NO_REAL_CREDENTIAL docker compose -f datadog/compose.yaml config --quiet`
- [ ] GitHub Actions quality gate passed (or blocker explained)

## Reversibility

State how to revert this change. For any future V7 software PR, also provide replay results, shadow checks and explicit safety rollback.
