---
name: panel-review
description: Stages a review by a panel of named practitioners simulated from their published positions, then reduces what they said to an issues table with no names left in it. Use when a design, a diff or a piece of positioning is about to be accepted and nobody available disagrees with it hard enough, or when somebody asks for a panel review, a mob review or a second opinion with teeth.
# An orchestrator: the driver starts it by name.
disable-model-invocation: true
allowed-tools: [Bash, Read, Glob, Grep, Agent]
---

# Panel Review

Simulate a review by an expert panel of influential voices in testing, BDD, observability, and software design. Panelists respond in character based on their published positions, talks, books, and known intellectual tendencies.

> **Disclaimer:** These are simulated responses based on each person's published positions, talks, books, and known intellectual tendencies. They represent what I believe each person *would likely say*, not what they have actually said about this project.

## Setup Flow

Before executing any review, walk through these steps with the user:

### 1. Review Type

Ask the user which type of review:

| Type | Input | Focus |
|---|---|---|
| **Design** | Docs, plans, design documents | Architectural soundness, trade-offs, scope, feasibility, missing considerations |
| **Code** | File paths, git diff range, branch changes | Code quality, test coverage, decomposition, naming, error handling, seams, dependencies |
| **Positioning** | Narratives, blog drafts, competitive analysis | Messaging clarity, audience targeting, competitive framing, defensibility, tone |
| **Combined** | Mix of the above | User specifies which combination |

### 2. Materials Under Review

Ask what specific files, docs, or diff range to review. For code reviews, get the file paths or git range. For design reviews, get the document paths. Read all materials before proceeding.

### 3. Panel Composition

Present the default panel and ask if the user wants to add or remove anyone:

**Default Panel:**

| Panelist | Lens |
|---|---|
| Kent Beck | TDD, simplicity, test quality |
| Martin Fowler | Refactoring, architecture, DSL design |
| Charity Majors | Operations, observability, failure modes |
| Dave Farley | Acceptance test architecture, continuous delivery |
| JB Rainsberger | Contract testing, economics, boundaries |
| Dave Thomas | Pragmatism, DRY, over-engineering |
| Dan North | BDD, behavioral language, discovery |
| Liz Keogh | Deliberate discovery, uncertainty, complexity |
| Michael Feathers | Legacy code, seams, testability, characterization tests |
| Emily Bache | Approval testing, test quality, refactoring katas |

If the user adds a custom panelist, ask for: name, lens, and a short persona description. The
expanded personas for the default eleven are in `reference/panelists.md`, one hop from here; they
are only needed once the panel is settled, so do not read them at setup.

### 4. Review Mode

Ask: **Group review (mob)** or **Individual reviews (parallel subagents)?**

- **Group (mob):** All panelists review together in a single roundtable discussion in the main conversation.
- **Individual (parallel):** Each panelist is dispatched as a separate subagent. Results are synthesized into a group discussion afterward.

## Executing a Group (Mob) Review

Write the review as a flowing roundtable discussion. Structure it as:

1. **Opening Round** — Each panelist states what they want to focus on
2. **Deep Dives** — Organized by topic. Panelists build on, challenge, and disagree with each other. Reference specific file:line locations for code reviews.
3. **Key Debates** — Where panelists disagree, let the debate play out
4. **Individual Verdicts**
5. **Group Consensus** — What N/M panelists agree on

End with the **Structured Summary** (see below).

## Executing Individual (Parallel) Reviews

Dispatch each panelist as a separate subagent using the Task tool with `subagent_type: "general-purpose"`.

### The subagent prompt

The prompt template and the expanded personas are in `reference/panelists.md`. Read that file when
you dispatch, fill in `{name}`, `{lens}` and `{persona}` per panelist, and keep the output format it
specifies so the synthesis round has the same shape from every subagent.


### Synthesis Round

After all subagents return:

1. Collate all individual findings by topic
2. Identify where panelists agree and disagree
3. Write a synthesis section where panelists react to each other's findings (group discussion format)
4. Produce the **Structured Summary** (see below)

## Structured Summary

Every review — group or individual — ends with this structure:

### Cross-Cutting Themes
What N/M panelists agree on, ordered by how many raised the point.

