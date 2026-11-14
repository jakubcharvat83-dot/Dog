# STROJ V7: software engineering workflow (target architecture)

**Status:** proposed development process, not a claim that the V7 implementation
has already migrated to GitHub. This public repository is templates-only.

## Actual software, not disconnected prototypes

Research / reverse engineering produces *evidence* (source/version/license,
algorithm notes, reproducer, simulation and benchmark). It does **not** directly
produce production firmware or a live HA automation. Promoting an idea to a feature
requires a short specification and a testable interface.

The real implementation belongs in a **private** STROJ V7 repository with:

| Component | Responsibility | Safety boundary |
| --- | --- | --- |
| `domain/` | Psychrometrics, constraints, state transitions | Pure functions, no network I/O |
| `ingestion/` | Typed SHT41, LG, DryFy, power, weather samples | Reject stale, implausible, missing data |
| `models/` | Forecasts, bias/error, confidence estimates | Shadow calculations, no actuator writes |
| `policy/` | Proposes candidate modes under constraints | Cannot write to HA or devices |
| `executor/` | One auditable writer and physical interlocks | Disabled until manual approval |
| `adapters/` | HA API, ESPHome, ThinQ, logging | Per-adapter credentials; read-only by default |
| `replay/` | Time-ordered simulation on scrubbed historical events | Deterministic repeatability |
| `telemetry/` | Black-box events, anomaly detection, KPIs | Never collect credentials or private content |

A feature is defined by one issue, explicit input/output schema, success and
failure criteria, tests, observability and rollback. Avoid standalone scripts with
silent access to production devices. Do not make the presence of an AI agent part
of the safety chain.

## Git and CI delivery chain

```
Issue / specification
    -> short design decision (ADR)
    -> feature branch + code + deterministic tests
    -> pull request + static checks + unit tests + security checks
    -> historical replay + fault injection + comparison with V6 baseline
    -> reviewed merge to private main
    -> versioned, checksummed release artifact
    -> manual install into shadow (no actuator writes)
    -> monitored evidence across day/night
    -> explicit go/no-go + limited controlled pilot
    -> gradual rollout, or tested one-step rollback to V6
```

CI must not possess production HA credentials, Docker socket or SSH access to N100.
GitHub Actions does **not** deploy to live hardware. Production operator uses a
pinned release after inspecting artifacts and signing off on the change.

## Test gates before each physical pilot

1. **Unit/property:** math, saturation, input validation, units and time handling.
2. **Replay:** deterministic historical episodes in day and night; split training
   and held-out validation, baseline comparison and robust confidence intervals.
3. **Failure simulation:** stale V1/V2, failed ThinQ, missing power feedback,
   stuck actuators, HA restarts, clock jumps and incorrect mode acknowledgements.
4. **Safety invariants:** V1/V2 control normal mode, V3 advisory plus emergency;
   verified LG/DryFy mutual exclusion and minimum OFF/run protection; hardware
   power feedback is not proof of actual compressor internals.
5. **Shadow:** collect independent production data; never issue actuator commands.
6. **Go/no-go:** human-approved scope and TTL, record pre-state and exact rollback.
   No new full-control rollout before sufficient shadow periods (initial target
   at least seven nights) and demonstrated V6 fallback.

## Definition of Done

Code merged is not "deployed". Done means tests green, documented interfaces,
recorded baseline and new metrics, no lost safety requirements, signed-off risk,
versioned artifact, rollout record, rollback executed in a test, and post-deploy
verification. A quality gate that does not run the V7 code must never be reported
as V7 CI passing.

## Current state and migration order

- V6 runs as current physical controller on N100.
- V7 P1 shadow runs independently and publishes diagnostic measurements.
- Existing local Python scripts and HA package YAML are **not** in this public repo.
- **Next:** create a separate private repository and move *sanitized, reviewed*
  V7 domain and shadow code; initially no production token, actuator access,
  runtime snapshots or raw measurements.
- Only after private CI can pass unit, replay and failure-injection tests should
  the team define the executor interface and a staged deployment workflow.
