# Sapien — Axiomatic Floor: Initial Proposal

> Every explanation ends somewhere.
> The question is not whether to have a floor,
> but how honestly to choose one.

---

## Table of Contents

1. [Purpose of This Document](#1-purpose-of-this-document)
2. [The Problem](#2-the-problem)
3. [What an Axiomatic Floor Is](#3-what-an-axiomatic-floor-is)
4. [What an Axiomatic Floor Is Not](#4-what-an-axiomatic-floor-is-not)
5. [Proposed Floor Categories](#5-proposed-floor-categories)
6. [Floor Node Schema](#6-floor-node-schema)
7. [Floor Selection Criteria](#7-floor-selection-criteria)
8. [Floor Governance](#8-floor-governance)
9. [Floor Revision Protocol](#9-floor-revision-protocol)
10. [Known Tensions](#10-known-tensions)
11. [Open Problems in This Proposal](#11-open-problems-in-this-proposal)

---

## 1. Purpose of This Document

ARCHITECTURE.md §18 and LIMITATIONS.md §8 identify WHY chain
infinite recursion as a High Severity limitation. Every causal
explanation can be asked "why?" again, descending without limit
into deeper physics, metaphysics, or logical foundations.

This document proposes an Axiomatic Floor — a defined set of
foundational concepts that Sapien accepts without further
justification — to terminate WHY chains at a principled stopping
point.

This is an initial proposal, not a final specification.
The open problems in Section 11 document where significant
work remains.

---

## 2. The Problem

Consider a simple WHY chain:

```
Fire is dangerous.
Why? Heat damages biological tissue.
Why? Proteins denature above ~60°C.
Why? Thermal energy disrupts hydrogen bonds in protein structures.
Why? Quantum mechanical interactions between atoms change at high temperatures.
Why? The electromagnetic force governs atomic bonding.
Why? Quantum field theory describes electromagnetic interactions.
Why? ...
Why? Fundamental physical constants have the values they have.
Why? ...
```

There is no natural floor to this sequence.
A system without a stopping criterion will recurse indefinitely —
consuming storage and computation without producing additional
useful knowledge for the learner.

Humans solve this problem implicitly. We accept certain things
as given without asking further. A child learning that fire is
hot does not need to understand quantum electrodynamics to act
safely around fire.

Sapien needs an explicit mechanism that achieves the same result.

---

## 3. What an Axiomatic Floor Is

The Axiomatic Floor F is a designated set of nodes in the
knowledge graph G that terminate WHY chains.

Formally:

```
F ⊆ N       — floor nodes are a subset of all nodes
```

A floor node n ∈ F satisfies:

```
n.why_chain = []           — empty WHY chain
n.status    = KNOWN        — treated as known without further justification
n.floor     = true         — explicitly marked as a floor node
```

When a WHY chain step reaches a floor node, the chain terminates:

```
traverse_why_chain(n, G):
    if n ∈ F:
        return [n]         — chain terminates here
    for each cause in n.why_chain:
        chain += traverse_why_chain(cause, G)
    return chain
```

Floor nodes are not gaps. They are not Unknown Unknowns.
They are deliberate stopping points — concepts the system accepts
as foundational without being unaware of them.

---

## 4. What an Axiomatic Floor Is Not

**The floor is not an assertion that floor concepts are unexplainable.**

Floor nodes exist at a practical boundary, not an explanatory one.
The electromagnetic force can be explained further — Sapien simply
does not need to go there for most purposes.

A floor node is marked `floor = true`, not `unexplainable = true`.
This distinction matters for integrity: Sapien should not pretend
its axiomatic floor is a metaphysical limit. It is a pragmatic one.

**The floor is not fixed.**

The floor is expected to shift as the system matures and as
research advances. A concept that is floor-level for Generation 1
may be explainable by Generation 5. See Section 9 — Floor Revision
Protocol.

**The floor is not universal across domains.**

Different topic domains may have different effective floors.
The floor for a medical knowledge graph is different from the
floor for a mathematical one. The floor is a function of the
current domain being learned, not a single global constant.

---

## 5. Proposed Floor Categories

Based on the design philosophy of Sapien and the domains it is
expected to operate in, the following categories of floor
concepts are proposed:

**Category A — Physical constants and fundamental laws**
Concepts accepted as empirical givens:
- Physical constants: speed of light, Planck's constant,
  gravitational constant, elementary charge
- Fundamental forces: electromagnetic, gravitational,
  strong nuclear, weak nuclear
- Conservation laws: energy, momentum, charge

These form the floor of physical causal chains.
WHY chains that reach a fundamental physical constant terminate.

**Category B — Mathematical foundations**
Concepts accepted as axiomatic in the mathematical sense:
- Peano axioms (number theory foundation)
- ZFC set theory axioms (or chosen alternative)
- Classical logic axioms (or chosen alternative)
- Euclidean or chosen geometric axioms

WHY chains that reach a mathematical axiom terminate.
A mathematical proof reaching an axiom is complete —
not shallow.

**Category C — Definitional primitives**
Concepts defined by their operational role rather than
by causal explanation:
- "Experience" — the fact that qualia exist, without
  explaining what qualia are
- "Existence" — the fact that something is, without
  explaining why there is something rather than nothing
- "Identity" — the fact that a thing is itself

These are philosophical primitives. Sapien does not need
to resolve philosophy of mind or metaphysics to function.
These are explicit floor nodes.

**Category D — Human consensus facts**
Empirical claims for which overwhelming human consensus
and evidence exist, accepted without requiring Sapien to
independently derive them:
- Historical facts (validated events)
- Geographic facts (physical boundaries, measurements)
- Scientific consensus claims (evolution, plate tectonics,
  age of the universe)

These form the floor of empirical claims. Importantly, this
category must be treated with care — human consensus can be
wrong. Floor nodes in Category D carry a designated label
distinguishing them from mathematical axioms.

---

## 6. Floor Node Schema

Floor nodes follow the standard node schema (SCHEMA_SPEC.md §3)
with the following extensions and constraints:

```json
{
  "concept_id":   "<UUID v4>",
  "version":      "<integer>",
  "label":        "<concept name>",
  "status":       "KNOWN",
  "floor":        true,
  "floor_category":"<A | B | C | D>",
  "floor_justification": "<why this concept is floor-level>",
  "floor_approved_by": "<human supervisor identifier>",
  "floor_approved_at": "<ISO 8601 timestamp>",
  "revisable":    true,
  "declarative": {
    "statement":  "<what this concept is>",
    "formal":     "<optional formal statement>"
  },
  "why_chain":    [],
  "provenance": {
    "teacher_id": "<agent or HUMAN_CONSENSUS or MATHEMATICAL_AXIOM>",
    "episode_id": "<UUID or FLOOR_INITIALIZATION>",
    "subtopic":   "<floor category label>",
    "generation": "<integer>"
  },
  "connections":  [],
  "uncertainty":  "<float — even floor nodes have uncertainty>",
  "reward_signal": 0.0,
  "created_at":   "<ISO 8601 timestamp>",
  "updated_at":   "<ISO 8601 timestamp>"
}
```

**Key differences from standard nodes:**

`floor = true` — explicitly marks this as a WHY chain termination point.
`floor_category` — A, B, C, or D, as defined in Section 5.
`floor_justification` — required prose explanation of why this
concept belongs at floor level.
`floor_approved_by` — floor node creation requires human supervisor
approval. No floor node can be created autonomously.
`why_chain = []` — floor nodes have empty WHY chains by definition.
`reward_signal = 0.0` — floor nodes do not generate curiosity reward.
Asking "why is this floor node true?" and being told "it is a
floor node" should not earn reward.
`uncertainty` — even floor nodes carry uncertainty. Mathematical
axioms can be questioned. Physical constants could be revised.
Category D (human consensus) can be wrong. The uncertainty of
floor nodes is not zero — it is simply expected to be low.

---

## 7. Floor Selection Criteria

A concept qualifies as a floor node if it satisfies all four
of the following criteria:

**Criterion 1 — Explanatory depth**
Further WHY chain extension beyond this concept provides
no additional predictive or reasoning utility for the
domains Sapien is expected to operate in.

A floor concept is not a hard explanatory wall —
it is a point of diminishing returns.

**Criterion 2 — Stability**
The concept has been stable across extended time in the
relevant field. A concept undergoing active scientific
revision is not floor-level. Floor nodes should not
require frequent revision.

**Criterion 3 — Human supervisor approval**
No concept can be self-designated as floor-level by
the learner. Floor node creation requires explicit human
supervisor approval.

**Criterion 4 — Explicit acknowledgment of the floor**
Floor nodes are not hidden. The existence of the floor,
the list of floor nodes, and the justification for each
are part of the documentation system and accessible to
anyone examining the knowledge graph.

---

## 8. Floor Governance

**Who manages the floor:**
The Axiomatic Floor is maintained by designated human
supervisors with authority over floor classification decisions.
Floor changes cannot be made by the Sapien learner itself.

**Floor transparency:**
The complete list of floor nodes, their categories, their
justifications, and their approval records is a publicly
accessible component of any deployed Sapien system.

Users and researchers inspecting the knowledge graph must
be able to identify every floor node and understand why
it holds floor status.

**Floor immutability within generations:**
Within a single generational cycle, the floor is stable.
It is revisited only at generational handoff.
Mid-generation floor changes risk destabilizing WHY chains
that depend on current floor nodes.

**Floor inheritance:**
When Generation n teaches Generation n+1, floor nodes are
taught as floor nodes — not as ordinary knowledge claims.
The next generation is told explicitly: "this concept is
accepted at floor level because..." and the justification
is transmitted.

Generation n+1 can raise questions about floor nodes through
the standard [QUESTION] or [PROPOSAL] issue system.
But floor status cannot be removed during active learning —
only during a designated floor review at generational handoff.

---

## 9. Floor Revision Protocol

The floor is not static. As understanding matures, concepts
that were floor-level may become explainable.

**Example of expected revision:**
A Sapien instance in early generations might hold
"protein denaturation at high temperatures" as a Category D
floor node — an empirical fact accepted without further
chemical explanation. A later generation with richer chemistry
knowledge may extend the WHY chain into molecular bond dynamics,
demoting the original floor node to an ordinary KNOWN node.

**Revision trigger conditions:**

1. A subsequent generation's teaching material provides a
   credible WHY chain for an existing floor node
2. Human supervisors determine the new WHY chain is valid
3. The floor node is reclassified from floor status to
   an ordinary KNOWN node with the new WHY chain committed

**Revision procedure:**

```
Review floor node n:

    proposed_why_chain ← teaching material or research contribution
    H.review(n, proposed_why_chain)

    if H.approved:
        n_v2 ← copy(n)
        n_v2.version    += 1
        n_v2.floor       = false
        n_v2.why_chain   = proposed_why_chain
        n_v2.status      = KNOWN
        store(n_v2)
        — n_v1 (floor version) is preserved in version history
```

**Direction of revision:**

Floor revision is almost always in one direction — floor nodes
become ordinary nodes as knowledge deepens. It is theoretically
possible for an ordinary KNOWN node to be promoted to floor status
if it turns out its WHY chain rested on circular reasoning or
unjustified assumptions. This is the more serious case and
requires elevated human oversight.

---

## 10. Known Tensions

**Tension 1 — The floor enables dogma**
Any concept designated as floor-level is protected from
further questioning within the system. This is necessary
for termination — and it creates a risk of institutionalized
dogma. Category D (human consensus) floor nodes are most
vulnerable to this. Consensus can be wrong. Human supervisors
must remain vigilant about floor nodes becoming sacred.

The mitigation is explicit floor justification, transparent
floor lists, and the revision protocol. But mitigation is not
elimination. This tension is genuine.

**Tension 2 — Floor size and reasoning quality**
A small floor requires deep WHY chains and produces richer
reasoning — but risks recursion and computational explosion.
A large floor terminates chains quickly — but risks shallow
understanding that treats too many things as given.
The correct floor size is a design question without a
principled answer in this specification.

**Tension 3 — Generation-dependent floor**
A floor appropriate for Generation 1 may be inappropriate
for Generation 10. What is floor-level for a learner with
limited knowledge becomes unnecessarily shallow for a
more advanced system. But floor revision requires human
oversight, which has its own scalability constraints.
Managing floor evolution across many generations is
an unsolved governance problem.

---

## 11. Open Problems in This Proposal

**1. Formal floor size**
This proposal defines what floor nodes are and how they
are governed. It does not specify how many floor nodes
are appropriate. Is a floor of 100 concepts correct?
1000? 10? The right floor size is unknown.

**2. Domain-specific floors**
The proposal acknowledges that different domains may have
different floors. It does not specify how domain boundaries
are determined or how a learner handles cross-domain
reasoning near the floor boundary.

**3. Floor for mathematical foundations**
Category B (mathematical axioms) assumes a specific set
of axioms (ZFC proposed above). Different mathematical
foundations produce different theorems. Whether Sapien
should commit to a specific mathematical foundation —
and which one — is an open question with philosophical
and practical consequences.

**4. Category D validation**
Human consensus can be wrong. The proposal does not
specify a mechanism for detecting when a Category D floor
node should be re-examined because the consensus has shifted
or was incorrect. Relying on human supervisors to notice
is necessary but insufficient.

**5. Emotional and aesthetic primitives**
If Sapien later incorporates affective weighting (see
LIMITATIONS.md §9), certain emotional and aesthetic primitives
may need floor-level treatment — "pain is aversive" being
one possible example. The current proposal does not address
this category.

---

*This proposal will be revised in light of Phase 2 prototype*
*experience and Phase 3 evaluation data.*
*Contributions to this document are especially welcome.*
*See CONTRIBUTING.md §3 — WHY chain depth termination.*

*Sapien — AGPLv3 — 28 May 2026*
*Author: Aarav — A Solo Engineer*
