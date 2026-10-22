# Risk register and escalation protocol

Authority: AGENTS.md, ADR-0004/0005, S008. risks.json lists monitored risks, not
probabilities, calibrated thresholds or claims that future gates already failed.
Each record has stable ID, affected sprint IDs, impact, trigger, mitigation,
owner/action, unblock condition, authority path and explicit status. No hidden
numeric risk scores or invented physical limits. Risk status is distinct from
sprint status. Existing STATE/BLOCKERS.md holds concrete triggered dependencies.

## Safe next action
Inspect progress, earliest eligible sprint, handoff, blockers, report and exact
head before edits. Determine facts from observed evidence, never silence/chat
memory. Prioritize the first applicable action; retain every coexisting blocker.

1. Corrupt/partial results: stop pipeline and downstream analysis immediately,
   mark run failed, preserve immutable raw inputs/hashes/logs/minimal reproducer.
2. Missing required scientific evidence or guessed value: stop the affected gate,
   record quantity/source/domain/units/data missing, and retain provisional or
   unavailable status. Authorization cannot turn a guess into scientific evidence.
3. Irreversible/destructive, paid, privacy-sensitive or externally restricted
   action lacking required specific authority: prepare the reviewable result,
   preserve safe work and request only the missing authorization/permission.
4. Mandatory test/CI failure: investigate actual cause, retain original failure,
   fix within sprint, rerun relevant tests and exact-head CI. Unavailable required
   platform/tool/data is NOT RUN, not NOT_APPLICABLE and not acceptance.
5. Otherwise continue within the accepted contract autonomously: routine edits,
   installs, tests, focused PRs and permitted merges need no repeated permission.

Scientific “available” means all evidence required by the current task is present;
a documentation-only task with no scientific claim may record a scope rationale.
No helper can authenticate these declarations or grant external authorization.
The next_action public function in validate_risk_protocol.py requires all six
strict boolean observations and returns these five action codes without writes.
Its irreversible flag also represents the authorization-sensitive classes in item
3. It does not contact the owner, alter state or start a pipeline. The calling
agent must still record exact facts and all blocked actions; precedence never
removes lower-priority blockers. Malformed/missing declarations raise ValueError.

## Durable blocker and recovery record
For every triggered risk record blocker ID, affected sprint/run, observed trigger,
commands/source locations/hash evidence, exact missing item, risk if guessed,
owner/action, safe work completed, condition to resume and next safe action.
Link report/validation evidence. Preserve failed runs and negative results.
Owner/action identifies responsibility; it does not require messaging another
person or asking the owner for routine decisions. Ask only for the genuinely
missing external input/authorization after independently checking available sources.

Transitions follow AGENTS.md: in_progress -> blocked when work cannot satisfy a
mandatory gate; blocked -> in_progress only with resolving evidence. Completed
regressions need a documented reopen decision, not silent deletion of acceptance.
Keep original blocker history and append resolution date/evidence. Revalidate
changed source/contracts, preserve failed artifacts and require the owning sprint's
full acceptance gate and permitted integration before completed. Run doc validator
after progress changes; update report, handoff, validation log and next sprint.

A resumed agent follows the recorded unblock action instead of retrying a missing
source, guessing a constant, fabricating CI or bypassing permissions. If safe
independent work remains within the same sprint it may continue; later sprints
cannot skip a blocked prerequisite. Research-source/license ambiguity that affects
validity stops the affected work until evidenced, without inventing a substitute.

Run `python scripts/validate_risk_protocol.py` and
`python -m unittest discover -s tests -p test_risk_protocol.py -v`. The CLI checks
register structure/authority paths, exits 0/1 and writes nothing. Tests cover every
six-boolean combination plus malformed facts, missing fields and duplicate IDs.
This is a software policy check, not proof risks were detected or sources exist.
No physical parameter, unit conversion, simulation time or seed is introduced.
