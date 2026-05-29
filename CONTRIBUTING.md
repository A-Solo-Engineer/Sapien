# Contributing to Sapien

First — thank you for being here.

Sapien is an ambitious long-term research direction. It is not a finished
product. It is an evolving idea that needs critical thinkers, researchers,
builders, and honest skeptics to grow into something real.

Every contribution matters — whether it is a challenge to the core ideas,
a refinement of the architecture, a formal proof, or a single sentence
that makes the documentation clearer.

---

## Table of Contents

1. [Who Should Contribute](#1-who-should-contribute)
2. [Ways to Contribute](#2-ways-to-contribute)
3. [What Sapien Needs Most](#3-what-sapien-needs-most)
4. [How to Contribute](#4-how-to-contribute)
5. [Contribution Standards](#5-contribution-standards)
6. [Opening an Issue](#6-opening-an-issue)
7. [Submitting a Pull Request](#7-submitting-a-pull-request)
8. [Research Contributions](#8-research-contributions)
9. [Discussion and Debate](#9-discussion-and-debate)
10. [Code of Conduct](#10-code-of-conduct)

---

## 1. Who Should Contribute

Sapien welcomes contributions from anyone who thinks seriously about
intelligence, learning, and AI architecture. You do not need a PhD.
You do not need industry experience. You need curiosity and honesty.

Specifically valuable backgrounds include:

- AI and machine learning researchers
- Cognitive scientists and developmental psychologists
- Neuroscientists and philosophers of mind
- Knowledge graph and graph database engineers
- Symbolic AI and neuro-symbolic systems researchers
- Distributed systems engineers
- Education theorists and learning scientists
- Anyone who has built and trained language models
  and noticed something was missing

If you have challenged these ideas and found them wanting — your
criticism is especially welcome. Sapien is strengthened more by honest
disagreement than by agreement.

---

## 2. Ways to Contribute

**Theoretical contributions**
Formal specifications, mathematical proofs, theoretical arguments for
or against components of the architecture. Papers, preprints, or
structured writeups.

**Architecture refinements**
Proposed changes, additions, or alternatives to the architecture
documented in ARCHITECTURE.md. Must include reasoning — not just
what to change but why.

**Limitation analysis**
Deeper investigation of the known limitations listed in LIMITATIONS.md.
New limitations identified. Proposed mitigations. Honest assessments
of what cannot be fixed.

**Implementation proposals**
Concrete proposals for how components of Sapien could be implemented.
Prototypes, proof-of-concept code, benchmarks.

**Documentation improvements**
Clarifications, corrections, better explanations. If something in the
documentation confused you, improving it helps everyone who comes next.

**Discussion and debate**
Opening issues to debate architectural decisions. Challenging assumptions.
Proposing alternatives. Even disagreeing with the entire premise.

---

## 3. What Sapien Needs Most

Current highest-priority research questions:

**Grounding and embodiment**
How can Sapien acquire grounded meaning without physical embodiment?
What role could simulated environments, multimodal perception, or
robotics integration play? This is the deepest open problem.
See LIMITATIONS.md §1 for detailed analysis.

**Formal didactic episode specification**
A mathematically rigorous definition of the didactic episode learning
loop. What are the formal termination conditions? How is epistemic
closure formally defined and measured?
See DIDACTIC_SPEC.md for the current proposal and its open problems.

**Knowledge graph scalability**
How does the DAG scale to billions of nodes? What pruning, compression,
and archival strategies preserve WHY chains while maintaining practical
retrieval latency?
See SCHEMA_SPEC.md §11 for current open problems in the schema.

**WHY chain depth termination**
How do you define an axiomatic floor — the set of foundational concepts
accepted without further justification? How is this floor selected and
validated?
See AXIOMATIC_FLOOR.md for the current proposal and its open problems.

**Curiosity reward formalization**
A formal specification of the productive utility gate that distinguishes
productive from pathological curiosity. How is semantic uniqueness
measured? How is productive utility quantified?
See REWARD_SPEC.md for the current specification and its open problems.

**Contradiction resolution**
How does Sapien represent and reason about genuinely unresolved
contradictions — contested science, philosophical disagreement,
uncertain empirical claims? Probabilistic epistemology approaches
are especially welcome.
See CONTRADICTION_FRAMEWORK.md for the current framework and
its open problems.

**Generational drift measurement**
How do you measure reasoning drift across generations? What metrics
indicate healthy evolution versus problematic divergence?
See LIMITATIONS.md §3 for detailed analysis.

---

## 4. How to Contribute

**Step 1 — Read first**
Before contributing, read:
- [README.md](README.md) — project overview
- [ARCHITECTURE.md](ARCHITECTURE.md) — complete technical specification
- [LIMITATIONS.md](LIMITATIONS.md) — known open problems
- [DIDACTIC_SPEC.md](DIDACTIC_SPEC.md) — formal episode specification
- [SCHEMA_SPEC.md](SCHEMA_SPEC.md) — knowledge graph schema
- [REWARD_SPEC.md](REWARD_SPEC.md) — reward signal specification
- [AXIOMATIC_FLOOR.md](AXIOMATIC_FLOOR.md) — axiomatic floor proposal
- [CONTRADICTION_FRAMEWORK.md](CONTRADICTION_FRAMEWORK.md) — contradiction framework
- Open issues — what is already being discussed

**Step 2 — Find your contribution**
Check open issues for areas needing work. Or identify something
not covered that you want to address.

**Step 3 — Open an issue before large contributions**
For significant architecture changes, new research directions, or
implementation proposals — open an issue first to discuss before
investing time in a full pull request.

**Step 4 — Fork and contribute**
Fork the repository, make your changes, and submit a pull request
with a clear description of what you changed and why.

---

## 5. Contribution Standards

**Honesty over agreement**
Do not contribute something you do not believe. If you think a part
of the architecture is flawed, say so clearly. Honest criticism is
more valuable than polite agreement.

**Reasoning required**
Every significant change or proposal must include reasoning. Not just
what you propose — why you propose it, what problem it solves, and
what tradeoffs it introduces.

**Acknowledge limitations**
If your proposed solution introduces new problems, state them. Sapien
already maintains an honest limitations document. Contributions should
maintain that standard of honesty.

**Attribution**
If your contribution builds on published research, cite the work.
If your contribution is an original idea, claim it. Credit matters.

**Language**
English only for now. Clear, precise, and direct. Academic formality
is not required. Clarity is.

---

## 6. Opening an Issue

Use issues for:
- Questions about the architecture
- Identified flaws or limitations not yet documented
- Proposals for architecture changes
- Discussion of open research problems
- Requests for clarification

**Issue title format:**
[TYPE] Brief description

Types:
- `[FLAW]` — identified architectural problem
- `[PROPOSAL]` — proposed change or addition
- `[QUESTION]` — request for clarification
- `[RESEARCH]` — relevant research to incorporate
- `[DISCUSSION]` — open-ended debate

**Example:**
[FLAW] WHY chain termination has no formal stopping criterion
[PROPOSAL] Probabilistic nodes for contradiction representation
[RESEARCH] Schmidhuber 1991 — formal theory of creativity and curiosity

---

## 7. Submitting a Pull Request

**Pull request checklist:**

- [ ] I have read ARCHITECTURE.md and LIMITATIONS.md
- [ ] My changes are consistent with the design philosophy
  in ARCHITECTURE.md Section 2
- [ ] I have included reasoning for every significant change
- [ ] I have updated LIMITATIONS.md if my change introduces
  new tradeoffs
- [ ] I have cited any external research I relied on
- [ ] My documentation changes are clear and accurate

**Pull request description format:**
What this changes
Clear description of what is being changed or added.
Why
Reasoning for the change. What problem does it solve?
What limitation does it address?
Tradeoffs introduced
Honest assessment of new problems this change creates.
References
Any research, papers, or prior work this builds on.

---

## 8. Research Contributions

Sapien is at the intersection of several active research fields.
Relevant published research is especially welcome.

If you are aware of work that directly addresses an open problem
in Sapien — grounding, curiosity formalization, generational learning,
contradiction resolution, WHY chain depth — please open a
`[RESEARCH]` issue with:

- Full citation
- Brief summary of relevance to Sapien
- Which open problem or architectural component it addresses
- Your assessment of how it could be incorporated

Research contributions do not require a pull request. An issue
is sufficient.

---

## 9. Discussion and Debate

Sapien's adversarial collaboration principle applies to its own
development. Disagreement is healthy. Debate improves the architecture.

The Forestritium Discord server has a dedicated channel for Sapien
discussion:

[Join Forestritium Discord](https://discord.gg/Q64wr956)

For longer-form discussion, open a `[DISCUSSION]` issue on GitHub.

---

## 10. Code of Conduct

Sapien follows a simple code of conduct:

**Be honest.** Say what you actually think. Honest disagreement
is more valuable than polite silence.

**Be specific.** Vague criticism helps nobody. If something is wrong,
explain precisely what and why.

**Be respectful.** Challenge ideas, not people. The architecture
can be wrong without the person who proposed it being wrong.

**Credit others.** If you build on someone else's idea, say so.

**Acknowledge uncertainty.** Nobody knows how to build human-like
intelligence. Contributions that claim certainty where none exists
are not helpful.

---

*Sapien — AGPLv3 — Contributions welcome*

*Author: Aarav* | **Forestritium**
