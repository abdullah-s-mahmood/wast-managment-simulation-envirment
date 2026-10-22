# Terminology, units, coordinates, time and identifiers

S005 sets representation policy, not model equations, parameter values or runtime
schemas. ADR-0002/0003/0004 still apply. Future adapters must preserve original
values/units and record conversion, version and provenance alongside normalized
values; these conventions alone do not establish physical accuracy.

## Glossary
| Term | Meaning |
|---|---|
| model | Versioned behavior/relationship with evidence, domain and tests. |
| hypothesis | Testable statement about behavior; separate from chosen cases. |
| specification | Stable entity design attributes with units and provenance. |
| scenario | A selected case: map, population, climate, instances, policy and inputs. |
| runtime state | Mutable state during a run; not an input specification. |
| measurement | Raw time-stamped observation with units/source, including failed-run context. |
| telemetry | Explicitly allow-listed sampled/transmitted data, distinct from internal state. |
| outcome | Predefined derived quantity with formula, units and provenance. |
| run / replicate | One execution / separately identified execution in a declared design; dependence and seed rules must be recorded. |
| latency / elapsed time | Duration / duration since declared simulation origin, both in seconds; neither is wall-clock timestamp. |
| emissions | Specify substance and whether mass, mass rate, concentration or other quantity; these are not interchangeable. |
| fuel | Specify substance and whether volume, mass or energy; no density/heating-value conversion without evidence. |
| fill | Explicitly distinguish occupied volume, mass and capacity fraction; no density assumption. |

## Unit policy
Use catalog version 1 in units.json. Unit tokens are case-sensitive ASCII
representations: m3 means cubic metre, degC means degree Celsius, and 1 means
dimensionless. L is an explicitly supported input token. Unknown aliases fail;
no guessing from a variable name. Source units remain in provenance.

| Quantity | Canonical token | Dimension | Supported alternative input |
|---|---|---|---|
| distance | m | L | km |
| mass / emission_mass | kg | M | g; emission_mass also mg |
| volume / fuel_volume | m3 | L^3 | L |
| temperature | K | Theta | degC (absolute-temperature offset) |
| temperature_interval | K | Theta | degC (no offset; signed difference) |
| humidity | 1 | 1 | % (relative humidity fraction only) |
| speed | m/s | L/T | km/h |
| emission_rate | kg/s | M/T | g/s |
| latency | s | T | ms |
| elapsed_time | s | T | min, h |

The table is a project allow-list. Context-specific model ranges require their
own evidence; this checker only rejects negative magnitudes/absolute temperature
and humidity outside the chosen bounded input profile [0,1]. This restricted
profile does not claim supersaturation is physically impossible; supporting it
requires an explicit future contract/domain decision. Signed temperature differences are allowed. It does
not normalize absolute humidity, emission concentration or fuel energy. No
implicit defaults, NaN/Infinity, guessed units or cross-dimension conversions.

BIPM defines SI base/derived units, prefixes, Celsius temperature and accepted
non-SI units. Our catalog uses exact rational scale/offset arithmetic. The
conversion is canonical_value = input_value * scale + offset; coefficients
are in units.json, not scenario defaults. Reference examples: 1 km = 1000 m,
1000 L = 1 m3, 36 km/h = 10 m/s, 0 degC = 273.15 K, 50% = 0.5.
A 1 degC temperature difference equals 1 K without the absolute offset.
See [BIPM SI Brochure, ninth edition, version 2.01, December 2022](https://www.bipm.org/documents/d/guest/si-brochure-9-2_01),
English §§2.3.1–2.3.4, §3/Table 7 and §4/Table 8. Accessed 2026-10-22;
conversion coefficients derive from these definitions, not measured model fits.

## Coordinates
GeoJSON boundaries follow [RFC 7946 §§3.1.1 and 4](https://www.rfc-editor.org/rfc/rfc7946.html):
WGS84/CRS84 longitude then latitude, in decimal degrees; optional height is metres
relative to its ellipsoid. Internal projected x/y require an explicit CRS,
axis order, units, transformation method/version and provenance. Never treat
degrees as metres or infer projection from city names. Reject missing CRS,
unknown axes or mixed conventions before distance/routing calculations. S037
will implement transforms; this sprint implements none and claims no geodesy test.

## Time
Use a documented subset of [RFC 3339 §§4.2, 5.6–5.8](https://www.rfc-editor.org/info/rfc3339/):
explicit-offset calendar timestamps, uppercase T/Z, up to six decimal second
digits, normalized to UTC with six digits and Z. Original offset is retained by
future provenance adapters. Naive local timestamps, unknown offset -00:00,
invalid dates/offsets, leap seconds and finer precision fail explicitly. This
is a narrower project profile, not a claim of full RFC3339 support. It makes no
assumption about a source's timezone. Offset syntax is insufficient to verify
that a local clock was correct. Source clock/timezone uncertainty must be recorded.

Simulation elapsed seconds start from an explicit origin and are separate from
wall-clock/provenance timestamps. No conversion to local time determines event
order. Tie-breaking, timestep and integer-tick resolution are deferred to S079;
wall-clock UTC normalization does not establish simulator determinism.

## Stable identity
Entity IDs follow `<lowercase_type>-<opaque_token>`: type matches
[a-z][a-z0-9_]*, token is 1–64 ASCII letters/digits/underscore/hyphen and begins
with a letter/digit. IDs are case-sensitive, immutable and unique within their
entity collection; references include the collection/run scope. Never derive
identity from display_name, location, array index or mutable attributes. Duplicate
labels are permitted; duplicate IDs fail. Renaming preserves IDs; deletion does
not authorize reuse. Separate run/replicate IDs prevent cross-run collisions.
Existing sprint Snnn, evidence EV-*, ADR-* and table concept IDs keep their own
accepted namespaces. Allocation/reference rules are finalized in S025–S036.

## Reference checker boundary
`scripts/check_conventions.py` is read-only governance tooling. Quantity values
are decimal strings (at most 80 characters; exponent magnitude <=100, a resource
limit). It returns an exact rational numerator/denominator, canonical unit and
dimension; no float precision or rounding policy is silently selected. A future
runtime adapter must declare its numeric representation/tolerance independently.
Public functions document quantity, timestamp and entity checks. CLI examples:
`python scripts/check_conventions.py quantity speed 36 km/h` and
`python scripts/check_conventions.py timestamp 2026-10-22T02:00:00+03:00`.
Invalid data exits 1; invalid CLI syntax exits 2. No files are written. Run
`python -m unittest discover -s tests -p test_conventions.py -v` for independent
rational references, equivalent-unit sweeps, ambiguous times and stable-ID attacks.
