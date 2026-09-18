# The Skills

Ten practices written down so an agent applies them without you in the room. They are the companion
files to [**Ship What You Can Prove**](https://prove.natejackson.dev), a self-paced guide to the
XP/BDD/CD practices and what they become when a machine does the typing.

Plain markdown with a small header. Nothing here needs a dashboard, a server, or a framework.

## Install

Six plugins in a Claude Code marketplace. The first line registers it; each line after installs one.

<!-- install:start -->
```sh
/plugin marketplace add njackson/prove-skills
/plugin install specify-first@prove-skills
/plugin install test-first@prove-skills
/plugin install parallel-agents@prove-skills
/plugin install improve-agent@prove-skills
/plugin install panel-review@prove-skills
/plugin install ship-what-you-can-prove@prove-skills
```
<!-- install:end -->

The first line registers the marketplace; each line after it installs one plugin. Take the ones you
want and leave the rest: a skill does its job with its neighbors absent, so skipping a plugin costs
you a pointer rather than a step.

**Then do the thing the files cannot do for you.** A rule here reads as a rule because somebody
watched it get broken. You can copy the paragraph. You cannot copy the afternoon it cost, and a rule
with nothing behind it is a preference that the next reasonable person in a hurry will override. Go
through what you keep and weld your own incidents onto it: what broke, when, how long it took to
find, and what it cost. That edit decides whether these files still exist in six months.

The second edit is subtraction. Where one of these asks an agent to remember something your tooling
could enforce, the enforcement wins. A check costs nothing per session and is obeyed absolutely;
a paragraph costs context every time and is obeyed probabilistically.

## What is here

The grouping follows what hands off to what, rather than the order the chapters come in. The first
thing `parallel-queue` gives an agent is its own worktree, and it sends you to `worktree-isolation`
for how, so those two travel together. `specify-behavior` stops at the point where red-green-refactor
starts and names `autonomous-tdd` as what runs it, and that hand-off crosses from the first plugin to
the second. Three of the skills dispatch the witness, so the witness ships inside all three of their
plugins: one file, three copies, written out from a single source every time the marketplace is
built.

<!-- plugins:start -->
| Plugin | What it is for | What it installs | How it starts | Chapters |
|---|---|---|---|---|
| [`specify-first`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/specify-first) | Turn a vague ask into concrete examples and executable specs before any code exists: map the journey, settle every open question, name the domain language, and characterize what is already there before changing it. | [`refine`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/specify-first/skills/refine/SKILL.md) | By name | 02 · 03 |
|  |  | [`specify-behavior`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/specify-first/skills/specify-behavior/SKILL.md) | On a match | 01 · 02 · 04 · 05 |
| [`test-first`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/test-first) | Build against an acceptance test the agent may not edit, run the inner loop without pausing, and finish with evidence instead of a report of success, including a required section for what was not verified. | [`autonomous-tdd`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/test-first/skills/autonomous-tdd/SKILL.md) | On a match | 05 |
|  |  | [`verify-work`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/test-first/skills/verify-work/SKILL.md) | On a match | 09 · 12 |
|  |  | [`agents/witness`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/test-first/agents/witness.md) | Dispatched | 09 |
| [`parallel-agents`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/parallel-agents) | Run several agents at once without them corrupting each other: one git worktree per stream, explicit file allow-lists, branch CI as the merge gate, and a queue that stops rather than thrashing. | [`worktree-isolation`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/parallel-agents/skills/worktree-isolation/SKILL.md) | On a match | 09 |
|  |  | [`parallel-queue`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/parallel-agents/skills/parallel-queue/SKILL.md) | On a match | 09 · 11 |
| [`improve-agent`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/improve-agent) | Make an agent measurably better by changing only the text it reads. Measures the noise floor before it claims anything, changes one component per round, and keeps a change only when it clears the spread. | [`improve-agent`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/improve-agent/skills/improve-agent/SKILL.md) | By name | 11 · 13 |
|  |  | [`agents/witness`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/improve-agent/agents/witness.md) | Dispatched | 09 |
| [`panel-review`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/panel-review) | A simulated panel of named practitioners reviews a design, a diff or a positioning draft, each from their own published positions, then the findings are verified against the code before any of them become tickets. | [`panel-review`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/panel-review/skills/panel-review/SKILL.md) | By name | 06 · 11 |
| [`ship-what-you-can-prove`](https://github.com/njackson/prove-skills/tree/HEAD/plugins/ship-what-you-can-prove) | Run the guide as a self-paced course inside this session: one chapter's exercise against your own repository, checked for the evidence it was supposed to leave, graded by an agent that cannot edit anything. | [`guide`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/ship-what-you-can-prove/skills/guide/SKILL.md) | By name | all 13 |
|  |  | [`agents/witness`](https://github.com/njackson/prove-skills/blob/HEAD/plugins/ship-what-you-can-prove/agents/witness.md) | Dispatched | 09 |
<!-- plugins:end -->

`tools/plugins.py` holds the one definition of which skill is in which plugin. The table above, the
install lines, and the guide's skills page are all generated from it, so none of them can describe a
grouping the marketplace does not have. Run `python3 tools/skills_page.py` after changing it.

None of that grouping is a dependency. Install one plugin and its skills run; what you lose is the
pointer at a file you do not have.

## Two rules the set is built on

**Practice or apparatus.** Everything here passes one test: could you do it with a text editor and
a test runner? Skills that need a particular pipeline, server or storage layout were left behind
where they belong, with the tool that provides them. That is also why these say "if the project
keeps acceptance scenarios" and never name a product: naming one makes a skill read as broken
wherever that product is absent.

**Orchestrator or discipline.** An orchestrator is started by a person and runs phases with
hand-offs; those carry `disable-model-invocation: true` and show up as *by name* in the table. A
discipline is loaded by the agent on its own because the moment matched. A discipline holds the rule
that would be true in any codebase; your project's own skill holds its paths, its thresholds and the
incidents that set them, and leans on the discipline for the rest. Chapter 08 of the guide is the
full treatment.

## Every skill is complete alone

Each one says what to do when nothing else fills the role. Where your project already owns a role
— an acceptance suite, a telemetry convention, a preflight script — the instruction inside is "cite
theirs, do not write a second one". Two descriptions of one behavior drift, and the day they
disagree the wrong one is already loaded.

## License

MIT. Copy them, change them, ship them; keep the notice.
