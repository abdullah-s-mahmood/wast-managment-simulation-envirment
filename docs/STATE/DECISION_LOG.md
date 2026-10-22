# Decision Log

| ID | Decision | Status | Rationale | Revisit condition |
|---|---|---|---|---|
| D-0001 | Build clean-room project; do not implement inside legacy execution. | Accepted | Avoids inheriting unverified behavior. | Explicit ADR after source audit/licensing review. |
| D-0002 | Separate model hypotheses from scenario settings. | Accepted | City/population/bin count/fleet/depot are experiment settings unless they describe module behavior. | New classification justified by model contract. |
| D-0003 | JSON-first configuration with versioned schemas/run snapshots. | Accepted in principle | Enables user control and reproducibility. | Exact contracts finalized in S025–S036. |
| D-0004 | SUMO and ns-3 are external adapters; domain modules independently testable. | Provisional | Separates mobility, network, physical models, and orchestration. | Verify versions/coupling in S017–S024. |
| D-0005 | Preserve currently approved PLC source set. | Accepted constraint | No silent substitution. | Evidence-backed ADR and explicit review. |
| D-0006 | No scientific equations or statistical models locked in bootstrap. | Accepted | Evidence/design precedes method choice. | Evidence and analysis gates pass. |
| D-0007 | Preserve raw observations and analyze independently. | Accepted | Enables audit and alternative analysis. | Refine output contracts in S081–S086. |
| D-0008 | Risk-based routine acceptance proposal in ADR-0005. | Proposed; inactive | Owner requested an autonomous workflow proposal; independent review and protection requirements remain effective. | Independent adoption and verified enforcement before use. |
