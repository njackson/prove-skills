---
name: specify-behavior
description: Takes a behavior from "nobody is sure what it does" to an executable specification: characterizes what exists before changing it, turns examples into specs, and names the domain language. Use before changing code whose behavior is not pinned, when turning examples or a mapped story into tests, or when the words for a concept keep shifting.
allowed-tools: [Bash, Read, Write, Edit]
---

# Specify behavior

The middle of the pipeline: discovery has produced examples, implementation has not started, and
the gap between them is where most rework is created. Four practices, none invented here and none
belonging to any one tool.

## 1 — Characterize what already exists

*Feathers.* Before changing code whose behavior nobody can state confidently, **pin the behavior
you have** — not the behavior you want.

Write tests that assert what the code actually does today, including the parts that look wrong.
Run them; they pass by construction. Now a change that alters behavior makes one fail, and you
find out which behavior you altered instead of discovering it in production.

The discipline is in the ordering: characterize, then change. Reversed, the test is written to
agree with the change, and it proves nothing. And when a characterization test pins something
plainly wrong, that is a finding to raise — not a license to fix it in the same commit.

That ordering is checkable, so check it rather than trusting it: the characterization commit touches
test files only, and `git show --stat` on it lists nothing under the source tree. If it does, the
characterization and the change went in together and the pin is worthless.

**Skip this only when the behavior is genuinely new.** "I read the code and it is obvious" is the
sentence that precedes the discovery that it was not.

## 2 — Turn examples into specifications

*Adzic — specification by example.* The examples that came out of mapping are already the spec;
what remains is making them executable without losing their language.

- One example, one specification. A test asserting three examples fails as one and tells you least
  where it hurts most.
- Keep the example's own values. Rounding "$47.30 on a 12-unit order" to "some price" throws away
  the reason the example was chosen.
- Write it from outside — the behavior a person can observe, not the function that implements it.
  A spec that names private functions is a spec that will be rewritten when the internals move,
  which is the moment you most want it unchanged.
- The awkward examples are the specification. The happy path is the part everyone gets right.

## 3 — Name the domain language

*Evans — ubiquitous language.* One concept, one word, everywhere: the conversation, the spec, the
code, the schema. Where the driver says "run" and the code says "execution" and the table says
`job`, three people are maintaining a translation nobody wrote down.

Propose names and have them confirmed before the vocabulary is baked into signatures and columns —
renaming is cheap in a document and expensive in a migration, where the cost arrives as downtime
rather than as an afternoon. Where the project already has a
glossary or a domain module, that is the authority; adopt it rather than coining beside it.

## 4 — Implement inside the spec

Only now. Red-green-refactor against the specification from outside — `autonomous-tdd` runs that
inner loop — with the characterization tests still passing the whole way, since they are the
statement that you changed *only* what you meant to.

## Where the stages are recorded

The progression — *unknown → characterized → specified → implemented* — is the practice. Some
projects track it explicitly, with named maturity stages a scenario advances through and a gate at
each; an acceptance-testing framework will usually own that, and where one exists, record the
stages there rather than keeping a private copy.

Where nothing tracks it, the progression still applies and the evidence is the tests themselves:
characterization tests that pass, specifications derived from named examples, and a domain
vocabulary the driver has agreed to. The bookkeeping is optional. The order is not.
