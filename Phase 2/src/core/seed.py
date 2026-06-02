"""
SEED node creation and management.

From AXIOMATIC_FLOOR.md and DIDACTIC_SPEC.md §5:
- SEED nodes represent isolated new domains with no connections to existing graph
- They require bridge knowledge (WHY chain) to integrate into graph
- Transition to PENDING when partial connections are made
"""

from datetime import datetime
from uuid import uuid4

from graph.dag import DAG
from graph.schema import Node, NodeStatus, Provenance, WhyStep


def create_seed_node(
    label: str,
    statement: str,
    episode_id: str,
    teacher_id: str = "teacher",
    subtopic: str = "discovered",
) -> Node:
    """
    Create a new SEED node.
    
    From AXIOMATIC_FLOOR.md §3: SEED nodes are isolated new domains
    with no connections yet. They will be integrated through WHY chains.
    """
    return Node(
        concept_id=str(uuid4()),
        version=1,
        label=label,
        status=NodeStatus.SEED,
        statement=statement,
        why_chain=[],  # SEED nodes have no WHY chain initially
        provenance=Provenance(
            teacher_id=teacher_id,
            episode_id=episode_id,
            subtopic=subtopic,
            generation=0,
        ),
        uncertainty=1.0,  # Maximum uncertainty for new domain
        reward_signal=1.0,  # Maximum reward for genuine discovery
        is_floor_node=False,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def create_floor_node(
    label: str,
    statement: str,
    category: str = "A",  # Category A: physical constants/fundamental laws
) -> Node:
    """
    Create an axiomatic floor node.
    
    From AXIOMATIC_FLOOR.md §3 & §6:
    - Floor nodes terminate WHY chains
    - They have empty why_chain, status=KNOWN, floor=true
    - They are treated as foundational without further justification
    """
    return Node(
        concept_id=str(uuid4()),
        version=1,
        label=label,
        status=NodeStatus.KNOWN,
        statement=statement,
        why_chain=[],  # Floor nodes always have empty why chain
        provenance=Provenance(
            teacher_id="system",
            episode_id="floor-initialization",
            subtopic=f"floor-category-{category}",
            generation=0,
        ),
        uncertainty=0.0,  # Floor nodes have zero uncertainty
        reward_signal=0.0,  # No reward for floor nodes
        is_floor_node=True,  # Explicitly marked as floor node
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


def initialize_floor_nodes(dag: DAG, episode_id: str):
    """
    Initialize basic axiomatic floor nodes.
    
    From AXIOMATIC_FLOOR.md §5: Category A - Physical constants and fundamental laws
    This is a minimal set for the MVP prototype.
    """
    floor_concepts = [
        ("causality", "Events have causes; causal chains are foundational to reasoning"),
        ("logic", "The laws of logic (identity, non-contradiction, excluded middle) are foundational"),
        ("set membership", "An object either belongs to a set or it does not"),
        ("empirical observation", "Direct observation of phenomena is a valid epistemological ground"),
    ]
    
    for label, statement in floor_concepts:
        node = create_floor_node(label, statement)
        dag.add_node(node)
