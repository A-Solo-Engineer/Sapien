"""
WHY chain construction and validation.

From SCHEMA_SPEC.md §3 and DIDACTIC_SPEC.md:
- WHY chains are ordered sequences of causal steps
- Each step has a claim, source, and certainty value
- Chains terminate at floor nodes (axiomatic floor)
- Used to establish complete understanding (KNOWN status)
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import uuid4

from graph.dag import DAG
from graph.schema import Node, NodeStatus, WhyStep, Edge, RelationType, Provenance


def create_why_step(
    step_number: int,
    claim: str,
    source: str,
    certainty: float = 0.9,
) -> WhyStep:
    """Create a single step in a WHY chain."""
    if not (0.0 <= certainty <= 1.0):
        raise ValueError("Certainty must be between 0.0 and 1.0")
    
    return WhyStep(
        step=step_number,
        claim=claim,
        source=source,
        certainty=certainty,
    )


def build_why_chain_from_response(
    response_text: str,
    steps_list: List[Dict[str, Any]],
    episode_id: str,
    teacher_id: str = "teacher",
) -> List[WhyStep]:
    """
    Build a WHY chain from teacher response.
    
    Each step should be a dict with:
    - claim: the causal statement
    - source: where this came from
    - certainty: confidence (0.0-1.0)
    """
    why_chain = []
    
    for i, step_dict in enumerate(steps_list, start=1):
        step = create_why_step(
            step_number=i,
            claim=step_dict.get("claim", ""),
            source=step_dict.get("source", f"{teacher_id}-{episode_id}"),
            certainty=float(step_dict.get("certainty", 0.9)),
        )
        why_chain.append(step)
    
    return why_chain


def compute_why_chain_depth(node: Node) -> int:
    """Get the depth of a node's WHY chain."""
    if node.is_floor_node:
        return 0
    return len(node.why_chain)


def is_deep_why_chain(node: Node, threshold: int = 3) -> bool:
    """
    Check if WHY chain is "deep" (exceeds threshold).
    
    From REWARD_SPEC.md: D_deep = 3 (minimum for deep explanation)
    A deep WHY chain indicates causal understanding, not just surface facts.
    """
    return compute_why_chain_depth(node) >= threshold


def compute_aggregate_certainty(node: Node) -> float:
    """
    Compute aggregate certainty from WHY chain steps.
    
    Simple approach: minimum certainty in the chain
    (chain is only as strong as its weakest link)
    """
    if not node.why_chain or node.is_floor_node:
        return node.uncertainty
    
    min_certainty = min(step.certainty for step in node.why_chain)
    return min_certainty


def add_why_chain_to_node(node: Node, why_chain: List[WhyStep]) -> Node:
    """Add a WHY chain to a node and update its uncertainty."""
    node.why_chain = why_chain
    node.uncertainty = compute_aggregate_certainty(node)
    return node


def validate_why_chain(why_chain: List[WhyStep]) -> bool:
    """
    Validate a WHY chain for structural integrity.
    
    Checks:
    - Non-empty (if not floor node)
    - Steps are ordered (1, 2, 3, ...)
    - All certainties are valid (0.0-1.0)
    """
    if not why_chain:
        return True  # Empty chain is valid for floor nodes
    
    for i, step in enumerate(why_chain, start=1):
        if step.step != i:
            return False  # Steps must be consecutive
        if not (0.0 <= step.certainty <= 1.0):
            return False  # Invalid certainty value
    
    return True


def trace_why_chain(dag: DAG, node: Node, max_depth: int = 10) -> List[Node]:
    """
    Trace a complete WHY chain by following CAUSES edges.
    
    Returns ordered list of nodes from deepest explanation back to original node.
    Stops at floor nodes or max depth.
    """
    chain = [node]
    visited = {node.concept_id}
    current_depth = 0
    
    # For now, we trace by edges. In practice, traverse through why_chain references.
    edges = dag.get_edges_to(node.concept_id)
    causes_edges = [e for e in edges if e.relation == RelationType.CAUSES]
    
    for edge in causes_edges[:1]:  # Take first cause for now
        source_node = dag.get_node(edge.source_id)
        if source_node and source_node.is_floor_node:
            chain.append(source_node)
            break
        elif source_node and source_node.concept_id not in visited and current_depth < max_depth:
            chain.append(source_node)
            visited.add(source_node.concept_id)
            current_depth += 1
    
    return chain


def get_why_chain_summary(node: Node) -> str:
    """Get a human-readable summary of a node's WHY chain."""
    if node.is_floor_node:
        return f"[Floor Node] {node.label}"
    
    if not node.why_chain:
        return f"[No WHY chain] {node.label}"
    
    summary = f"{node.label}:\n"
    for step in node.why_chain:
        summary += f"  Step {step.step} (certainty: {step.certainty:.1%}): {step.claim}\n"
    
    return summary
