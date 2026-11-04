# Datadog host metrics (EU1) - not deployed

Requires a Datadog **API key**; Google OAuth is not an API key.

1. `cp .env.example .env` and edit `.env` privately, never in chat or Git.
2. `chmod 600 .env`.
3. `docker compose config --quiet` to validate.
4. `docker compose up -d` to send host/container metrics to Datadog EU1.
5. Check `docker compose ps` and `docker logs stroj-datadog-agent`.

Host/container metrics are opt-in and may incur Datadog charges. Docker socket
access is powerful even on a read-only bind mount. Logs, APM and process
collection are disabled by default. Review billing and host access first.

Datadog MCP (AI tools) is separate; authenticate via `codex mcp login datadog-eu`.
