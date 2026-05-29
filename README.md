# Sapien

> Human civilization did not become intelligent through compression alone.
> It became intelligent through teaching.

[![Architecture Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/A-Solo-Engineer/Sapien)
[![License: AGPLv3](https://img.shields.io/badge/License-AGPLv3-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-conceptual-blue.svg)](https://github.com/A-Solo-Engineer/Sapien)
[![Author](https://img.shields.io/badge/author-Aarav-orange.svg)](https://dev.to/admin-forestritium)

A didactic, generational framework for neuro-symbolic cognitive AI. Sapien shifts the paradigm from machine *training* to machine *teaching* — decoupling statistical pattern recognition from long-term structured memory.

---

## What is Sapien?

Modern AI systems are extraordinary at recognizing patterns. But after building and training smaller language models, a fundamental observation emerged:

**The models were not learning. They were optimizing.**

A child can connect "fire is hot" and "hot things hurt" to conclude "I should not touch fire" — without ever being explicitly trained on that sentence. Most current AI systems struggle to do this reliably unless similar patterns already existed in their training data.

Sapien is an attempt to rethink what learning itself means for artificial intelligence.

---

## Core Idea

| Current AI | Sapien |
|---|---|
| Static dataset training | Live didactic episodes |
| Loss minimization | Curiosity-driven questioning |
| Opaque neural weights | Inspectable knowledge graph |
| Single training run | Generational knowledge inheritance |
| No causal reasoning | WHY chain preservation |
| No intrinsic motivation | Reward-scaled curiosity |

---

## Architecture Overview

Sapien is organized into seven layers:
Layer 1 — Grounded Learning Substrate
Layer 2 — Didactic Learning Engine (Generation 0)
Layer 3 — 1st Generation Learner (Adversarial Collaboration)
Layer 4 — Causal Knowledge Representation (DAG)
Layer 5 — Continual Generational Learning
Layer 6 — Human-in-the-Loop Oversight (Permanent)
Layer 7 — Multi-Generational Error Correction

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete technical specification.

---

## Key Components

**Didactic Episodes**
Learning occurs through structured teaching sessions. A teacher AI presents topics in chunks. The learner identifies gaps, asks curiosity-driven questions, and stores both the answer and the reasoning behind it. An episode ends when the learner reaches epistemic closure — no meaningful unresolved gaps remain.

**Knowledge Gap Map**
Three-tier epistemic tracking:
- Known Knowns — fully understood concepts with WHY chains
- Known Unknowns — identified gaps driving questions
- Unknown Unknowns — new territory exposed by teaching, become SEED nodes

**Knowledge Graph (DAG)**
Every concept stored as a node in a directed acyclic graph with:
- Declarative knowledge — WHAT
- Causal reasoning chain — WHY
- Epistemic provenance — SOURCE
- Connection strengths
- Uncertainty estimates

**SEED Nodes**
When the learner encounters something it cannot connect to existing knowledge, it creates a new isolated conceptual branch. As more information arrives, the branch grows and integrates. SEED node creation receives maximum reward signal — it represents genuine discovery.

**Adversarial Collaboration**
Two learner instances trained by different teacher models develop different reasoning perspectives and debate each other. A verifier model monitors hallucinations. Human supervisors remain the permanent final authority.

**Generational Handoff**
Generation 1 teaches Generation 2 through the same didactic process it experienced — not by copying the DAG, but by reconstructing understanding through guided teaching. WHY chains and reasoning provenance are preserved across every generation.

---

## Known Limitations

Sapien is a conceptual architecture. Many fundamental problems remain open:

| Severity | Problem |
|---|---|
| Critical | Symbol grounding — meaning without embodiment |
| Critical | Hallucinated reasoning chains |
| Critical | Generational drift |
| Critical | Knowledge graph explosion at scale |
| High | Curiosity reward hacking |
| High | Contradiction resolution |
| High | Human oversight scalability |
| High | WHY chain infinite recursion |
| Medium | Emotional cognition absence |
| Medium | Computational expense |
| Philosophical | Identity continuity across generations |
| Philosophical | Consciousness ambiguity |

See [LIMITATIONS.md](LIMITATIONS.md) for detailed analysis of each problem.

---

## Project Status

Sapien has completed Phase 1 of its development roadmap —
documentation and theoretical specification — and is ready to
advance to Phase 2: prototype implementation.

Phase 1 produced a complete theoretical foundation:
- Core architecture specification
- Known limitations analysis
- Formal mathematical specification of the didactic episode
- Formal knowledge graph schema
- Reward signal formal definition
- Axiomatic floor proposal
- Contradiction resolution framework

There is no implementation yet. Phase 2 begins with a documented
specification complete enough for an independent prototype.

See [ROADMAP.md](ROADMAP.md) for the full development plan.

---

## Getting Started

There is no code to run yet. The best starting points are:

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for the complete technical specification
2. Read the introductory article: [Sapien on dev.to](https://dev.to/admin-forestritium/sapien-teaching-ai-to-think-like-humans-instead-of-predicting-patterns-5nd)
3. Read [LIMITATIONS.md](LIMITATIONS.md) for honest assessment of open problems
4. Read [DIDACTIC_SPEC.md](DIDACTIC_SPEC.md) for the formal learning loop specification
5. Read [SCHEMA_SPEC.md](SCHEMA_SPEC.md) for the knowledge graph schema
6. Read [REWARD_SPEC.md](REWARD_SPEC.md) for the curiosity reward system
7. Read [AXIOMATIC_FLOOR.md](AXIOMATIC_FLOOR.md) for the WHY chain termination proposal
8. Read [CONTRADICTION_FRAMEWORK.md](CONTRADICTION_FRAMEWORK.md) for contradiction handling
9. Join the discussion in [Forestritium Discord](https://discord.gg/ezc9Y7eeQt)

---

## Contributing

Sapien needs researchers, thinkers, and builders. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

Areas where contribution is most needed:
- Theoretical refinement of the knowledge graph design
- Formal mathematical specification of the didactic episode
- Approaches to the grounding problem
- Contradiction resolution and probabilistic epistemology
- Computational efficiency proposals

---

## Author

**Aarav** | Forestritium

Date of Idea: 28 May 2026.

---

## License

AGPLv3 — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

Sapien emerged from a conversation about why a small language model trained in LLM Developer never truly learned anything. It only optimized. That observation led me here.

Related researchers whose work intersects with Sapien's ideas:
- Jürgen Schmidhuber — intrinsic motivation and curiosity
- Karl Friston — active inference
- Yann LeCun — world models and joint embedding architectures
- Gary Marcus — neurosymbolic AI
- Judea Pearl — causal reasoning