### Key Debates
Where panelists disagree, with both sides stated.

### Issues Table

| ID | Severity | Description | Lens | Effort |
|---|---|---|---|---|
| C-1 | Critical | ... | testability, CI fitness | ... |
| I-1 | Important | ... | observability | ... |
| S-1 | Suggestion | ... | pragmatism, DRY | ... |

**Lens** describes the technical concern that surfaced the issue (e.g., "observability", "test economics", "naming/DX"), NOT the panelist name. Panelist names are for the review narrative — they must NOT leak into issue descriptions, tickets, or downstream work items.

Severity levels:
- **Critical** — Must fix before shipping
- **Important** — Should fix before or shortly after shipping
- **Suggestion** — Nice to have, consider for later

### Individual Verdicts
One sentence per panelist with their name in bold.

### Group Consensus
Overall assessment — ship / ship with caveats / needs work. State the vote (e.g., "9/10 panelists agree...").

## Ticketing Findings

When creating tickets (Linear, GitHub Issues, etc.) from review findings:

- **Do NOT reference panelist names** in ticket titles, descriptions, or comments. These are simulated personas — attributing findings to them is misleading outside the review context.
- Describe each issue on its **technical merits only**: what the problem is, where it is, why it matters, and how to fix it.
- Use the **Lens** column (e.g., "observability", "test economics") for categorization, not attribution.

That last rule is checkable, so check it rather than trusting yourself at the end of a long review:
before anything is filed, grep the ticket bodies for each panelist's surname and refuse on a hit.
Eleven names in a file and one `grep -F -f` is the whole control.

### Ticketing Triage

After creating tickets from the issues table, do a three-pass triage with the user:

**Pass 1 — Verify findings against code.** Before triaging, spot-check panelist claims against the actual codebase. Simulated reviewers sometimes assert things that aren't true (wrong dependency format, missing features that exist, etc.), confidently, in the register of somebody who checked. Flag and discard false positives. Skip this pass and the output is a backlog of wrong tickets that somebody has to disprove one at a time, which costs more than the review saved.

**Pass 2 — Sort into vetted vs. needs refinement.** Present all validated findings and categorize:

| Category | Criteria | Action |
|---|---|---|
| **Vetted → Todo** | Clear what to do, no design decisions, could be described to any engineer | Move straight to Todo status |
| **Needs refinement** | Requires a design decision, API design, naming choice, scope decision, or content strategy | Leave in Backlog |

**Pass 3 — Quick-vet the borderline items.** Review the "needs refinement" list and identify items where a simple, defensible decision can be made without the user. Present as a summary table for the user to approve or override:

| Ticket | Decision | Rationale |
|---|---|---|
| AI-NNN | [one-line decision] | [one-line why] |

Move approved items to Todo with the decision captured in the ticket body.

**What remains** after Pass 3 are the **real design questions** — items that genuinely need collaborative discussion. Present these grouped by natural clusters (related subsystems, coupled API decisions, content vs. code), with a "What needs deciding" column:

| Ticket | Description | What needs deciding |
|---|---|---|
| **AI-NNN + AI-MMM** | [cluster name] | [the actual design question] |

Clustering helps the user see which items can be refined together in a single conversation, and which are independent decisions. Common cluster types:
- Items touching the same subsystem or protocol
- Coupled API design decisions (where one choice constrains another)
- Content/docs vs. code work
- Feature design (new public API surface)

## Output

Save the review where the project keeps its decision records — a `docs/`, `plans/` or
`decisions/` directory if one exists, named `YYYY-MM-DD-<topic>-<review-type>-review.md`. If
there is no such place, or the user asks to skip saving, present it conversationally instead.

The saved file should use the format:

```markdown
# {Review Type} Review: {Topic}

**Date:** YYYY-MM-DD
**Format:** Simulated {mob review / individual reviews with synthesis}
**Scope:** {what was reviewed}
**Panelists:** {comma-separated list with lenses}

> **Disclaimer:** These are simulated responses based on each person's published positions, talks, books, and known intellectual tendencies. They represent what I believe each person *would likely say*, not what they have actually said about this project.

---

{review body}

---

{structured summary}
```
