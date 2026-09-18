# The Skills

Practices written down so an agent applies them without you in the room. Companion plugins to
[**Ship What You Can Prove**](https://prove.natejackson.dev), a guide to the XP/BDD/CD practices and
what they become when a machine does the typing.

## Install

```
/plugin marketplace add njackson/prove-skills
```

Then install whichever you want:

```
/plugin install specify-first@prove-skills
/plugin install test-first@prove-skills
/plugin install parallel-agents@prove-skills
/plugin install improve-agent@prove-skills
/plugin install panel-review@prove-skills
/plugin install ship-what-you-can-prove@prove-skills
```

| Plugin | What it is for | Chapters |
|---|---|---|
| [`specify-first`](./plugins/specify-first) | Turn a vague ask into concrete examples and executable specs before any code exists: map the journey, settle every open question, name the domain language, and characterize what is already there before changing it. | 01 – 05 |
| [`test-first`](./plugins/test-first) | Build against an acceptance test the agent may not edit, run the inner loop without pausing, and finish with evidence instead of a report of success, including a required section for what was not verified. | 05, 09, 12 |
| [`parallel-agents`](./plugins/parallel-agents) | Run several agents at once without them corrupting each other: one git worktree per stream, explicit file allow-lists, branch CI as the merge gate, and a queue that stops rather than thrashing. | 09, 11 |
| [`improve-agent`](./plugins/improve-agent) | Make an agent measurably better by changing only the text it reads. Measures the noise floor before it claims anything, changes one component per round, and keeps a change only when it clears the spread. | 11, 13 |
| [`panel-review`](./plugins/panel-review) | A simulated panel of named practitioners reviews a design, a diff or a positioning draft, each from their own published positions, then the findings are verified against the code before any of them become tickets. | 06, 11 |
| [`ship-what-you-can-prove`](./plugins/ship-what-you-can-prove) | Run the guide as a self-paced course inside this session: one chapter's exercise against your own repository, checked for the evidence it was supposed to leave, graded by an agent that cannot edit anything. | all 13 |

The witness agent, which verifies work and has no tools that can write, ships with every plugin that
dispatches it.

**Then do the thing the files cannot do for you.** A rule here reads as a rule because somebody
watched it get broken. You can copy the paragraph. You cannot copy the afternoon it cost, and a rule
with nothing behind it is a preference that the next reasonable person in a hurry will override. Go
through what you keep and weld your own incidents onto it: what broke, when, how long it took to
find, and what it cost. That edit decides whether these files still exist in six months.

The second edit is subtraction. Where one of these asks an agent to remember something your tooling
could enforce, the enforcement wins. A check costs nothing per session and is obeyed absolutely;
a paragraph costs context every time and is obeyed probabilistically.

## Two rules the set is built on

**Practice or apparatus.** Everything here passes one test: could you do it with a text editor and
a test runner? Skills that need a particular pipeline, server or storage layout were left behind
where they belong, with the tool that provides them. That is also why these say "if the project
keeps acceptance scenarios" and never name a product: naming one makes a skill read as broken
wherever that product is absent.

**Orchestrator or discipline.** An orchestrator is started by a person and runs phases with
hand-offs. A discipline is loaded by the agent on its own because the moment matched. A discipline
holds the rule that would be true in any codebase; your project's own skill holds its paths, its
thresholds and the incidents that set them, and leans on the discipline for the rest. Chapter 08 of
the guide is the full treatment.

## Every skill is complete alone

Each one says what to do when nothing else fills the role. Where your project already owns a role
— an acceptance suite, a telemetry convention, a preflight script — the instruction inside is "cite
theirs, do not write a second one". Two descriptions of one behavior drift, and the day they
disagree the wrong one is already loaded.

## License

MIT. Copy them, change them, ship them; keep the notice.
