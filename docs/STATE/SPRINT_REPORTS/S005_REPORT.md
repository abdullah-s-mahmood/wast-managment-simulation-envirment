# S005 — Terminology, units, and identifier conventions

Date 2026-10-22, Asia/Baghdad. Branch sprint/S005-conventions.
Base 3799b5cdf9a2e5355885d93a86c492490cb1aced. Evidence E-S005-01;
ADR-0002/0003/0004/0005. Local checks and CI/integration recorded below.

## Gap, files and decisions
Added docs/conventions/README.md (glossary, unit/coordinate/time/ID rules),
units.json (external versioned exact conversion catalog), read-only
scripts/check_conventions.py, and tests/test_conventions.py. Inventory/state/log
and this report are the only dependent changes. No simulation/runtime schemas,
physical relationship or scenario parameter accepted. Conversion factors are
unit definitions, not empirical parameters. No new architecture ADR required.

Author self-audit: all 12 quantity categories carry explicit dimensions and
canonical units, including absolute versus interval temperature, relative
humidity versus other humidity measures, mass versus emission rate, and fuel
volume versus energy. No density/energy inference. UTC requires known explicit
offset; IDs survive display-name changes. Invalid data fail without writes.
The humidity checker deliberately supports a bounded [0,1] input profile; it is
not a universal scientific assertion that supersaturation cannot occur.

## Source evidence and scope
Accessed primary sources via web tool 2026-10-22:
- BIPM SI Brochure ninth edition V2.01 December 2022, English §§2.3.1–2.3.4,
  §3/Table 7, §4/Table 8; https://www.bipm.org/documents/d/guest/si-brochure-9-2_01
- RFC3339 §§4.2, 5.6–5.8; https://www.rfc-editor.org/info/rfc3339/
- RFC7946 §§3.1.1, 4; https://www.rfc-editor.org/rfc/rfc7946.html
Links and exact sections are in policy. No source bytes copied into repository.
No physical evidence record is accepted by this conventions sprint. Coordinate
transforms remain S037; no implementation/geodesy verification claimed now.
A first web open of RFC7946 without .html timed out; .html primary source opened.

## Commands, original failures and actual results
Linux x86_64 / Python 3.11.15, standard library only.
- python -m unittest discover -s tests -p test_conventions.py -v:
  first exit 1 (test-first missing module); after implementation exit 0, 6 tests.
  Added malformed-offset attack +01:99; exit 1 (Python silently normalized it).
  Added strict offset hour/minute bounds; exit 0, same 6 tests including attack.
- Final suite and validators: E-S005-01 below records actual observed results.

WB: quantity dimensions, explicit catalog version, numeric/domain guards, IDs.
BB: public CLI and independent Fraction reference values for every quantity.
Adversarial: unknown/cross-dimension units, Celsius/Kelvin confusion, humidity
bounds, negative absolute temperature, nonfinite/bool/oversized numbers, naive
local time, unknown offset, invalid date/offset, leap seconds, finer precision,
duplicate/malformed IDs. Metamorphic: 101 generated distance/speed equivalents.
Equivalent timestamps normalize identically; renamed duplicate labels retain IDs.
Reference checks use exact rational arithmetic, no tolerance/float assumptions.
NOT RUN: Windows, SUMO/ns-3, physical/empirical or coordinate-transform validation;
no such runtime, model or transform is implemented/advertised by S005.
Residual limits: narrow UTC profile, restricted unit allow-list and humidity
profile; no runtime rounding policy or natural-language dimensional inference.
Next eligible after accepted merge: S006.
