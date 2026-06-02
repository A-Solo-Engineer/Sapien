# Sapien Phase 2 — Minimal Didactic Episode Prototype

## Overview

This is the MVP (Minimum Viable Prototype) implementation of the Sapien didactic episode system. It demonstrates the core loop of supervised learning with knowledge graph construction.

## Phase 2 Scope

**In scope:**
- ✓ Single learner instance (no adversarial collaboration)
- ✓ Single teacher model (mock LLM via API stub)
- ✓ Basic DAG implementation (knowledge graph storage)
- ✓ Didactic episode loop (question generation and gap tracking)
- ✓ SEED node creation and management
- ✓ Basic WHY chain storage and validation
- ✓ Epistemic closure detection (KU = ∅)
- ✓ Axiomatic floor initialization

**Out of scope (Phase 2+):**
- ✗ Generational handoff
- ✗ Adversarial collaboration
- ✗ Verifier model (not implemented, human review flagging only)
- ✗ Open world learning
- ✗ Full reward signal implementation (basic structure only)

## Project Structure

```
Phase 2/
├── venv/                          # Virtual environment
├── src/
│   ├── graph/
│   │   ├── schema.py              # Node, Edge, and status schemas
│   │   └── dag.py                 # DAG implementation (SQLite)
│   ├── episode/
│   │   ├── state.py               # Epistemic state management (KK, KU, S, P)
│   │   └── episode_loop.py        # Main didactic episode loop
│   ├── agents/
│   │   ├── teacher.py             # Teacher interface and MockTeacher
│   │   └── learner.py             # Learner agent implementation
│   └── core/
│       ├── seed.py                # SEED node creation & floor initialization
│       └── why_chain.py           # WHY chain construction and validation
├── main.py                        # Entry point for MVP demo
├── requirements.txt
├── knowledge_graph.db             # SQLite database (created on first run)
└── README.md                      # This file
```

## Key Components

### 1. Knowledge Graph (DAG)

**File:** `src/graph/dag.py`

SQLite-backed implementation of the knowledge graph as a DAG. Stores:
- **Nodes:** represent concepts with schemas from SCHEMA_SPEC.md
  - Status: KNOWN, KNOWN_UNKNOWN, SEED, PENDING
  - WHY chain: ordered causal steps with certainty values
  - Provenance: where knowledge came from
  - Uncertainty: confidence level (0.0-1.0)

- **Edges:** represent relations between nodes
  - Types: IS_TYPE_OF, USED_IN, CAUSES, CONTRADICTS, RELATED_TO, APPLIED_IN
  - Strength: confidence in the relation (0.0-1.0)
  - Established_in: which episode created this edge

### 2. Epistemic State Management

**File:** `src/episode/state.py`

Tracks the four epistemic states (from DIDACTIC_SPEC.md §4):
- **KK (Known Knowns):** Concepts with complete WHY chains (status = KNOWN)
- **KU (Known Unknowns):** Identified gaps with questions pending (status = KNOWN_UNKNOWN)
- **S (SEED nodes):** Isolated new domains with no connections (status = SEED)
- **P (PENDING):** SEED nodes with partial connections (status = PENDING)

Epistemic closure is reached when **KU = ∅** (no more gaps to address).

### 3. Didactic Episode Loop

**File:** `src/episode/episode_loop.py`

Main orchestration logic (from DIDACTIC_SPEC.md §6):

```
while KU(t) ≠ ∅ or chunks remain:
  1. Receive chunk from teacher → process or create SEED node
  2. Generate question from gap in KU
  3. Get answer from teacher (with WHY chain)
  4. Integrate answer into graph
  5. Transition nodes: KNOWN_UNKNOWN → KNOWN or SEED → PENDING → KNOWN
  6. Check if KU is now empty (closure)
```

### 4. SEED Nodes and Axiomatic Floor

**File:** `src/core/seed.py`

Implements SEED node creation (from AXIOMATIC_FLOOR.md):
- SEED nodes represent isolated new domains
- They have empty WHY chains initially
- They transition to PENDING when connections are found
- They transition to KNOWN when fully integrated

Axiomatic floor nodes (from AXIOMATIC_FLOOR.md §5):
- Terminate WHY chains at principled stopping points
- Have empty why_chain, status = KNOWN, is_floor_node = true
- Category A (MVP): causality, logic, set membership, empirical observation

### 5. WHY Chain Logic

**File:** `src/core/why_chain.py`

WHY chains (from SCHEMA_SPEC.md §3):
- Ordered sequences of causal steps
- Each step has: claim, source, certainty (0.0-1.0)
- Chain depth ≥ 3 considered "deep" (from REWARD_SPEC.md)
- Aggregate certainty = minimum of chain steps

### 6. Teacher and Learner Agents

**Files:** `src/agents/teacher.py`, `src/agents/learner.py`

**Teacher** (from DIDACTIC_SPEC.md §3):
- Partitions topics into bounded chunks
- Answers questions with WHY chains
- Interface: `TeacherInterface`
- MVP uses `MockTeacher` for testing

