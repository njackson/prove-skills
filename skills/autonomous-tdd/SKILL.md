---
name: autonomous-tdd
description: Implements a slice against an acceptance test it may not edit, using strict red-green-refactor without pausing for input, and reports at the end. Use when handed an outer test and told to make it pass, or when the user wants you to just go and build it.
allowed-tools: [Bash, Read, Write, Edit]
---

# Autonomous TDD

You have been handed an acceptance test — the outer test — and the command that runs it. The test
decides when you are done. You did not write it, and you may not change it. Everything below is
the inner loop that runs underneath it until it goes green.

## The one rule

**The acceptance test and its step helpers are not yours to edit.** Not to fix, not to tidy, not to
make pass. If it cannot pass as written — it references something that does not exist, it asserts
something the ticket contradicts — stop and report exactly that. A green reached by changing what
green means carries no information, and the person who handed you the test will check the diff
for it first.

They should not have to check by hand, and neither should you. The rule is one command:

```
git diff --name-only <base>..HEAD -- <spec path> <step helper path>
```

Empty, or you broke it. Run it before you report, put the result in the report, and if the project
gates on CI, add it there as a job so the answer arrives without anyone asking.

The same goes for the gate: no edits to CI configuration, test configuration, skip lists or
timeouts, and no weakening of any existing assertion. If the suite has a flaky test, report it;
do not retry it into silence.

## Before you start

1. Run the outer test. Confirm it fails, and fails for the **right reason** — the behavior is
   missing, not an import error, a typo, or a broken fixture. If it fails for the wrong reason,
   that is a finding; report it rather than working around it.
2. Read the ticket, not only the test. Where the two differ, say so before writing code.
3. Start a **test list**: a plain-text note of the inner tests you intend to write, in order. Add to
   it as you go. It is how a reader later sees what you intended, and it stops you improvising the
   next test under pressure.

## The inner loop

Repeat until the outer test is green:

1. **Write one failing inner test** for the next behavior on the list, in the domain's words where
   the domain has words for it.
2. **Make it pass by the simplest means available.** Three gears, chosen by how sure you are:
   - *Obvious implementation* — when you know how, write it. The common case.
   - *Fake it* — return the constant the test expects. It proves the test can fail and pass, which
     proves the test works. Use it when "obvious" has been wrong twice in a row.
   - *Triangulate* — add a second example the constant cannot satisfy, so the general shape is
     forced rather than guessed. The rarest gear.
3. **Run the full suite.** Anything red, fix it before going on.
4. **Refactor on green**, against Beck's four rules in priority order: passes the tests; reveals
   intention; no duplication; fewest elements. If an abstraction has one implementation and one
   caller, delete it. **Commit the refactor separately from the commit that went green**, so the
   history shows the step happened.
5. Run the full suite again.

**Prefer sociable tests.** Real collaborators; fakes only at the process boundary, and there prefer
the project's nulled wrappers (a `createNull()` factory, or whatever the project calls it) to a
mocking library. If the project has a rule about mocking imports, obey it; if it has none, do not
introduce a mocking library to a codebase that has been living without one.

If a step's red-to-green regularly runs past a few minutes, the steps are too big: revert and take a
smaller one. Reverting ten minutes of work is almost always faster than debugging it.

## Autonomy rules

- **Do not ask for input between steps.** Make the decision, write it down, keep going.
- **On ambiguity**, make the simplest reasonable choice, record it in the decisions list, and put a
  one-line comment at the point in the code where the choice was made.
- **If refactoring breaks a test, undo the refactor.** Green takes priority over clean.
- **Never claim success with failures.** If anything is red at the end, the report says so first.

## Test commands

Use the project's own: if it has an acceptance-test runner, that is the outer loop this inner loop
serves, and its unit-test command is the inner one. If the ticket names the commands, use those. If
nothing does, find them (`package.json`, `Makefile`, `pyproject.toml`, the CI config) and state
which you used in the report.

## Final report

```
## Results

Outer test: green | red (and why)
Suite: X passed, Y failed
Files changed: <list>
Spec and step helpers unchanged: yes — <the command above, and its empty output>

## Commits
- <sha> green: <what>
- <sha> refactor: <what>   ← present, or say why not

## Decisions made
- <decision>: <rationale>

## Not verified
- <the edge you did not cover, the environment you could not reach>

## Test output
<final run>
```

If any tests are still failing, say so clearly — do not claim success with failures.
