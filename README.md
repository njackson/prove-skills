# The Skills

Ten practices written down so an agent applies them without you in the room. They are the companion
files to [**Ship What You Can Prove**](https://prove.natejackson.dev), a self-paced guide to the
XP/BDD/CD practices and what they become when a machine does the typing.

Plain markdown with a small header. Nothing here needs a dashboard, a server, or a framework.

## Install

```sh
npx degit njackson/prove-skills .claude          # this project only
npx degit njackson/prove-skills ~/.claude        # every project on this machine
```

Or clone it and copy what you want:

```sh
git clone https://github.com/njackson/prove-skills
```

The layout matches Claude Code's, so the repo root drops straight into `.claude/`. Other tools have
equivalents; the files themselves are just markdown.

**Then do the thing the files cannot do for you.** A rule here reads as a rule because somebody
watched it get broken. You can copy the paragraph. You cannot copy the afternoon it cost, and a rule
with nothing behind it is a preference that the next reasonable person in a hurry will override. Go
through what you keep and weld your own incidents onto it: what broke, when, how long it took to
find, and what it cost. That edit decides whether these files still exist in six months.

The second edit is subtraction. Where one of these asks an agent to remember something your tooling
could enforce, the enforcement wins. A check costs nothing per session and is obeyed absolutely;
a paragraph costs context every time and is obeyed probabilistically.

## What is here

| Skill | What it does | Kind | Chapters |
|---|---|---|---|
| `refine` | Turn a vague ask into tickets a stranger could pick up cold: story map, example map, grill every open question, name the risks, slice vertically with a walking skeleton first. | Orchestrator — you start it by name | 02, 03 |
| `specify-behavior` | Characterize what exists, turn examples into executable specs, name the domain language, then implement inside the spec. | Discipline | 01, 02, 04, 05 |
| `autonomous-tdd` | The inner loop, run without pausing, against an outer test the agent may not edit. Three gears, four rules, refactor committed separately. | Discipline | 05 |
| `verify-work` | Assemble the evidence that a change works, up a ladder from acceptance to traces, with a required section for what was not verified. | Discipline | 09, 12 |
| `worktree-isolation` | One tree per stream, branched from the remote tip, closed by rebase and never by force; the shared stash stack. | Discipline | 09 |
| `parallel-queue` | Several agents at once without collisions: worktree each, file allow-lists, branch CI as the gate, revert on red, stop after three failures. | Discipline | 09, 11 |
| `improve-agent` | Make an agent measurably better by changing only the text it reads: an ownership line the loop may not cross, a frontier file, a noise floor measured before any claim, one component per round, and a witness for the verdict. | Orchestrator — `/improve-agent` | 11, 13 |
| `guide` | The tutor: picks up where the reader left off, runs one chapter's exercise on their own repository, checks the evidence it was supposed to leave, and has the witness grade it. Keeps `.guide/progress.md`. | Orchestrator — `/guide` | all 13 |
| `panel-review` | A simulated expert panel for design, code or positioning review. This course was reviewed with it. | Orchestrator — `/panel-review` | 06, 11 |
| `agents/witness` | An agent that verifies and cannot edit: its tool list has no write tools, so its report cannot become "I fixed it". | Agent definition | 09 |

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