**Learner** (from DIDACTIC_SPEC.md §3):
- Maintains knowledge graph
- Evaluates chunk connectivity
- Generates questions from gaps
- Integrates answers into graph
- Transitions node statuses

## Running the MVP Demo

### Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a local .env file:**
   ```bash
   copy .env.example .env
   ```
   Then replace the placeholder values with your actual API keys.

### Run Demo

```bash
python main.py
```

### Example Output

```
======================================================================
SAPIEN PHASE 2 - MINIMAL DIDACTIC EPISODE PROTOTYPE
======================================================================

This MVP demonstrates:
  ✓ Single learner instance
  ✓ Single teacher model (mock for this demo)
  ✓ Basic DAG implementation (SQLite)
  ✓ Didactic episode loop
  ✓ SEED node creation
  ✓ WHY chain storage & validation
  ✓ Epistemic closure detection

======================================================================

Initialized DAG at: knowledge_graph.db
Initialized MockTeacher

=== STARTING DIDACTIC EPISODE ===
Topic: photosynthesis
Max iterations: 5
Max questions: 3

=== MAIN EPISODE LOOP ===

--- Iteration 1 ---
Question 1: What is the detailed explanation of foundational concepts?
Answer confidence: 90.0%
WHY chain length: 3 steps
✓ Answer integrated into node <uuid>
  WHY chain depth: 3

=== EPISTEMIC STATE ===
Total nodes: 8
Known: 5
Gaps remaining: 2
  - Known Unknowns (KU): 2
  - SEED nodes (S): 0
  - PENDING nodes (P): 0
Epistemic closure reached: False

[... more iterations ...]

=== EPISODE SUMMARY ===
Episode ID: <uuid>
Topic: photosynthesis
Iterations: 5/5
Questions: 3/3
Total nodes: 20
Known concepts: 15
Remaining gaps: 0
Closure reached: True
Events logged: 42
```

## Key Concepts from Reference Specs

### From DIDACTIC_SPEC.md

- **Episode as state machine:** Transitions defined by Δ function
- **Epistemic closure:** Reached when KU = ∅
- **Main loop termination:** When KU empty or chunks exhausted
- **Node status lifecycle:** SEED → PENDING → KNOWN (or KNOWN_UNKNOWN as intermediate)

### From SCHEMA_SPEC.md

- **Immutability:** Every node update creates new version
- **Complete provenance:** Every node tracks: teacher_id, episode_id, subtopic, generation
- **WHY chain as causal steps:** Not just facts, but reasoning chains
- **Versioning:** Allows tracking of knowledge evolution

### From REWARD_SPEC.md

- **Base rewards:** KU resolved (0.4), deep WHY (0.6), cross-domain (0.8), SEED→KNOWN (0.9), new SEED (1.0)
- **Productive utility gate:** Prevents reward hacking through three gates:
  - G_gap: gap validity check
  - G_integration: answer integration check
  - G_unique: semantic uniqueness
- **MVP note:** Basic structure included, full implementation deferred

### From AXIOMATIC_FLOOR.md

- **Floor nodes:** Terminate WHY chains at principled stopping points
- **Not metaphysical:** Floor is pragmatic (can shift as knowledge grows)
- **Category A example:** Physical constants, fundamental laws, logic, causality
- **MVP floor:** 4 basic floor nodes for initialization

## Phase 2 Completion Criteria

✓ Single learner instance can conduct supervised didactic episode on defined topic
✓ Learner asks curiosity-driven questions from identified gaps
✓ WHY chains stored with proper schema (steps, certainty, provenance)
✓ System demonstrates epistemic closure when gaps are filled
✓ SEED nodes created for novel domains
✓ Axiomatic floor prevents infinite WHY recursion
✓ Knowledge graph persists in SQLite

## Next Steps (Phase 3+)

1. **Verifier Model:** Implement hallucination detection
2. **Human Supervision:** Integration points for human review
3. **Reward System:** Full implementation of productive utility gate
4. **Adversarial Collaboration:** Multi-agent interaction
5. **Generational Handoff:** Knowledge transfer between generations
6. **Real Teacher Integration:** Swap MockTeacher for actual LLM API

## Architecture References

- **ARCHITECTURE.md** — Full system design and pipelines
- **DIDACTIC_SPEC.md** — Formal episode state machine
- **SCHEMA_SPEC.md** — Node and edge schema specification
- **REWARD_SPEC.md** — Curiosity reward formal definition
- **AXIOMATIC_FLOOR.md** — Epistemic floor mechanism

## Design Philosophy

From the Sapien documentation:

> Learning is not a transfer of information.
> It is the construction of understanding.

This MVP embodies that philosophy:
- Knowledge is a **graph of causal relationships**, not disconnected facts
- **WHY chains** trace reasoning, not just memorization
- **SEED nodes** acknowledge the Unknown Unknowns
- **Epistemology** is explicit (provenance, uncertainty, floor)

---

**Phase 2 created:** June 2026
**Status:** MVP - Ready for testing and iteration
