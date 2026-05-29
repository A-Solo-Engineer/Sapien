# Sapien — Knowledge Graph Schema Specification

> The shape of knowledge determines what can be known.

---

## Table of Contents

1. [Purpose of This Document](#1-purpose-of-this-document)
2. [Design Principles](#2-design-principles)
3. [Node Schema](#3-node-schema)
4. [Edge Schema](#4-edge-schema)
5. [Node Status Lifecycle](#5-node-status-lifecycle)
6. [Relation Type Definitions](#6-relation-type-definitions)
7. [Versioning and Immutability](#7-versioning-and-immutability)
8. [Graph Constraints](#8-graph-constraints)
9. [Storage Representation](#9-storage-representation)
10. [Retrieval Protocol](#10-retrieval-protocol)
11. [Archival Policy](#11-archival-policy)
12. [Schema Validation Rules](#12-schema-validation-rules)
13. [Open Problems in This Specification](#13-open-problems-in-this-specification)

---

## 1. Purpose of This Document

ARCHITECTURE.md §14 describes the DAG at a conceptual level with
a prose-and-pseudocode node structure. This document formalizes
that description into a complete, unambiguous schema specification.

The schema defined here is the canonical reference for:

- Any prototype implementation of the knowledge graph
- Validation of whether a given storage format is Sapien-compatible
- Reasoning about graph properties, constraints, and edge cases

Where this schema conflicts with ARCHITECTURE.md, this document
takes precedence. Where this schema is silent, ARCHITECTURE.md
governs.

---

## 2. Design Principles

**Immutability**
Knowledge is never overwritten. Every update to a node creates a
new version. Old versions are preserved for provenance and audit.
This is not a performance optimization — it is a philosophical
commitment. Sapien's knowledge must be traceable to its origin.

**Explicit uncertainty**
Every node carries an uncertainty value. Certainty is a special
case of uncertainty, not its opposite. A node with uncertainty 0.0
is a node the system is maximally confident about — not a node
where uncertainty has been ignored.

**Contradiction preservation**
Contradictions are stored, not resolved. When two nodes conflict,
a CONTRADICTS edge is created between them. The graph deliberately
holds opposing truths until resolution is possible through evidence,
adversarial collaboration, or human authority.

**Complete provenance**
Every node records where its knowledge came from — which teacher,
which episode, which subtopic. A knowledge claim with no provenance
is not a valid Sapien node.

**Structural interpretability**
The schema is designed for human inspection. A person with access
to the graph should be able to follow any WHY chain and understand
both the claim and its full reasoning history.

---

## 3. Node Schema

A node is the fundamental unit of the Sapien knowledge graph.
Every concept, fact, or claim is represented as a node.

```json
{
  "concept_id":   "<UUID v4>",
  "version":      "<integer, starting at 1, incremented on update>",
  "label":        "<human-readable concept name, max 256 chars>",
  "status":       "<KNOWN | KNOWN_UNKNOWN | SEED | PENDING>",
  "declarative": {
    "statement":  "<what this concept is, in plain language>",
    "formal":     "<optional formal or mathematical statement>"
  },
  "why_chain": [
    {
      "step":     "<integer — step index, 1-based>",
      "claim":    "<causal statement for this step>",
      "source":   "<provenance reference — see provenance schema>",
      "certainty":"<float 0.0–1.0 — confidence in this specific step>"
    }
  ],
  "provenance": {
    "teacher_id": "<agent identifier of the teaching source>",
    "episode_id": "<UUID of the didactic episode>",
    "subtopic":   "<label of the chunk within the episode>",
    "generation": "<integer — which Sapien generation taught this>"
  },
  "connections":  "<array of edge objects — see Edge Schema>",
  "uncertainty":  "<float 0.0–1.0 — aggregate confidence in this node>",
  "reward_signal":"<float 0.0–1.0 — reward value at creation>",
  "created_at":   "<ISO 8601 timestamp>",
  "updated_at":   "<ISO 8601 timestamp>",
  "archived":     "<boolean — true if moved to slow storage>",
  "flagged_by_human": "<boolean — human supervisor has reviewed>",
  "flags": [
    {
      "flag_type": "<HALLUCINATION | CONTRADICTION | SEED | REVIEW>",
      "flagged_at":"<ISO 8601 timestamp>",
      "flagged_by":"<agent or human identifier>",
      "note":      "<optional free-text explanation>"
    }
  ]
}
```

### Field Definitions

**concept_id**
Globally unique identifier for this concept. UUID v4.
Never reused, even after archival.

**version**
Integer version counter. The first time a node is created,
version = 1. Each subsequent update creates a new record with
version = previous + 1. Old versions are never deleted.

**label**
A short, human-readable name for the concept. Not a sentence —
a concept title. Examples: "heat transfer", "causal inference",
"SEED node formation".

**status**
Current epistemic status. See Section 5 for the full lifecycle.

**declarative**
A plain-language statement of what the concept is (the WHAT).
The optional `formal` field holds a mathematical, logical, or
structured statement for concepts that admit precise formalization.

**why_chain**
The causal reasoning chain (the WHY). An ordered list of causal
steps from the concept back to its grounding or axiomatic floor.
Each step carries its own certainty value.

**provenance**
Epistemic provenance — where this knowledge came from.
Required for every node. A node with no provenance is invalid.

**connections**
Directed edges to other nodes. See Edge Schema in Section 4.

**uncertainty**
Aggregate confidence in this node. Computed from:
- Certainty values of individual WHY chain steps
- Trust rating of the teaching source
- Agreement or disagreement from adversarial collaboration
- Human supervisor assessments

Not a derived field — explicitly stored and updated.

**reward_signal**
The curiosity reward received at the moment of node creation.
Recorded for analysis of learning patterns across generations.
See REWARD_SPEC.md for the reward signal specification.

---

## 4. Edge Schema

An edge represents a directed relationship between two nodes.

```json
{
  "edge_id":      "<UUID v4>",
  "source_id":    "<concept_id of the source node>",
  "target_id":    "<concept_id of the target node>",
  "relation":     "<IS_TYPE_OF | USED_IN | CAUSES | CONTRADICTS |
                    RELATED_TO | APPLIED_IN>",
  "strength":     "<float 0.0–1.0 — connection confidence>",
  "established_in":"<episode_id where this edge was created>",
  "created_at":   "<ISO 8601 timestamp>",
  "version":      "<integer — as with node versioning>",
  "notes":        "<optional free-text annotation>"
}
```

### Field Definitions

**edge_id**
Globally unique identifier for this specific edge.
Allows edge history to be tracked independently of nodes.

**strength**
How confident the system is that this relationship holds.
1.0 means the connection is fully established with complete WHY
chains on both ends. Lower values indicate weaker or partial
connections established through inference rather than direct
teaching.

**relation**
The semantic type of the relationship. See Section 6 for
complete definitions of each relation type.

---

## 5. Node Status Lifecycle

Nodes transition through a defined lifecycle:

```
                    ┌─────────────────┐
                    │      SEED       │
                    │ (new territory, │
                    │  no connections)│
                    └────────┬────────┘
                             │
                    partial connections
                    accumulate
                             │
                             ▼
                    ┌─────────────────┐
                    │    PENDING      │
                    │ (partial WHY    │
                    │  chain, awaiting│
                    │  bridge concepts│
                    └────────┬────────┘
                             │
                    bridge concepts
                    taught in future
                    episode
                             │
                             ▼
┌─────────────────┐          │           ┌─────────────────┐
│  KNOWN_UNKNOWN  │          │           │      KNOWN      │
│ (gap identified,│──question │           │ (full WHY chain │
│  question       │  answered─┤           │  established)   │
│  pending)       │          └──────────►│                 │
└─────────────────┘                      └─────────────────┘
        ▲                                        │
        │                                        │
        └────────────────────────────────────────┘
                new contradicting evidence
                or revised teaching reduces
                certainty below threshold
```

**Status transition rules:**

| From | To | Condition |
|---|---|---|
| SEED | PENDING | First connection edge established to G |
| PENDING | KNOWN | WHY chain complete, uncertainty ≤ θ_known |
| PENDING | SEED | All connections severed (edge strength → 0) |
| KNOWN | KNOWN_UNKNOWN | New contradicting evidence reduces certainty below θ_known |
| KNOWN_UNKNOWN | KNOWN | Gap closed by question/answer exchange |

Where θ_known is the minimum certainty threshold for KNOWN status.
The initial proposed value is 0.6 — a node requires at least
60% confidence to be considered known. This value is a
design parameter requiring empirical validation.

---

## 6. Relation Type Definitions

| Relation | Direction | Definition |
|---|---|---|
| IS_TYPE_OF | A → B: A is a type of B | Taxonomic subsumption. A is a more specific instance of B. |
| USED_IN | A → B: A is used in B | Functional dependency. A appears as a component or mechanism within B. |
| CAUSES | A → B: A causes B | Causal direction. A is a sufficient or contributing cause of B. |
| CONTRADICTS | A ↔ B | Epistemic conflict. A and B cannot both be fully true under the same interpretation. Bidirectional — if A contradicts B, B contradicts A. |
| RELATED_TO | A ↔ B | Associative relationship without causal direction. A and B are semantically adjacent but no causal or taxonomic link is established yet. |
| APPLIED_IN | A → B: A is applied in B | Application instance. A (an abstract concept or method) has a concrete application within B (a real-world context or domain). |

**On CONTRADICTS:**

CONTRADICTS is the only relation that is intrinsically bidirectional.
When A CONTRADICTS B, two edges are stored — one in each direction.
This preserves the symmetry of the conflict and allows traversal
from either node.

Neither node is automatically marked uncertain when CONTRADICTS is
established. The contradiction is tracked explicitly. Resolution
occurs through adversarial collaboration, new evidence, or human
authority — not by automatically lowering one node's certainty.

See CONTRADICTION_FRAMEWORK.md for the full contradiction
resolution specification.

---

## 7. Versioning and Immutability

**Immutability rule:**

Once committed, a node record is never modified in place.

When a node must be updated — its WHY chain extended, its
certainty recalculated, its status changed — a new version is
created:

```
node_v2 = copy(node_v1)
node_v2.version    = node_v1.version + 1
node_v2.updated_at = now()
[apply changes to node_v2]
store(node_v2)
[node_v1 remains unchanged in storage]
```

**Version chain access:**

Given any `concept_id`, all historical versions of that node
are retrievable by querying all records with that `concept_id`
ordered by version.

The current active version is always the highest-numbered version.

**Why immutability matters:**

An AI system that silently overwrites its own knowledge history
is an AI system whose past cannot be audited. Sapien's
generational architecture requires complete auditability — future
generations and human supervisors must be able to trace how any
belief formed and how it changed over time. Immutability is the
technical foundation of that auditability.

---

## 8. Graph Constraints

These constraints must hold at all times. A graph that violates
any of these is not a valid Sapien knowledge graph.

**C1 — Acyclicity**
The graph must be a DAG. No directed cycle may exist among
CAUSES, IS_TYPE_OF, or USED_IN edges. CONTRADICTS and RELATED_TO
edges are bidirectional and are exempt from the acyclicity
constraint.

Formally: for all non-CONTRADICTS, non-RELATED_TO edge sequences
(n₁→n₂→...→nₖ), n₁ ≠ nₖ.

**C2 — Unique concept_id**
No two nodes with different content may share the same
concept_id. A concept_id uniquely identifies one concept
across all versions and all generations.

**C3 — Provenance completeness**
Every node must have a non-null provenance object with
valid teacher_id, episode_id, and generation fields.
Nodes with missing provenance must not be committed to G.

**C4 — WHY chain for KNOWN nodes**
A node with status KNOWN must have a non-empty why_chain
with at least one step. A KNOWN node with an empty why_chain
is a schema violation.

**C5 — CONTRADICTS symmetry**
If edge A CONTRADICTS B exists, then edge B CONTRADICTS A
must also exist. A unidirectional CONTRADICTS edge is invalid.

**C6 — Strength bounds**
All strength and uncertainty values must satisfy 0.0 ≤ v ≤ 1.0.
Values outside this range are schema violations.

**C7 — Version monotonicity**
For any concept_id, version numbers must be strictly
increasing. No two versions of the same concept may share
a version number.

---

## 9. Storage Representation

The schema above is storage-format agnostic. Three candidate
storage formats are discussed below. The final choice is an
implementation decision for Phase 2.

**Option A — Native graph database (e.g., Neo4j, ArangoDB)**
Nodes map to graph database nodes. Edges map to relationships.
Properties map to node/relationship properties.

*Advantages:* Native graph traversal, ACID compliance, mature
tooling, native support for relationship types.
*Disadvantages:* External dependency, operational complexity,
potential licensing concerns.

**Option B — Adjacency-list representation in a relational database**
Nodes stored in a `nodes` table. Edges stored in an `edges` table
with source_id and target_id foreign keys.

*Advantages:* Universal tooling, easy backup and migration, no
special graph database expertise required.
*Disadvantages:* Graph traversal requires recursive queries or
application-level traversal logic. Performance degrades at scale.

**Option C — Custom memory-mapped binary format**
Nodes and edges stored in flat binary files with an in-memory
index for fast traversal.

*Advantages:* Maximum performance, no external dependencies.
*Disadvantages:* High implementation complexity, no existing tooling,
risk of bugs in custom serialization.

**Recommendation for Phase 2 prototype:**
Option B — relational database adjacency list.
It imposes no external graph database dependency and is
sufficient for a prototype at small scale. Migration to
Option A can occur when scale demands it.

---

## 10. Retrieval Protocol

When L receives a query — a question to answer or new material
to evaluate — the retrieval protocol is:

```
retrieve(query, G):

    candidates ← semantic_match(query, G)
                — find top-K nodes by semantic similarity

    for each n in candidates:
        chain ← traverse_why_chain(n, G)
        certainty ← aggregate_certainty(chain)

    response ← construct_response(candidates, chains)
    uncertainty ← aggregate_uncertainty(candidates)
    provenance ← collect_provenance(candidates)

    return {
        response:    response,
        uncertainty: uncertainty,
        provenance:  provenance,
        sources:     [n.concept_id for n in candidates]
    }
```

**Responses always include uncertainty and provenance.**

A response without an uncertainty estimate is not a valid
Sapien response. The system must communicate confidence,
not just conclusions.

---

## 11. Archival Policy

When Gₜ approaches the hardware storage limit for the current
learner instance, low-priority nodes are moved to archival storage.

**Archival does not mean deletion.**

An archived node retains its full schema — all fields, all versions,
all WHY chains, all provenance. Only retrieval latency increases.

**Retention priority order (highest to lowest):**

1. Nodes flagged by human supervisor (`flagged_by_human = true`)
2. SEED nodes and their immediate descendants
3. Nodes with high connection count (degree centrality in G)
4. Nodes referenced in the most recent N episodes
5. Nodes with high certainty and complete WHY chains
6. All other nodes

**No node is ever permanently deleted.**

Deletion would violate the provenance and auditability requirements
of the architecture. Every node ever created must remain
recoverable, however slowly.

---

## 12. Schema Validation Rules

A knowledge graph G is valid if and only if all of the following
hold:

```
validate(G):

    for each n in G.nodes:
        assert n.concept_id is UUID-v4-format
        assert n.version >= 1
        assert n.status in {KNOWN, KNOWN_UNKNOWN, SEED, PENDING}
        assert n.uncertainty in [0.0, 1.0]
        assert n.reward_signal in [0.0, 1.0]
        assert n.provenance is not null
        assert n.provenance.teacher_id is not null
        assert n.provenance.episode_id is not null
        if n.status = KNOWN:
            assert len(n.why_chain) >= 1
        for each step in n.why_chain:
            assert step.certainty in [0.0, 1.0]

    for each e in G.edges:
        assert e.source_id in G.node_ids
        assert e.target_id in G.node_ids
        assert e.relation in valid_relation_types
        assert e.strength in [0.0, 1.0]

    assert is_dag(G, exclude_relations={CONTRADICTS, RELATED_TO})

    for each e in G.edges where e.relation = CONTRADICTS:
        assert reverse_edge_exists(e, G)

    return VALID
```

---

## 13. Open Problems in This Specification

**1. Semantic match function**
The retrieval protocol calls `semantic_match(query, G)`. The
implementation of this function — graph embeddings, vector
similarity, or structured query expansion — is not specified.
The correct approach depends on graph scale and the embedding
strategy used for node labels and declarative statements.

**2. WHY chain certainty aggregation**
`aggregate_certainty(chain)` is referenced but not formally
defined. A chain of causal steps each with their own certainty
values must be combined into a single node-level certainty.
Simple multiplication is the naive approach but underestimates
certainty for long chains. A principled aggregation function
is an open research problem.

**3. θ_known calibration**
The threshold θ_known (minimum certainty for KNOWN status)
is proposed as 0.6 but has no principled justification.
The correct value may be domain-dependent, generation-dependent,
or impossible to define universally. Empirical calibration
during Phase 3 is expected to refine this value.

**4. Contradiction impact on connected nodes**
The current schema stores CONTRADICTS edges but does not
specify how a contradiction between A and B affects the
certainty of nodes connected to A or B. Uncertainty
propagation through a graph containing contradictions is
formally undefined. See CONTRADICTION_FRAMEWORK.md.

---

*This specification supersedes the node structure in ARCHITECTURE.md §14*
*where the two documents conflict.*
*It will be updated as open problems are resolved.*

*Sapien — AGPLv3 — 28 May 2026*
*Author: Aarav — A Solo Engineer*
