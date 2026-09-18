---
name: verify-work
description: Assembles the evidence that a change actually works (acceptance, seam-level tests, mutation, a real run, and traces) into a report the driver can confirm in one pass, with a required section for what was NOT verified. Use when work is finished and needs confirming, when writing a verification or QA report, or before telling anyone something is done.
allowed-tools: [Bash, Read, Write, Edit]
---

# Verify work

Done is not "the agent believes it is done". This assembles what would convince somebody who does
not trust you, and says plainly where that evidence runs out.

## The rule the whole report rests on

**Separate what was measured from what was assumed, in writing.** Every line in the report is one
or the other, and the ones that are assumptions are labeled as assumptions. A report that reads
uniformly confident is not a verification, it is a summary — and the driver cannot tell which
claims to trust, so they end up trusting none of them or all of them, and both are wrong.

## The ladder

Climb as far as the change deserves. A typo fix stops at the first rung; anything touching money,
data, or a user-visible path goes to the top.

**1 — Does it do the thing?** The acceptance level: the behavior a person asked for, expressed as
a scenario rather than a unit — written from outside, in the language of the person who asked.

*If the project already keeps acceptance scenarios* — a spec suite, a feature file, an
acceptance-testing framework — **that pipeline owns this rung.** Cite the scenario
and its result; do not write a second description of the same behavior here. Two descriptions
drift, and the day they disagree the wrong one is already open.

*If it does not*, this rung is yours: state the behavior as a scenario, say how it was exercised,
and say so plainly if the only thing standing behind it is a unit test.

**2 — Does each seam behave?** Sociable tests at the seams: real collaborators, fakes only at the
process boundary. If a test needs the internals mocked to pass, it is testing the mock. Name the
seams covered and the ones left bare.

**3 — Would the tests catch a regression?** This is the rung everyone skips, and it is the one that
decides whether the rest was theatre. If the project has a mutation runner, run it on the changed
files and report the score with the surviving mutants named — a survivor is a line no test is
actually checking. If it has none, **mutate by hand**: break the line the feature depends on, run
the suite, confirm a *named* test goes red, and put it back. One deliberate break, honestly
reported, beats a coverage percentage.

**4 — Does it work outside the test harness?** A real run in a real environment: the command, the
page, the endpoint. Say what you did, in steps somebody could repeat, and what you saw. "Tests
pass" is not this rung — the whole point is the path the tests do not take.

**5 — Can it be seen in production?** Traces and telemetry: is the new path instrumented, does the
span appear, would a failure page anybody. An async path that fails silently is not finished,
however green — the caller returned successfully, and the failure is now somebody's Thursday.

*If the project has a telemetry convention* — declarations, a span-naming scheme, a dashboard —
follow it and point at the result rather than inventing a parallel account. *If it has none*, say
which of these questions you could not answer, because that is the honest report.

## The report

Write it as markdown — in the pull request description, or wherever the project keeps verification notes — and lead with the verdict rather than the journey.

- **What was asked for**, in one sentence.
- **What was done**, in two or three.
- **The evidence**, one line per rung: what was run, and what it showed. Numbers where there are
  numbers. Commands the driver could paste.
- **What was NOT verified.** Required, and never empty — there is always something: an untested
  edge, an environment you could not reach, a rung you decided the change did not deserve. If this
  section is hard to fill, that is a sign you have not thought about it, not that the work is
  perfect.
- **What would change the verdict** — the one thing you would look at first if it turns out broken.
- Then a short list of anything the driver has to decide, and anything you propose doing next. One line each.

Keep those headings in a template file and have something check them. A four-line script that reads
the report and exits non-zero when the not-verified section is missing or empty catches the case
this discipline is worst at catching: the report written at the end of a long day by somebody who
has already decided the work is fine.

## Who should run this

You can. But where the change is somebody's own work — including yours — dispatch it to the
**`witness`** agent instead. It has no edit tools, so it cannot quietly repair what it finds and
report success, which is the failure this discipline is least able to catch in itself. Bash still
lets it write, so that is a guardrail rather than a jail; the point is that fixing is not on its
path of least resistance.

## This skill is complete on its own

Every rung above says what to do when nothing else fills it. Where another tool DOES fill one, the
rule is not "delegate the work" — it is **do not produce a second artifact describing the same
thing**. Cite theirs. That way the report is honest in a project with a full acceptance suite and
in a project with nothing but a test runner, and neither arrangement is the one it was written for.

## Two failure modes this exists to prevent

**Reporting finished because the loop ended.** A run that dies mid-token and reports success is the
most common way agent work goes wrong. Doneness is externally observable — a green build, a merged
branch, a scenario passing — or it is not established.

**Verifying the thing you built rather than the thing that was asked for.** Re-read the ticket
before writing the report, not from memory. Where the two differ, that difference IS the report's
most important line.
