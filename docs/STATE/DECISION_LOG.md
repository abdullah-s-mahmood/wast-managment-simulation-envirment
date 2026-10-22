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
| D-0008 | Single-maintainer sprint acceptance under ADR-0005. | Accepted by owner 2026-10-22 | The project has no second human reviewer. Authorized agent may self-audit, merge a tested PR after exact-head CI where GitHub allows, and continue without routine approval requests. Scientific/test/provenance gates remain mandatory. | Reconsider if collaborators join or repository policy changes. |
| D-0009 | Owner designates LEGACY-CANDIDATE-001 at SHA-256 da08e1a78e73215ddf9d165e32a07f262a0b8379b3b04f4b17b27d5b6b525da8 for read-only local audit; expected compressed size 487062036 bytes verified. | Authorized by owner, identity verified | Resolves B-S009-01; no extraction/execution/copying/redistribution or reuse permission. | B-S009-02 safety finding must resolve before full intake; any baseline replacement requires explicit designation. |
| D-0010 | Private inventory quarantines suspicious entries and continues safely under ADR-0006. | Accepted by owner 2026-10-22 | Separate technical inventory completion from clearance, reuse and scientific validation; archive remains unchanged. | Parser/resource/integrity bypass or proposed extraction/execution/reuse/publication. |
