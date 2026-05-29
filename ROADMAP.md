# Roadmap

Sapien is a long-term research direction. This roadmap reflects
honest current thinking about how the project develops — not
a commitment to specific timelines.

---

## Phase 1 — Documentation ✓ Complete

**Goal:** Establish a complete, honest, and rigorous theoretical
foundation before any implementation begins.

**Tasks:**
- [x] Core architecture specification (ARCHITECTURE.md)
- [x] Known limitations analysis (LIMITATIONS.md)
- [x] Contributing guidelines (CONTRIBUTING.md)
- [x] Architecture diagram (assets/architecture.svg)
- [x] Introductory article published
- [x] Formal mathematical specification of the didactic episode (DIDACTIC_SPEC.md)
- [x] Formal DAG schema specification (SCHEMA_SPEC.md)
- [x] Reward signal formal definition (REWARD_SPEC.md)
- [x] Axiomatic floor initial proposal (AXIOMATIC_FLOOR.md)
- [x] Contradiction resolution framework proposal (CONTRADICTION_FRAMEWORK.md)

**Phase 1 completion criteria:**
The architecture is specified completely enough that an
independent researcher could begin a prototype implementation
using only this documentation.

**Phase 1 status: COMPLETE — 28 May 2026**

---

> Phase 1 produced nine documentation files totalling the full
> theoretical specification of Sapien. Phase 2 begins with a
> working foundation rather than open questions.


## Phase 2 — Prototype (Next)

**Goal:** A minimal working proof of concept demonstrating
the core didactic episode loop and knowledge graph.

**Scope — minimum viable prototype:**
- Single learner instance (no adversarial collaboration yet)
- Single teacher model (existing frontier LLM via API)
- Basic DAG implementation (knowledge graph storage)
- Didactic episode loop (question generation and gap tracking)
- SEED node creation
- Basic WHY chain storage

**Reference documents for Phase 2 implementation:**
- DIDACTIC_SPEC.md — episode state machine and termination logic
- SCHEMA_SPEC.md — node and edge schema (Section 9 recommends
  relational database for prototype storage)
- REWARD_SPEC.md — productive utility gate and curiosity reward
- AXIOMATIC_FLOOR.md — floor node initialization

**Explicitly out of scope for Phase 2:**
- Generational handoff
- Adversarial collaboration
- Verifier model
- Open world learning
- Full reward signal implementation

**Phase 2 completion criteria:**
A single learner instance can conduct a supervised didactic
episode on a defined topic, ask curiosity-driven questions,
store WHY chains, and demonstrate epistemic closure when gaps
are filled.

---

## Phase 3 — Evaluation Framework

**Goal:** Define and implement metrics for measuring whether
Sapien is actually working as intended.

**Key metrics to develop:**
- Epistemic closure measurement — how do we verify genuine
  understanding vs pattern matching?
- Curiosity quality score — productive vs pathological curiosity
- WHY chain depth and validity assessment
- Cross-episode knowledge retention measurement
- Generational drift detection metrics

**Phase 3 completion criteria:**
A reproducible evaluation suite that can objectively compare
Sapien learning outcomes against baseline transformer inference
on defined reasoning tasks.

---

## Phase 4 — Adversarial Collaboration

**Goal:** Implement dual-instance learning with adversarial
debate and verifier model integration.

**Tasks:**
- Two parallel learner instances
- Structured debate protocol
- Verifier model integration
- Human oversight interface
- Contradiction resolution mechanism

---

## Phase 5 — Generational Handoff

**Goal:** Implement the first complete generational cycle.
Generation 0 teaches Generation 1 through full didactic episodes.

**Tasks:**
- Generational handoff protocol implementation
- Knowledge graph archival system
- Cross-generational verification suite
- Drift detection and alerting

---

## Phase 6 — Open World Learning

**Goal:** Enable supervised internet access for learning
beyond structured teaching.

**Tasks:**
- Controlled internet access environment
- Misinformation detection pipeline
- SEED node creation from open world exploration
- Human oversight for open world learning sessions

---

## Phase 7 — Community Research Collaboration

**Goal:** Open Sapien to collaborative research investigation
of remaining open problems.

**Focus areas:**
- Grounding and embodiment experiments
- Contradiction resolution approaches
- Scalability engineering
- Formal theoretical analysis

---

## Long-Term Vision

Sapien is not attempting to build AGI on a schedule.
It is attempting to establish whether teaching-based cognitive
architecture is a viable alternative to training-based architecture.

The honest answer to that question may take years to emerge.
The goal is to ask it rigorously and document the findings
honestly — regardless of whether the answer is yes or no.

---

## What Will Not Change

Regardless of where the roadmap goes:

- Sapien will remain open source under AGPLv3
- Known limitations will always be documented honestly
- Human oversight will remain permanent infrastructure
- WHY chain preservation will remain a core requirement
- The architecture will never claim to solve what it has not solved

---

*Roadmap last updated: 29 May 2026 — Phase 1 marked complete*
*Sapien — AGPLv3*
*Author: Aarav — A Solo Engineer*
