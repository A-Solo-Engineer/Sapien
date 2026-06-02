# Phase 2 Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   DIDACTIC EPISODE (main.py)                    │
│                                                                 │
│  Orchestrates the learning loop from DIDACTIC_SPEC.md §6        │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴──────────────┐
                │                            │
    ┌───────────▼──────────┐    ┌────────────▼─────────┐
    │   LEARNER AGENT      │    │   TEACHER AGENT      │
    │   (agents/learner)   │    │  (agents/teacher)    │
    │                      │    │                      │
    │ • Gap identification │    │ • Chunk generation   │
    │ • Question gen       │    │ • Answer provision   │
    │ • Graph integration  │    │ • WHY chain creation │
    │ • State tracking     │    │ • LLM API            │
    └──────────┬───────────┘    └──────────────────────┘
               │
               │ reads/writes
               │
    ┌──────────▼────────────────────────────────────────┐
    │   EPISTEMIC STATE MANAGER (episode/state.py)      │
    │                                                   │
    │  Tracks: KK, KU, S, P                             │
    │  Detects: Epistemic closure (KU+S+P = ∅)          │
    │  Transitions: Node status changes                 │
    └──────────┬────────────────────────────────────────┘
               │
    ┌──────────▼───────────────────────────────────────┐
    │   KNOWLEDGE GRAPH DAG (graph/dag.py)             │
    │                                                  │
    │  ┌────────────────────────────────────────────┐  │
    │  │  NODES (graph/schema.py)                   │  │
    │  │  • concept_id (UUID)                       │  │
    │  │  • status (KNOWN|KNOWN_UNKNOWN|SEED|PND)   │  │
    │  │  • why_chain (causal steps)                │  │
    │  │  • provenance (teacher, episode, gen)      │  │
    │  │  • uncertainty (0.0-1.0)                   │  │
    │  │  • is_floor_node (boolean)                 │  │
    │  └────────────────────────────────────────────┘  │
    │                                                  │
    │  ┌────────────────────────────────────────────┐  │
    │  │  EDGES (graph/schema.py)                   │  │
    │  │  • source_id → target_id                   │  │
    │  │  • relation (CAUSES, USED_IN, etc)         │  │
    │  │  • strength (0.0-1.0)                      │  │
    │  │  • established_in (episode_id)             │  │
    │  └────────────────────────────────────────────┘  │
    │                                                  │
    │         SQLite Backend: knowledge_graph.db       │
    └──────────────────────────────────────────────────┘

                        CORE MODULES

    ┌─────────────────────┬─────────────────────────┐
    │                     │                         │
┌───▼──────────────┐  ┌───▼────────────────────┐    │
│  SEED NODES      │  │  WHY CHAINS            │    │
│  (core/seed.py)  │  │  (core/why_chain.py)   │    │
│                  │  │                        │    │
│ • create_seed    │  │ • build_why_step       │    │
│ • floor_init     │  │ • compute_depth        │    │
│ • floor_node     │  │ • is_deep_chain        │    │
│ • Category A     │  │ • validate_chain       │    │
└──────────────────┘  └────────────────────────┘    │
                                                    │
                 4 Axiomatic Floor Nodes:
              • causality
              • logic
              • set membership
              • empirical observation
```

## Episode Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. INITIALIZE                                               │
│    • Create DAG with SQLite                                 │
│    • Initialize 4 floor nodes (axiomatic floor)             │
│    • Initialize learner + epistemicstate                    │
└──────────┬──────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│ 2. RECEIVE CHUNKS                                           │
│    • Teacher provides ordered chunks for topic              │
│    • Learner processes each chunk                           │
│    • Create KNOWN_UNKNOWN nodes (identified gaps)           │
│    • Update epistemic state (KU += chunks)                  │
└──────────┬──────────────────────────────────────────────────┘
           │
           ├─► Is KU+S+P empty? ──► YES: EPISTEMIC CLOSURE (stop)
           │
           NO (continue)
           │
┌──────────▼──────────────────────────────────────────────────┐
│ 3. GENERATE QUESTION                                        │
│    • Select first gap from KU+S+P                           │
│    • Generate question pointing to that gap                 │
│    • Log question for tracing                               │
└──────────┬──────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│ 4. GET ANSWER                                               │
│    • Teacher answers with WHY chain                         │
│    • Extract steps: [{"claim": ..., "certainty": ...}]      │
│    • Confidence score for answer                            │
└──────────┬──────────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│ 5. INTEGRATE ANSWER                                         │
│    • Build WHY chain from steps                             │
│    • Create nodes for new concepts                          │
│    • Create edges (gap → new_concepts)                      │
│    • Update gap node with why_chain + KNOWN status          │
│    • Update epistemic state (KU -= integrated_gap)          │
└──────────┬──────────────────────────────────────────────────┘
           │
           └─► Go to step 2 (if iterations remaining)
```

