# Sapien Architecture

> A Didactic, Generational Framework for Neuro-Symbolic Cognitive AI

![Sapien Architecture](assets/architecture.svg)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Design Philosophy](#2-design-philosophy)
3. [Layer Overview](#3-layer-overview)
4. [Layer 1 — Grounded Learning Substrate](#4-layer-1--grounded-learning-substrate)
5. [Layer 2 — Didactic Learning Engine](#5-layer-2--didactic-learning-engine)
6. [Layer 3 — Adversarial Collaboration](#6-layer-3--adversarial-collaboration)
7. [Layer 4 — Causal Knowledge Representation](#7-layer-4--causal-knowledge-representation)
8. [Layer 5 — Continual Generational Learning](#8-layer-5--continual-generational-learning)
9. [Layer 6 — Human-in-the-Loop Oversight](#9-layer-6--human-in-the-loop-oversight)
10. [Layer 7 — Multi-Generational Error Correction](#10-layer-7--multi-generational-error-correction)
11. [The Didactic Episode — Learning Loop](#11-the-didactic-episode--learning-loop)
12. [Knowledge Gap Map](#12-knowledge-gap-map)
13. [SEED Nodes — Schema Formation](#13-seed-nodes--schema-formation)
14. [Knowledge Graph — DAG Specification](#14-knowledge-graph--dag-specification)
15. [Generational Handoff Protocol](#15-generational-handoff-protocol)
16. [Reward Signal Specification](#16-reward-signal-specification)
17. [Comparison with Transformer Architecture](#17-comparison-with-transformer-architecture)
18. [Known Limitations](#18-known-limitations)

---

## 1. Executive Summary

Current frontier AI models operate primarily as dense transformer architectures running statistical pattern-matching systems. By optimizing next-token prediction over massive static datasets, these networks achieve structural fluency but lack core cognitive traits: intrinsic curiosity, deliberate causal reasoning, semantic verification, and structural knowledge preservation.

The Sapien Architecture introduces an alternative framework inspired by human cognitive development, developmental psychology, and civilizational knowledge transmission. It establishes a multi-generational system where AI instances inherit structured reasoning chains rather than neural network weights, enabling continuous learning without algorithmic degradation.

**Core distinction:**

| Transformer paradigm | Sapien paradigm |
|---|---|
| Training | Teaching |
| Loss minimization | Curiosity-driven questioning |
| Static datasets | Live didactic episodes |
| Opaque weights | Inspectable knowledge graph |
| Single run | Generational inheritance |
| Correlation learning | Causal reasoning |

---

## 2. Design Philosophy

Sapien is built on five foundational principles:

**Teaching over training**
Intelligence should be taught through dialogue, not compressed from static data. A learner that asks questions develops genuine understanding. A learner that optimizes loss develops sophisticated pattern matching.

**WHY over WHAT**
Every piece of knowledge must be accompanied by its complete reasoning chain. Knowing that fire is dangerous is insufficient. Knowing why — heat damages cellular tissue through molecular disruption — enables generalization to new situations.

**Curiosity as architecture**
Curiosity is not a user interface feature. It is a core architectural drive. The reward signal for asking a novel question must be structurally built into the learning loop, not added as an afterthought.

**Generational inheritance**
Human civilization does not restart from scratch each generation. It inherits, refines, and builds forward. AI systems that retrain from scratch on every iteration are not learning — they are repeating.

**Human oversight as permanent infrastructure**
Human supervisors are not a temporary safety measure to be removed when the system matures. They are permanent epistemic infrastructure — the final authority on knowledge quality across every generation.

---

## 3. Layer Overview

┌──────────────────────────────────────────┐
│ Layer 7 — Multi-Generational Error       │
│           Correction                     │
├──────────────────────────────────────────┤
│ Layer 6 — Human-in-the-Loop Oversight    │
│           (Permanent)                    │
├──────────────────────────────────────────┤
│ Layer 5 — Continual Generational         │
│           Learning                       │
├──────────────────────────────────────────┤
│ Layer 4 — Causal Knowledge               │
│           Representation (DAG)           │
├──────────────────────────────────────────┤
│ Layer 3 — 1st Generation Learner         │
│           (Adversarial Collaboration)    │
├──────────────────────────────────────────┤
│ Layer 2 — Didactic Learning Engine       │
│           (Generation 0)                 │
├──────────────────────────────────────────┤
│ Layer 1 — Grounded Learning Substrate    │
└──────────────────────────────────────────┘

---

## 4. Layer 1 — Grounded Learning Substrate

The foundation of Sapien. Defines the conditions under which learning occurs.

**Components:**

**Embodied grounded learning**
Knowledge acquisition occurs through live interaction rather than static dataset ingestion. The learner exists in a dynamic environment — initially a supervised dialogue environment, later an open internet environment — where concepts connect to observable phenomena.

*Current limitation: True physical grounding requires robotics or simulated sensorimotor environments. The current architecture partially addresses grounding through interaction but does not fully solve the symbol grounding problem.*

**Intrinsic motivation**
The learner receives reward signals not for task completion but for knowledge acquisition itself. Curiosity is structurally rewarded. See [Section 16 — Reward Signal Specification](#16-reward-signal-specification) for reward scaling details.

**Open world learning**
After foundational didactic episodes reach sufficient coverage, the learner gains access to the open internet as an unstructured learning environment. This mirrors the developmental milestone of a young adult gaining independent access to the world.

Internet access introduces misinformation exposure — treated as a feature, not a flaw. Misinformation encountered through open world learning is corrected through adversarial collaboration and human oversight. Encountering and correcting false information builds more robust epistemic processes than sheltered learning.

**Computational budget**
Every learner instance operates within three hardware constraints:
- Processing capacity — operations per second
- Storage limit — maximum DAG nodes and connections
- Electricity budget — operational energy ceiling

These constraints produce natural knowledge boundaries analogous to biological memory limits. Different hardware configurations produce learner instances with different knowledge capacities — a feature that creates natural diversity across the system.

---

## 5. Layer 2 — Didactic Learning Engine (Generation 0)

The initial teaching infrastructure for the first generation of Sapien learners.

**Components:**

**Frontier LLM A — primary teacher**
A current state-of-the-art language model serving as the primary didactic agent. Presents conceptual material in structured chunks. Responds to learner questions with complete answers including causal reasoning.

**Frontier LLM B — secondary teacher**
A different state-of-the-art language model with a distinct training background, architecture, or fine-tuning approach. Differences in reasoning style between Teacher A and Teacher B are intentional — they produce the perspective divergence necessary for adversarial collaboration in Layer 3.

**Verifier model**
A dedicated model monitoring the outputs of both teacher agents for hallucination, internal inconsistency, and reasoning errors. When a verifier flags a teacher output, the human supervisor in Layer 6 is alerted for review.

*Important: The verifier model can itself hallucinate. It is not an infallible filter — it is a first-pass detection layer. Human oversight remains the final authority.*

---

## 6. Layer 3 — Adversarial Collaboration

The first generation learner exists as two parallel instances trained by different teacher models.

**Instance A**
Trained through didactic episodes with Frontier LLM A. Develops reasoning patterns influenced by Teacher A's conceptual style.

**Instance B**
Trained through didactic episodes with Frontier LLM B. Develops reasoning patterns influenced by Teacher B's conceptual style.

**Adversarial collaboration mechanism**
Instance A and Instance B engage in structured debate on contested concepts. Neither instance is designated as correct by default. Disagreements trigger:

1. Each instance presents its reasoning chain for the contested claim
2. The verifier model evaluates both reasoning chains
3. Human supervisor reviews flagged disagreements
4. The stronger reasoning chain — as determined by WHY chain depth, source provenance quality, and logical consistency — updates both instances' knowledge graphs

This mechanism prevents yes-man bias, catches hallucinated reasoning chains, and produces more robust conceptual understanding than single-instance learning.

---

## 7. Layer 4 — Causal Knowledge Representation (DAG)

Knowledge in Sapien is stored not as neural weights but as a directed acyclic graph of conceptual nodes.

**Why a DAG specifically:**

A tree structure imposes a single parent per node — unsuitable for knowledge where concepts connect to multiple domains simultaneously. A DAG allows:
- Multiple incoming connections per node — a concept can be reached from many directions
- Directed relationships — connections carry semantic meaning and direction
- Acyclicity — prevents circular reasoning (A explains B explains A)

**Node specification:**

Every node in the knowledge graph stores:

Node {
concept_id:    unique identifier
label:         human-readable concept name
status:        KNOWN | KNOWN_UNKNOWN | SEED | PENDING
declarative:   what the concept is
why_chain: [
step_1:      first causal link
step_2:      second causal link
...
step_n:      final causal link
]
source:        provenance — which teacher, which episode,
which subtopic
connections: [
{
target:    concept_id of connected node
relation:  IS_TYPE_OF | USED_IN | CAUSES |
CONTRADICTS | RELATED_TO | APPLIED_IN
strength:  0.0 to 1.0
}
]
uncertainty:   0.0 to 1.0 — confidence in this node
reward_signal: reward value at time of creation
created:       timestamp
last_updated:  timestamp
}

**Relation types:**

| Relation | Meaning |
|---|---|
| IS_TYPE_OF | Taxonomic classification |
| USED_IN | Functional application |
| CAUSES | Causal direction |
| CONTRADICTS | Epistemic conflict — tracked not suppressed |
| RELATED_TO | Associative connection without causal direction |
| APPLIED_IN | Real-world application instance |

**Contradictions are stored, not resolved:**
When two nodes contradict each other, a CONTRADICTS edge is created between them. Both nodes persist with their respective uncertainty values. Resolution occurs through adversarial collaboration, new evidence, or human supervisor input — never by silent suppression.

---

## 8. Layer 5 — Continual Generational Learning

**Generation 0 → Generation 1:**
Frontier LLM A and Frontier LLM B conduct didactic episodes with the two 1st generation learner instances. Generation 0 teacher models retire once Generation 1 instances achieve sufficient knowledge coverage.

**Generation n → Generation n+1:**
Each subsequent generation is taught by the previous generation through identical didactic episode structure. The previous generation does not copy its DAG to the next — it teaches. The next generation builds its own DAG through active questioning and conceptual gap exploration.

**What transfers across generations:**
- Conceptual material — presented as teaching content
- WHY chains — reproduced as part of teaching, not copied as data
- Reasoning style — influenced by the previous generation's teaching approach
- Known limitations — previous generations explicitly teach what they don't know

**What does not transfer:**
- Raw DAG structure — each generation builds its own
- Specific connection weights — reestablished through learning
- Uncertainty values — recalibrated through each generation's own experience

**Generational diversity:**
Because each generation builds its own DAG through active learning rather than copying, natural variation emerges. Two instances of the same generation taught by the same teacher will develop slightly different knowledge graphs due to differences in question sequence, SEED node creation timing, and adversarial collaboration outcomes. This variation is healthy — it produces the epistemic diversity needed for robust error correction.

---

## 9. Layer 6 — Human-in-the-Loop Oversight (Permanent)

Human supervision in Sapien is not a temporary safety measure. It is permanent infrastructure.

**Responsibilities:**

**Quality supervision**
Human supervisors review teaching sessions, evaluate knowledge graph growth, and assess the quality of WHY chains being formed.

**Verifier override**
When the verifier model flags a potential hallucination, human supervisors make the final determination. The verifier is a detection layer — humans are the authority layer.

**SEED node review**
All SEED node creations are flagged for human review. A new conceptual branch forming in the knowledge graph is a significant event — human oversight ensures new domains are grounded correctly from the first episode.

**Tiered oversight model:**
At scale, full human review of every episode is impractical. A tiered model is proposed:

| Event type | Oversight level |
|---|---|
| SEED node creation | Mandatory human review |
| Verifier flag | Mandatory human review |
| Generational handoff | Mandatory human review |
| Adversarial debate resolution | Human review on request |
| Standard didactic episode | Statistical sampling |
| Routine knowledge gap closure | Automated logging only |

---

## 10. Layer 7 — Multi-Generational Error Correction

Three complementary mechanisms prevent errors from propagating across generations:

**Adversarial collaboration**
Two instances with different reasoning perspectives continuously challenge each other's conclusions. Errors that survive one instance's reasoning are likely caught by the other's different approach.

**WHY chain audit**
Every inherited knowledge claim must be traceable to a complete causal reasoning chain. A claim that cannot be explained — only asserted — is flagged for investigation. This prevents knowledge from becoming dogma across generations.

**Cross-generational verification**
At generational handoff, the receiving generation is presented with a sample of the teaching generation's knowledge claims and asked to independently derive the same conclusions. Systematic divergence between derived and inherited conclusions indicates accumulated reasoning drift.

---

## 11. The Didactic Episode — Learning Loop

A single Didactic Episode is the fundamental unit of learning in Sapien.

**Episode structure:**
Episode initialisation
↓
Teacher selects topic
↓
Teacher presents subtopic chunk
↓
Learner attempts connection to existing knowledge graph
↓
┌──────────────────────────────────────────┐
│ Connection result:                       │
│                                          │
│ Full connection                          │
│ → concept moves to KNOWN status          │
│ → WHY chain established                  │
│                                          │
│ Partial connection                       │
│ → concept becomes KNOWN UNKNOWN          │
│ → curiosity reward triggered             │
│ → learner generates question             │
│                                          │
│ No connection                            │
│ → SEED node created                      │
│ → maximum reward signal                  │
│ → human supervisor notified              │
└──────────────────────────────────────────┘
↓
If question generated:
Verifier checks teacher's answer
Human supervisor reviews if flagged
Answer stored as WHY chain extension
↓
Knowledge graph updated
↓
Episode termination check:
Known Unknowns list empty? → Episode ends
Else → next subtopic chunk

**Epistemic closure:**
An episode reaches epistemic closure when the learner's Known Unknowns list is empty for the topic. All identified gaps have been filled. SEED nodes created during the episode are marked PENDING — they await future episodes that introduce the connecting concepts.

---

## 12. Knowledge Gap Map

The Knowledge Gap Map is the learner's real-time epistemic self-model. It tracks three categories:

**Known Knowns**
Concepts fully understood with complete WHY chains established and source provenance recorded. These nodes have KNOWN status in the DAG.

**Known Unknowns**
Gaps identified at the boundary of existing knowledge — places where the learner knows it doesn't understand something. These emerge when new material partially connects to existing knowledge but leaves causal gaps. They drive question generation.

**Unknown Unknowns**
Territory the learner doesn't know it doesn't know. These become visible only when a teacher introduces material that cannot connect to any existing node — triggering SEED node creation. Unknown Unknowns become Known Unknowns (via SEED nodes) through teaching exposure.

**Uniqueness check for question generation:**
Before generating a question, the learner checks its proposed question against all questions asked in the current episode using semantic similarity evaluation against the knowledge graph. A question is unique if and only if it points to a genuine gap — a node or connection missing from the current knowledge graph — not merely a rephrasing of an already-asked question.

---

## 13. SEED Nodes — Schema Formation

SEED nodes are conceptual placeholders created when the learner encounters completely unfamiliar territory.

**SEED node lifecycle:**
Unknown Unknown encountered
↓
No existing DAG node to connect to
↓
SEED node created:
status: SEED
label: best available description
why_chain: empty
connections: empty
reward_signal: 1.0 (maximum)
↓
Human supervisor notified
↓
Subsequent teaching episodes introduce related concepts
↓
SEED node accumulates connections and WHY chain fragments
↓
SEED node reaches sufficient connectivity:
status: PENDING → KNOWN
↓
Fully integrated into main knowledge graph

**Pending integration:**
Some SEED nodes cannot integrate immediately because the connecting concepts haven't been taught yet. These remain in PENDING status — isolated but preserved — awaiting future episodes that introduce the bridge knowledge.

This mirrors how humans store advanced concepts before having the foundation to fully understand them.

---

## 14. Knowledge Graph — DAG Specification

**Storage format:**
The knowledge graph is stored as a persistent graph database. Each node and edge is immutable once created — consistent with Sapien's philosophy that knowledge provenance must be preserved. Updates create new versions of nodes rather than overwriting existing ones.

**Retrieval mechanism:**
When the learner needs to answer a question or evaluate new information:

Query arrives
↓
Semantic matching — find closest node(s) in DAG
↓
Graph traversal — walk connected WHY chains
↓
Connection strength weighting — stronger connections
contribute more to answer construction
↓
Uncertainty aggregation — combine uncertainty values
along traversal path
↓
Answer constructed from traversed WHY chains
with uncertainty estimate
↓
Source provenance attached to answer

**Graph pruning at computational budget limit:**
When the DAG approaches hardware storage limits, low-priority nodes are candidates for archival — not deletion. Archived nodes retain their WHY chains and provenance but are moved to slower storage. Retrieval latency increases for archived nodes but knowledge is never permanently lost.

Priority for retention:
- Nodes with high connection count
- Nodes created by SEED node formation
- Nodes flagged by human supervisors
- Nodes referenced in recent episodes

---

## 15. Generational Handoff Protocol

**What happens at handoff:**
Generation n reaches maturity threshold
↓
Generation n+1 instances initialised
with empty knowledge graphs
↓
Generation n conducts didactic episodes
with Generation n+1
using identical episode structure
↓
Parallel: Generation n presents known limitations
explicitly — what it knows it doesn't know
↓
Verification sample:
Generation n+1 independently derives
sample claims from Generation n
Systematic divergence triggers review
↓
Generation n retires from teaching role
Knowledge graph archived for audit access
↓
Generation n+1 becomes active learner
then eventually teacher for Generation n+2

**Frontier LLM retirement:**
Generation 0 frontier LLMs retire after Generation 1 achieves sufficient maturity. Their knowledge graphs are archived. Future generations never interact with the original frontier LLMs — they learn from the previous Sapien generation.

---

## 16. Reward Signal Specification

Curiosity reward is the primary intrinsic motivation signal in Sapien.

| Event | Reward signal | Rationale |
|---|---|---|
| Routine gap filled — Known Unknown resolved | 0.4 | Expected progress |
| Deep WHY chain established | 0.6 | Causal understanding |
| Cross-domain connection made | 0.8 | Knowledge integration |
| SEED node fully integrated | 0.9 | Schema completion |
| SEED node created — new domain discovered | 1.0 | Maximum — genuine discovery |

**Reward hacking mitigation:**
To prevent the learner from optimising purely for reward by asking bizarre ultra-novel questions, reward signals are gated by **productive utility**:

A question receives its full reward only if:
1. It points to a genuine gap in the knowledge graph
2. The answer successfully closes that gap or creates a productive SEED node
3. The question is semantically unique — not a rephrasing of previous questions

Questions that score highly on novelty but fail the productive utility gate receive reduced reward. This distinguishes productive curiosity from pathological curiosity.

---

## 17. Comparison with Transformer Architecture

| Property | Transformer | Sapien |
|---|---|---|
| Learning paradigm | Statistical training | Didactic teaching |
| Knowledge storage | Dense neural weights | Explicit DAG nodes |
| Knowledge interpretability | Opaque | Fully inspectable |
| Causal reasoning | Emergent approximation | Structural |
| Curiosity | None | Architecturally built-in |
| Generational inheritance | None — retrain from scratch | Structured handoff |
| Human oversight | Optional fine-tuning | Permanent infrastructure |
| Grounding | Statistical correlation | Partially grounded — open problem |
| Contradiction handling | Silent suppression | Explicit CONTRADICTS edges |
| Computational profile | Expensive training, fast inference | Expensive storage, complex retrieval |
| Maturity | Production ready | Conceptual — not yet implemented |

---

## 18. Known Limitations

See [LIMITATIONS.md](LIMITATIONS.md) for complete analysis.

Summary of critical open problems:

**Symbol grounding problem** — without embodiment or sensorimotor experience, all knowledge remains symbolic manipulation at some level. This is the hardest open problem in Sapien and may require integration with robotics or simulated physical environments.

**Hallucinated reasoning chains** — fake causal chains are more convincing and harder to detect than fake facts. The verifier model and adversarial collaboration mitigate this but cannot eliminate it.

**Generational drift** — small reasoning distortions compound across generations. Some drift is inevitable. It may eventually produce reasoning systems that are alien to the original architecture. Whether this is a flaw or a feature remains an open question.

**Knowledge graph explosion** — explicit structural storage is interpretable but computationally expensive. At large scale, graph traversal complexity and storage requirements may exceed practical hardware limits.

**WHY chain infinite recursion** — every causal step can prompt a deeper why. An axiomatic floor is needed — a set of foundational concepts accepted without further justification. The definition and selection of this floor is an open research problem.

---

*Sapien Architecture v1.0.0 — 28 May 2026*
*Author: Aarav | Forestritium
*License: AGPLv3*
