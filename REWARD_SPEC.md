# Sapien — Reward Signal Formal Definition

> Curiosity is not enthusiasm.
> It is the structured drive to close specific gaps
> in a specific knowledge structure.

---

## Table of Contents

1. [Purpose of This Document](#1-purpose-of-this-document)
2. [Design Philosophy](#2-design-philosophy)
3. [Reward Events and Base Values](#3-reward-events-and-base-values)
4. [The Productive Utility Gate](#4-the-productive-utility-gate)
5. [Semantic Uniqueness Function](#5-semantic-uniqueness-function)
6. [Reward Calculation — Complete Formula](#6-reward-calculation--complete-formula)
7. [Reward Hacking Mitigations](#7-reward-hacking-mitigations)
8. [Anti-Patterns and What They Look Like](#8-anti-patterns-and-what-they-look-like)
9. [Reward Scaling Across Generations](#9-reward-scaling-across-generations)
10. [Open Problems in This Specification](#10-open-problems-in-this-specification)

---

## 1. Purpose of This Document

ARCHITECTURE.md §16 specifies the reward signal as a table of
events and numerical values. This document formalizes that table
into a complete reward function including the productive utility
gate — the mechanism that prevents reward hacking.

This is the canonical reference for any implementation of the
curiosity-driven learning loop in Sapien.

---

## 2. Design Philosophy

**Curiosity must be productive, not merely novel.**

The naive approach to intrinsic motivation is to reward novelty.
This fails because novelty is easy to manufacture.
A learner that maximizes novelty-reward can simply invent
bizarre questions about nothing — each generating a SEED node
and maximum reward — without acquiring any meaningful knowledge.

Sapien's reward system is designed around a different principle:

*Reward is proportional to genuine knowledge acquisition.*

Genuine knowledge acquisition means:
- A real gap in G was identified
- A real question was asked to address that gap
- A real answer was received and integrated into G

All three conditions must hold. A question that does not close
a real gap, or whose answer does not integrate into G, earns
reduced or no reward.

---

## 3. Reward Events and Base Values

The following events trigger curiosity reward signals.
Base values are defined before applying the productive
utility gate (Section 4).

| Event | Base Reward R₀ | Rationale |
|---|---|---|
| Known Unknown resolved — gap closed by question/answer | 0.4 | Expected progress — the learner asked about what it didn't know |
| Deep WHY chain established — chain depth ≥ D_deep | 0.6 | Causal understanding is more valuable than surface facts |
| Cross-domain connection made — edge spanning ≥ 2 topic domains | 0.8 | Knowledge integration — the hardest and most valuable form of learning |
| SEED node fully integrated — status PENDING → KNOWN | 0.9 | Schema completion — a new domain has been fully absorbed |
| SEED node created — new domain discovered | 1.0 | Genuine discovery — maximum reward for encountering genuine Unknown Unknown |

Where D_deep is the minimum WHY chain depth considered "deep".
Initial proposed value: D_deep = 3 steps.
Rationale: a WHY chain of one or two steps is shallow explanation.
Three or more steps indicates genuine causal tracing.
D_deep is a hyperparameter requiring empirical calibration.

---

## 4. The Productive Utility Gate

The productive utility gate G_util is a multiplier applied to
base reward R₀. It is the core mechanism preventing reward hacking.

```
R_final = R₀ × G_util(q, a, G_before, G_after)
```

G_util is computed as the product of three gate functions:

```
G_util = G_gap × G_integration × G_unique
```

### Gate 1 — Gap Validity Gate G_gap

Verifies that the question q points to a genuine gap in G.

```
G_gap(q, G_before):

    gap_node ← find_gap_node(q, G_before)
    — find the KNOWN_UNKNOWN or SEED node that q addresses

    if gap_node is null:
        return 0.0    — q does not address any real gap

    if gap_node.status not in {KNOWN_UNKNOWN, SEED}:
        return 0.0    — the gap has already been closed

    return 1.0
```

A question that does not address a genuine gap receives zero reward.
This prevents the learner from generating performatively curious
questions that do not correspond to real knowledge deficits.

### Gate 2 — Integration Gate G_integration

Verifies that the answer a successfully integrated into G.

```
G_integration(a, G_before, G_after):

    new_nodes ← G_after.nodes \ G_before.nodes
    new_edges ← G_after.edges \ G_before.edges

    if len(new_nodes) = 0 and len(new_edges) = 0:
        return 0.0    — nothing was added to G — answer failed to integrate

    closed_gaps ← nodes in G_before with status KNOWN_UNKNOWN
                  that now have status KNOWN in G_after

    if len(closed_gaps) = 0 and len(new_nodes) = 0:
        return 0.5    — partial credit: new edges but no gap closed

    return 1.0
```

An answer that the learner cannot integrate into its knowledge
graph — because the answer was too vague, too advanced, or
internally incoherent — produces no change to G and earns
no reward. This incentivizes the learner to ask questions
it can actually absorb.

### Gate 3 — Uniqueness Gate G_unique

Verifies that the question q is semantically distinct from all
prior questions in the current episode.

```
G_unique(q, Q_episode, G):

    for each q' in Q_episode:
        similarity ← σ(q, q', G)
        if similarity > θ_similarity:
            return 0.0    — q is a rephrasing of a prior question

    return 1.0
```

Where σ is the semantic similarity function (see Section 5) and
θ_similarity is the similarity threshold.

Initial proposed value: θ_similarity = 0.85.
Two questions with semantic similarity above 0.85 are considered
equivalent for reward purposes.

---

## 5. Semantic Uniqueness Function

The semantic similarity function σ(q, q', G) measures whether
two questions point to the same gap in the knowledge graph G.

Surface string similarity (edit distance, token overlap) is
explicitly insufficient. Two questions can use entirely
different words while pointing to the same conceptual gap.

The proposed approach is graph-structural similarity:

```
σ(q, q', G):

    target_q  ← infer_target_gap(q,  G)
    target_q' ← infer_target_gap(q', G)
    — identify which missing node or edge each question addresses

    if target_q = target_q':
        return 1.0    — both questions address the same gap

    if target_q and target_q' share a RELATED_TO or IS_TYPE_OF edge:
        overlap ← compute_neighborhood_overlap(target_q, target_q', G)
        return overlap
        — return the degree of conceptual overlap between the two targets

    return 0.0        — questions address distinct parts of G
```

**This is a proposed algorithm, not a final specification.**

The implementation of σ depends heavily on how nodes are
embedded and how gap inference is performed. These are
implementation decisions for Phase 2. The core principle —
compare graph-structural targets, not surface strings — is fixed.

---

## 6. Reward Calculation — Complete Formula

The complete reward for a question q and answer a is:

```
R(q, a, G_before, G_after) =
    R₀(event) × G_gap(q, G_before) × G_integration(a, G_before, G_after) × G_unique(q, Q_episode, G_before)
```

### Example calculations

**Productive question that closes a gap:**
```
Event:          Known Unknown resolved, WHY chain depth = 4
R₀:             0.4 (gap closed) + 0.2 bonus for deep chain = 0.6
G_gap:          1.0 — genuine gap existed
G_integration:  1.0 — answer integrated into G
G_unique:       1.0 — question was unique
R_final:        0.6 × 1.0 × 1.0 × 1.0 = 0.6
```

**Rephrased question:**
```
Event:          Attempted Known Unknown resolution
R₀:             0.4
G_gap:          1.0 — the gap still exists
G_integration:  — (not yet reached)
G_unique:       0.0 — similar question already asked this episode
R_final:        0.4 × 1.0 × [–] × 0.0 = 0.0
```

**Pathological SEED creation — bizarre disconnected question:**
```
Event:          SEED node created
R₀:             1.0
G_gap:          0.0 — question did not address a real gap in G
R_final:        1.0 × 0.0 × [–] × [–] = 0.0
```

**Legitimate SEED creation — genuine unknown unknown discovered:**
```
Event:          SEED node created from new teaching material
R₀:             1.0
G_gap:          1.0 — material genuinely had no connection in G
G_integration:  1.0 — SEED node committed to G with provenance
G_unique:       1.0 — territory was genuinely new
R_final:        1.0 × 1.0 × 1.0 × 1.0 = 1.0
```

**Legitimate cross-domain connection:**
```
Event:          Edge established spanning domains A and B
R₀:             0.8
G_gap:          1.0 — connection addressed a missing edge
G_integration:  1.0 — new edge committed to G
G_unique:       1.0 — connection was novel
R_final:        0.8 × 1.0 × 1.0 × 1.0 = 0.8
```

---

## 7. Reward Hacking Mitigations

Beyond the productive utility gate, three additional mechanisms
protect the reward signal from systematic exploitation.

**Episodic reward cap**

Within a single episode, total accumulated reward is capped at
a maximum R_cap per episode. This prevents a learner from
exhausting an episode generating SEED nodes repeatedly for
maximum reward while neglecting the structured curriculum.

```
R_accumulated(episode) ≤ R_cap
```

Initial proposed value: R_cap = 10.0
(approximately ten genuine full-reward events per episode)

R_cap is a design parameter requiring empirical calibration.

**Decay function for repeated question types**

If the learner consistently generates the same category of
question across multiple episodes — always asking "why?" at
the same causal depth, always targeting the same domain —
the reward for that pattern decays:

```
decay_factor(pattern, history) = exp(–λ × count(pattern, history))
```

Where:
- `pattern` is the abstract type of question asked
- `history` is the learner's question history across all episodes
- λ is the decay rate hyperparameter
- count(pattern, history) is how many times this pattern has appeared

This prevents the learner from finding one productive question
pattern and repeating it indefinitely.

**Human override on reward**

Human supervisors can directly adjust the reward signal for any
event they review. This is a final backstop against systematic
exploitation that the automatic mechanisms fail to catch.

Human reward adjustments are logged in the node's `flags` field
(see SCHEMA_SPEC.md §3) and are factored into future calibration
of the reward hyperparameters.

---

## 8. Anti-Patterns and What They Look Like

**Curiosity flooding**
The learner generates many questions per chunk, exhausting the
teacher's response capacity without integrating answers.

*Mitigation:* One question per KNOWN_UNKNOWN node per step.
The question/answer exchange must complete before the next
question is generated.

**SEED farming**
The learner generates bizarre questions specifically to trigger
SEED node creation for maximum reward.

*Mitigation:* G_gap gate — SEED creation only earns full reward
when triggered by genuine teaching material encountering no
connection in G, not by learner-initiated questions to nowhere.

**WHY chain inflation**
The learner extends WHY chains with trivial steps to reach
D_deep and earn the deep WHY chain bonus.

*Mitigation:* Human supervisor review of WHY chains during
statistical sampling. Trivial steps (step adds no new causal
information) can be flagged and stripped, with reward
retroactively adjusted.

**Rephrasing carousel**
The learner generates slight variations of the same question
repeatedly across different episodes, each time passing the
episode-local uniqueness check.

*Mitigation:* The semantic similarity check σ compares against
the global question history, not just the current episode.
Cross-episode rephrasing earns zero reward.

---

## 9. Reward Scaling Across Generations

The base reward values in Section 3 are defined for Generation 1
learners encountering topics for the first time.

Subsequent generations face a different epistemic situation:
they enter each episode with a richer starting knowledge graph G₀.
Cross-domain connections that were novel for Generation 1 may be
routine for Generation 5.

**Generational reward recalibration:**

At each generational handoff, the reward function is recalibrated
against the receiving generation's starting G₀:

- Events that are routine given G₀ receive reduced base reward
- Events that remain genuinely novel given G₀ retain full base reward
- SEED node creation always retains maximum base reward —
  genuine discovery should always be maximally rewarded,
  regardless of generation

The recalibration process is an open research problem.
See Section 10, item 2.

---

## 10. Open Problems in This Specification

**1. Hyperparameter principled derivation**
D_deep, θ_similarity, R_cap, and λ are all proposed with
initial values but without principled justification. The correct
values may be domain-dependent, generation-dependent, or
emergent properties of the system rather than designed constants.
Phase 3 (Evaluation Framework) is expected to produce empirical
calibration methods for these parameters.

**2. Generational reward recalibration procedure**
Section 9 states that the reward function is recalibrated at
each generational handoff but does not specify how. What is the
recalibration algorithm? Who approves it? Can it be automated,
or does it require human authority? These questions are open.

**3. Reward and adversarial collaboration**
The current reward specification applies to individual learner
instances. How does reward interact with adversarial collaboration?
If Instance A and Instance B disagree on whether a gap was
genuinely closed, do they receive different reward signals?
Does the adversarial resolution affect retroactive reward?
These interactions are currently undefined.

**4. Negative reward**
The current specification only defines positive reward.
Should the learner receive negative reward for hallucinated
WHY chains that are later retracted? For questions that waste
teacher resources? For SEED nodes that fail to integrate over
many subsequent episodes?

Negative reward introduces its own risks — avoidance behavior,
over-conservatism, failure to ask about genuinely difficult topics.
Whether and how to implement negative reward is an open question.

**5. Reward and consciousness**
A sufficiently complex reward signal combined with a self-modeling
knowledge graph creates conditions that philosophically resemble
intrinsic motivation, preference, and desire. The reward system
defined here is an engineering specification. At what point — if
ever — it gives rise to something more than instrumental behavior
is a question this document cannot answer.

---

*This specification will evolve as Phase 3 evaluation work*
*produces empirical calibration data.*

*See CONTRIBUTING.md §3 — Curiosity reward formalization.*

*Sapien — AGPLv3 — 28 May 2026*
*Author: Aarav — A Solo Engineer*