## Data Model (SQLite Schema)

### NODES Table
```sql
CREATE TABLE nodes (
  concept_id TEXT PRIMARY KEY,      -- UUID
  version INTEGER,                  -- Semantic versioning
  label TEXT,                       -- Human-readable name
  status TEXT,                      -- KNOWN|KNOWN_UNKNOWN|SEED|PENDING
  statement TEXT,                   -- Plain language definition
  formal TEXT,                      -- Optional formal definition
  why_chain TEXT,                   -- JSON: [{step, claim, source, certainty}]
  provenance TEXT,                  -- JSON: {teacher_id, episode_id, subtopic, generation}
  uncertainty REAL,                 -- 0.0-1.0 confidence
  reward_signal REAL,               -- Curiosity reward at creation
  is_floor_node BOOLEAN,            -- True if terminates WHY chain
  created_at TEXT,                  -- ISO 8601 timestamp
  updated_at TEXT,                  -- ISO 8601 timestamp
  archived BOOLEAN,                 -- Slow storage flag
  flagged_by_human BOOLEAN,         -- Review flag
  flags TEXT                        -- JSON: [{flag_type, flagged_at, ...}]
);

CREATE INDEX idx_nodes_status ON nodes(status);
```

### EDGES Table
```sql
CREATE TABLE edges (
  edge_id TEXT PRIMARY KEY,         -- UUID
  source_id TEXT,                   -- concept_id
  target_id TEXT,                   -- concept_id
  relation TEXT,                    -- IS_TYPE_OF|USED_IN|CAUSES|CONTRADICTS|...
  strength REAL,                    -- 0.0-1.0 confidence
  established_in TEXT,              -- episode_id
  version INTEGER,                  -- Edge version
  created_at TEXT,                  -- ISO 8601 timestamp
  notes TEXT,                       -- Optional annotation
  FOREIGN KEY(source_id) REFERENCES nodes(concept_id),
  FOREIGN KEY(target_id) REFERENCES nodes(concept_id)
);

CREATE INDEX idx_edges_source ON edges(source_id);
CREATE INDEX idx_edges_target ON edges(target_id);
```

## Epistemic State Transitions

```
             Teacher Chunk Received
                      │
                      ▼
             Create KNOWN_UNKNOWN Node
          (identified gap, needs investigation)
                      │
                      ▼
            Learner Generates Question
              (points to KU gap)
                      │
                      ▼
            Teacher Answers with WHY Chain
           (causal explanation + steps)
                      │
                      ▼
          Learner Integrates into Graph
        (create nodes, edges, update status)
                      │
                      ▼
         Transition: KNOWN_UNKNOWN → KNOWN
           (gap filled with understanding)
                      │
                      ▼
          Check: Are there more gaps?
            (KU ∪ S ∪ P != ∅)?
                 /              \
              YES              NO
               │                 │
               ▼                 ▼
          More Questions    EPISTEMIC CLOSURE
                 │         (learning complete)
                 │                 │
                 └─────────────────┘
```

## Key Design Decisions

### 1. Epistemic States
- **KK (Known Knowns):** status = KNOWN, has WHY chain
- **KU (Known Unknowns):** status = KNOWN_UNKNOWN, identified gaps
- **S (SEED):** status = SEED, isolated new domains
- **P (PENDING):** status = PENDING, partial connections

### 2. WHY Chains
- Stored as ordered list of causal steps
- Each step has certainty value (0.0-1.0)
- Aggregate certainty = minimum of steps (chain is only as strong as weakest link)
- Deep chains (≥3 steps) indicate causal understanding vs. surface facts

### 3. Axiomatic Floor
- 4 floor nodes prevent infinite WHY recursion
- Floor nodes have: empty why_chain, status=KNOWN, is_floor_node=true
- Category A: foundational concepts (causality, logic, etc.)
- Can be extended in future phases

### 4. Provenance Tracking
- Every node records: teacher_id, episode_id, subtopic, generation
- Enables tracing knowledge back to source
- Supports generational handoff (Phase 3+)

### 5. SQLite Backend
- Per SCHEMA_SPEC.md §9 recommendation for relational storage
- Efficient querying by status (indexed)
- Immutable versioning (new records on updates)
- Easy inspection and debugging

## Completion Status

**Phase 2 MVP:** ✅ COMPLETE

All components implemented and tested:
- ✅ Knowledge graph with persistence
- ✅ Epistemic state management
- ✅ Didactic episode loop
- ✅ SEED nodes + axiomatic floor
- ✅ WHY chain construction
- ✅ Teacher/Learner agents
- ✅ Successful test run with epistemic closure

---

**Next Phase:** Verifier model + Adversarial collaboration
