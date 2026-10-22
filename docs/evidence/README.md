# Evidence ledger contract and source-review checklist

Authority: RESEARCH_AND_EVIDENCE_POLICY.md and ADR-0004. The production ledger
is intentionally empty; S003 accepts no scientific model, citation or parameter.
`record_contract.json` is a custom machine-readable record schema, **not JSON
Schema**. Version 1 requires exactly the listed fields plus `variables` (a list
of objects with exactly the listed variable fields). Unknown versions/fields,
duplicate JSON keys/IDs, non-finite numbers and missing/empty values are rejected.
No new validation dependency is required. Runtime/scenario schemas remain S025–S036.

## Record semantics
- IDs: `EV-` followed by uppercase letters, digits or hyphens; stable and unique.
- `kind` and E1–E5 classes follow the evidence policy. An E4 legacy observation
  or E5 assumption cannot be accepted for implementation as a sourced scientific fact.
- Record a full citation, DOI or explicit `not_applicable: reason`, URL, version,
  access date (ISO calendar date), exact source page/table/equation/code location,
  repository-relative `source_path`, and SHA-256 of retained source bytes. Do not hash a description instead of source.
- `verification_status` is unverified/verified/synthetic; `verification_artifact`
  names a repository-relative source-review record. A schema pass does not verify
  that the source exists or that the equation was transcribed correctly.
- `equation` is exact notation/text, never evaluated as executable code. When the
  evidence kind has no equation, use `not_applicable: reason`. Each variable has
  symbol, definition, explicit units (`1` for dimensionless), and valid range.
  An empty variable list is allowed only for nonnumerical protocol/claim records.
- Applicability, source conditions, initial conditions, time update, boundary
  behavior, randomness, assumptions, limitations and uncertainty are mandatory.
  Use `not_applicable: reason` explicitly where a field truly does not apply.
- Domain transfer requires `domain_transfer_required=true` and a substantive
  rationale. E3 always requires transfer treatment. A rationale is an argument
  to review, not automatic permission to transfer a model.
- Calibration, independent/empirical validation and sensitivity plans name the
  intended tests/data and remaining gaps. No field calls the model validated.
- `module`, repository-relative `config_path`, RFC-6901-style `config_pointer`,
  and repository-relative `reference_test` locate implementation use and checks.
  Proposed/unavailable records may name planned paths. Accepted/synthetic records
  require a retained source with matching SHA-256, existing config/test/review paths and a resolvable configuration pointer.
- Decisions: proposed, unavailable, accepted_for_implementation, synthetic. Accepted
  requires verified source review, source hash, supported class and rationale;
  **scientific acceptance still requires the owning sprint's empirical gates**.
  Synthetic records must be E5/synthetic, use `fixture:` URLs and cannot enter the
  production ledger. No implicit defaults or acceptance by file existence.

## Source-review checklist (each verified record)
1. Open the primary source, check authors/title/version/publication and DOI/URL;
   record acquisition date and exact source location. Preserve authorized bytes/hash.
2. Confirm transcription and variable units/dimensions, valid ranges, sampling
   population/material/network and environmental conditions. Mark unavailable
   evidence honestly instead of inferring precise values.
3. Compare target domain against source domain. Document transfer assumptions,
   counterexamples, uncertainty, sensitivity and grounds to reject applicability.
4. Separate published measurements, calibration, scenario settings, assumptions,
   generated states and software-tested properties. Never promote legacy code to
   scientific evidence or replace the approved PLC sources silently.
5. Trace source value/equation to the config pointer and module, then independently
   reproduce the reference calculation with units and tolerances. Keep calibration
   and holdout validation distinct. Define empirical validation and data gaps.
6. Record decision, rationale, reviewer identity/method (author self-audit allowed
   by ADR-0005), tests, actual results, failures and unresolved limitations. Never
   label author checks independent-person review. Changes require revalidation.

## Commands and boundaries
`python scripts/validate_evidence_ledger.py` checks production structure and
acceptance prerequisites; it does not fetch URLs or certify source authenticity.
`python -m unittest discover -s tests -v` includes synthetic source/config tracing
and hostile record mutations. Fixture citations are explicit local synthetic
artifacts, never invented papers. No physical reference result is claimed.
Malformed input exits 1, creates no artifacts and emits field diagnostics without
record contents. Preserve failed inputs privately when sensitive; do not publish
credentials. Roll back ledger edits with a normal revert preserving history.
