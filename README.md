# STROJ GitOps

Local Git repository with explicitly allowlisted, reviewed configuration templates.
There is no GitHub remote yet because the linked GitHub account has no accessible
repositories or GitHub App installation. Create a private repo and authorize access
before synchronizing. No active HA package/configuration or credentials are tracked.

Datadog EU1 MCP is configured in the local Codex CLI as `datadog-eu`.
OAuth still requires owner authorization: `codex mcp login datadog-eu`.

Datadog Docker telemetry is not running. See `datadog/README.md`.
