# Sapien — Contradiction Resolution Framework

> A system that silences contradiction does not resolve it.
> It buries it.
> Buried contradictions resurface — usually at the worst time.

---

## Table of Contents

1. [Purpose of This Document](#1-purpose-of-this-document)
2. [Why Contradictions Must Be Preserved](#2-why-contradictions-must-be-preserved)
3. [Types of Contradiction in Sapien](#3-types-of-contradiction-in-sapien)
4. [The CONTRADICTS Edge — Formal Behavior](#4-the-contradicts-edge--formal-behavior)
5. [Uncertainty Propagation Through Contradiction](#5-uncertainty-propagation-through-contradiction)
6. [Resolution Pathways](#6-resolution-pathways)
7. [Reasoning Under Unresolved Contradiction](#7-reasoning-under-unresolved-contradiction)
8. [Contradiction Across Generations](#8-contradiction-across-generations)
9. [Probabilistic Epistemology — Future Direction](#9-probabilistic-epistemology--future-direction)
10. [Open Problems in This Framework](#10-open-problems-in-this-framework)

---

## 1. Purpose of This Document

ARCHITECTURE.md §14 establishes that contradictions in Sapien
are stored, not suppressed. A CONTRADICTS edge is created
between conflicting nodes. Neither node is deleted.

LIMITATIONS.md §6 identifies contradiction resolution as a
High Severity open problem: the architecture currently lacks
formal procedures for reasoning about contradictions,
propagating uncertainty through them, and resolving them
when resolution is possible.

This document proposes a formal framework for:

- How CONTRADICTS edges behave formally
- How uncertainty propagates through nodes connected by contradiction
- Under what conditions contradiction can be resolved
- How the learner reasons when a contradiction is unresolved
- How contradictions are handled across generational handoff

This is a framework proposal, not a final specification.
The open problems in Section 10 document where formal
work remains incomplete.

---

## 2. Why Contradictions Must Be Preserved

The instinctive engineering response to contradiction is
to resolve it — choose a winner, delete the loser, move on.

Sapien explicitly rejects this approach for four reasons.

**Reason 1 — Many genuine contradictions are unresolved.**
Consciousness is computational or biological. Free will exists
or it does not. Fine-tuned physical constants are designed or
coincidental. These are not solvable by selecting one side
and discarding the other. A system that pretends to resolve
them is lying.

**Reason 2 — Suppressed contradictions corrupt provenance.**
If Sapien silently overwrites node A with node B because B
arrived more recently, the fact that A ever existed — and
was taught by a specific teacher in a specific episode —
is erased. This breaks the provenance requirement. The
knowledge graph must be able to explain how it reached
any belief, including beliefs it later revised.

**Reason 3 — Contradictions are information.**
The existence of a contradiction between two sources signals
something meaningful: the sources disagree, one may be wrong,
or the question is genuinely contested. This signal is
epistemically valuable. Erasing it destroys information.

**Reason 4 — Adversarial collaboration requires it.**
The adversarial collaboration mechanism (ARCHITECTURE.md §6)
depends on instances having genuine disagreements that can
be debated. If contradictions are silently resolved before
adversarial collaboration can act on them, the mechanism
has nothing to work with.

---

## 3. Types of Contradiction in Sapien

Not all contradictions are equal. The framework distinguishes
four types:

**Type 1 — Factual contradiction**
Two nodes make directly opposing claims about a verifiable fact.

```
Node A:  "The Eiffel Tower is 324 metres tall."
Node B:  "The Eiffel Tower is 330 metres tall."
```

One of these is wrong. Factual contradictions are resolvable
in principle — through evidence, authoritative sources, or
human supervisor verification.

**Type 2 — Methodological contradiction**
Two nodes use the same terms but with different definitions or
methodologies, producing apparently opposing conclusions.

```
Node A:  "Intelligence is fixed at birth." (heritability studies)
Node B:  "Intelligence is highly malleable." (intervention studies)
```

The contradiction may dissolve under disambiguation. It is not
that one is wrong — they may be measuring different things.
Methodological contradictions require clarification before
resolution is possible.

**Type 3 — Theoretical contradiction**
Two established theoretical frameworks produce incompatible
predictions in some domain.

```
Node A:  "Quantum mechanics governs all physical phenomena."
Node B:  "General relativity governs all physical phenomena."
```

Both are well-supported theories that currently have no complete
unified formulation. Theoretical contradictions are unresolvable
with current knowledge. They must be held open — possibly for
generations.

**Type 4 — Philosophical contradiction**
Claims that cannot be adjudicated by evidence because they
concern questions that evidence cannot settle.

```
Node A:  "Subjective experience is reducible to physical processes."
Node B:  "Subjective experience is not reducible to physical processes."
```

Philosophical contradictions may never be resolvable. They are
preserved as open questions, not as errors to be corrected.

---

## 4. The CONTRADICTS Edge — Formal Behavior

Formal definition from SCHEMA_SPEC.md §6:

```
CONTRADICTS(A, B) implies CONTRADICTS(B, A)
```

Both edges are stored. The CONTRADICTS relationship is symmetric
and bidirectional.

**When CONTRADICTS is created:**

A CONTRADICTS edge between A and B is created when:

1. A teaching episode presents material B that conflicts with
   existing node A, AND
2. The conflict is flagged by the verifier model V or identified
   by adversarial collaboration, AND
3. The conflict cannot be resolved within the episode through
   clarification or disambiguation

OR

1. Human supervisor H identifies a conflict between A and B
   that the automated systems missed

**What CONTRADICTS does NOT do automatically:**

- Reduce the certainty of A or B
- Trigger deletion of either node
- Block the learner from using A or B in reasoning
- Force immediate resolution

The existence of a CONTRADICTS edge is a flag, not a verdict.

**What CONTRADICTS DOES do automatically:**

- Log both nodes in a contradiction tracking register
- Alert human supervisors of new contradictions above a
  severity threshold
- Mark both nodes with a flag: `flags: [{flag_type: "CONTRADICTION"}]`
- Inhibit both nodes from being presented to the next generation
  as resolved facts until the contradiction is addressed

---

## 5. Uncertainty Propagation Through Contradiction

When A CONTRADICTS B, the uncertainty of A and B must be updated
to reflect the existence of the conflict.

**Proposed propagation rule:**

Let:
- u_A = current uncertainty of A
- u_B = current uncertainty of B
- s_AB = strength of the CONTRADICTS edge (how severe the conflict is)

After CONTRADICTS(A, B) is established:

```
u_A_new = u_A + (s_AB × (1 - u_A))
u_B_new = u_B + (s_AB × (1 - u_B))
```

This formula:
- Increases uncertainty of both A and B
- Scales the increase by the severity of the contradiction
- Cannot push uncertainty above 1.0 (the formula is bounded)
- Does not reduce the uncertainty of either node — the
  contradiction is not evidence that either is true, only
  that the situation is less certain than before

**s_AB — contradiction strength:**

s_AB is assessed at the time the CONTRADICTS edge is created.
It is not a mechanical calculation — it requires judgment
about how direct and severe the conflict is.

Proposed initial values:

| Contradiction type | Proposed s_AB |
|---|---|
| Direct factual opposition | 0.8 |
| Methodological disagreement | 0.4 |
| Theoretical incompatibility | 0.6 |
| Philosophical disagreement | 0.2 |

These values are proposed heuristics, not formal derivations.
See Section 10, item 1.

**Propagation to connected nodes:**

Nodes connected to A or B by causal edges inherit partial
uncertainty increases from the contradiction. The propagation
decays with distance from the contradicted node:

```
For each node C connected to A by an edge with strength s_CA:
    u_C_new = u_C + (s_CA × u_A_new × decay_factor)
```

Where `decay_factor` is a constant less than 1.0, controlling
how far contradiction uncertainty propagates through the graph.

Initial proposed value: `decay_factor = 0.3`

This means a contradiction reduces the certainty of directly
connected nodes by 30% of its own uncertainty increase —
and nodes two steps away by 9%, three steps away by 2.7%,
and so on. Uncertainty propagation has a natural tail-off.

---

## 6. Resolution Pathways

Contradictions are resolved through three mechanisms.
All three require human supervisor confirmation.

**Pathway 1 — Evidence resolution**
New evidence, authoritative sources, or direct measurement
establishes which of the two contradicting nodes is correct.

Procedure:
```
1. Evidence e is presented to learner L or human supervisor H
2. H evaluates e against nodes A and B
3. H determines:
   — e supports A: B is reclassified as KNOWN with reduced
     certainty, CONTRADICTS edge weight adjusted
   — e supports B: A is reclassified similarly
   — e supports neither: CONTRADICTS edge persists
   — e supports a synthesis C: new node C is created,
     both A and B gain RELATED_TO edges to C
4. Resolution is logged in both A and B as a flag entry
```

**Pathway 2 — Disambiguation resolution**
The apparent contradiction dissolves when it is found that A and B
use different definitions of a shared term or measure different things.

Procedure:
```
1. Analysis reveals definitional mismatch between A and B
2. A and B are both updated with clarified declarative statements
3. CONTRADICTS edge is replaced with RELATED_TO edges
4. No node is deleted — both concepts are preserved
   with their respective scopes clarified
```

**Pathway 3 — Adversarial debate resolution**
Instance A and Instance B reach a conclusion through structured
debate that human supervisors ratify.

Procedure:
```
1. Instance A presents its WHY chain for node A
2. Instance B presents its WHY chain for node B
3. Verifier model V evaluates both chains for consistency
4. Human supervisor H reviews and determines:
   — One chain is stronger (based on depth, source quality,
     logical consistency)
   — Both chains are weak — contradiction remains open
   — A synthesis emerges from the debate
5. The stronger chain's node has its uncertainty reduced
6. The weaker chain's node has its uncertainty increased
7. Both nodes and their WHY chains are preserved
```

**What resolution does NOT do:**

Resolution never deletes a node. Even if node B is determined
to be incorrect after a factual contradiction, node B is preserved
in the knowledge graph with:
- Its certainty significantly reduced
- Its CONTRADICTS edge weight reduced
- A resolution flag documenting what was determined and by whom
- Its WHY chain intact as a historical record

Deletion would destroy provenance. Preservation with
updated certainty and flags maintains the full epistemic history.

---

## 7. Reasoning Under Unresolved Contradiction

When the learner L must reason about a question that touches
an unresolved CONTRADICTS edge, three behaviors are defined:

**Behavior 1 — Transparent dual presentation**
The learner presents both nodes, their uncertainty values,
and the contradiction explicitly:

```
"There are two established positions on this question.
Position A holds that [declarative_A] (certainty: u_A,
source: provenance_A). Position B holds that [declarative_B]
(certainty: u_B, source: provenance_B). These positions are
in direct conflict. This contradiction is currently unresolved."
```

This is the default behavior when uncertainty on both sides
is high and no resolution has occurred.

**Behavior 2 — Weighted preference**
When one node has significantly higher certainty than the other,
the learner can express a weighted preference while acknowledging
the contradiction:

```
"The stronger-supported position is [declarative_A]
(certainty: u_A). An alternative position [declarative_B]
exists (certainty: u_B) but is in direct conflict with
the former. The confidence gap is [u_A - u_B]."
```

Threshold for weighted preference: u_A - u_B > 0.3

**Behavior 3 — Deferral to human**
For questions where the contradiction is Type 3 (theoretical)
or Type 4 (philosophical) and both nodes carry high certainty
on their respective sides, the learner defers:

```
"This question involves a currently unresolved [theoretical /
philosophical] contradiction in the knowledge graph. Human
supervisor input is required for questions that depend on its
resolution."
```

Deferral is not failure. A learner that knows what it does not
know — and says so — is epistemically healthier than one that
fabricates resolution.

---

## 8. Contradiction Across Generations

When Generation n teaches Generation n+1, how are unresolved
contradictions transmitted?

**Unresolved contradictions are taught as unresolved.**

Generation n does not present a contested claim as settled
simply because it cannot resolve it. During generational
handoff, each significant unresolved CONTRADICTS pair is
presented to Generation n+1 through a dedicated teaching session
that:

1. Presents both nodes and their WHY chains
2. Explains why the contradiction exists
3. Documents what resolution attempts have been made
4. Explicitly marks the question as open

Generation n+1 builds its own DAG entries for both nodes —
starting with the uncertainty values inherited from Generation n.
It may later contribute new resolution through its own learning
and adversarial collaboration.

**Contradictions as open research problems:**

Significant long-standing unresolved contradictions are
candidates for documentation in the project's public issues
as `[RESEARCH]` questions — inviting external researchers to
contribute resolution pathways.

This transforms internal epistemic conflicts into explicit
research contributions. Sapien's knowledge graph is a living
record of what humanity does and does not yet know.

---

## 9. Probabilistic Epistemology — Future Direction

The current framework represents contradiction through discrete
nodes, binary CONTRADICTS edges, and scalar uncertainty values.
This is a simplification.

A more powerful long-term approach is a fully probabilistic
knowledge graph where:

- Nodes carry probability distributions over their truth values,
  not scalar uncertainty estimates
- CONTRADICTS edges carry conditional probability relationships
- Belief revision follows Bayes' theorem formally
- Uncertainty propagation follows established probabilistic
  graphical model rules

**Why this is not the current approach:**

Fully probabilistic belief networks at the scale Sapien requires
are computationally demanding to maintain and update in real time.
The scalar uncertainty approach is a practical approximation
that preserves the core epistemic properties — tracking
uncertainty, propagating it through contradictions, and
updating it as evidence arrives — without the full computational
overhead.

**Candidate frameworks for future development:**

- Bayesian networks — nodes carry conditional probability tables
- Dempster-Shafer theory — belief and plausibility functions
  over propositions, formally handle incomplete evidence
- Imprecise probabilities — intervals rather than point values,
  better suited to genuine uncertainty about uncertainty
- Paraconsistent logic — formal logical systems that tolerate
  contradictions without making everything derivable (ex contradictione quodlibet)

These frameworks are documented here as future directions,
not current commitments. The transition from scalar uncertainty
to probabilistic epistemology is expected during Phase 4 or later.

---

## 10. Open Problems in This Framework

**1. Principled derivation of s_AB values**
The proposed contradiction strength values (Section 5) are
heuristics. No formal method exists for computing how strongly
two contradicting nodes conflict. Direct factual contradiction
between two specific measurements has a different severity
than a broad theoretical incompatibility. A principled
approach to s_AB derivation is an open research problem.

**2. Decay factor calibration**
The uncertainty propagation decay factor is proposed as 0.3
without empirical justification. A high decay factor spreads
uncertainty widely through the graph — potentially degrading
the certainty of many nodes over time as contradictions
accumulate. A low factor keeps contradictions too localized.
The correct value requires empirical calibration in Phase 3.

**3. Contradiction accumulation at scale**
In a knowledge graph with billions of nodes, the number of
CONTRADICTS edges may grow significantly. Managing, tracking,
and reasoning about a large contradiction network is an
unsolved engineering problem. Query performance near
densely contradicted areas of the graph may degrade severely.

**4. Automated contradiction detection**
This framework describes what happens when a contradiction
is detected. It does not specify how contradictions are
detected automatically. Currently, detection depends on
the verifier model (which can hallucinate) and adversarial
collaboration (which requires two instances to disagree).
Systematic contradiction detection across a large graph
requires semantic comparison of all node pairs — which is
computationally intractable at scale. A practical automated
detection approach is undefined.

**5. Meta-contradiction**
What if the contradiction resolution procedure itself produces
a contradiction? Two instances using Pathway 3 (adversarial
debate) may reach opposite conclusions about the same
CONTRADICTS pair. The framework does not currently define
a procedure for meta-level contradictions about the outcome
of contradiction resolution.

---

*This framework addresses LIMITATIONS.md §6.*
*Contributions to contradiction resolution are especially welcome.*
*See CONTRIBUTING.md §3 — Contradiction resolution.*
*Candidate frameworks: Dempster-Shafer, Bayesian networks,*
*paraconsistent logic.*

*Sapien — AGPLv3 — 28 May 2026*
*Author: Aarav — A Solo Engineer*
