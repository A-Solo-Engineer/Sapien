"""
Epistemic state management for the didactic episode.

Tracks Known Knowns (KK), Known Unknowns (KU), SEED nodes (S), and PENDING nodes (P).
Implements state transition logic from DIDACTIC_SPEC.md.
"""

from typing import Set, List
from dataclasses import dataclass, field
from uuid import uuid4

from graph.dag import DAG
from graph.schema import Node, NodeStatus


@dataclass
class EpistemicState:
    """
    Represents the epistemic state at a point in the episode.
    
    From DIDACTIC_SPEC.md §4:
    - KK (Known Knowns): concepts with complete WHY chains
    - KU (Known Unknowns): gaps identified with questions pending
    - S (SEED): isolated new domains with no connections
    - P (PENDING): SEED nodes with partial connections
    """
    
    kk: Set[str] = field(default_factory=set)  # concept_ids
    ku: Set[str] = field(default_factory=set)
    s: Set[str] = field(default_factory=set)
    p: Set[str] = field(default_factory=set)

    def __str__(self) -> str:
        return (
            f"EpistemicState(\n"
            f"  KK (Known Knowns): {len(self.kk)} nodes\n"
            f"  KU (Known Unknowns): {len(self.ku)} nodes\n"
            f"  S (SEED): {len(self.s)} nodes\n"
            f"  P (PENDING): {len(self.p)} nodes\n"
            f")"
        )

    def is_closure_reached(self) -> bool:
        """
        Check if epistemic closure is reached.
        From DIDACTIC_SPEC.md §7: closure when all gaps are filled.
        Gaps include: KU (Known Unknowns), S (SEED), P (PENDING)
        """
        # All gaps must be addressed for closure
        all_gaps_empty = (len(self.ku) == 0 and len(self.s) == 0 and len(self.p) == 0)
        return all_gaps_empty


class EpistemicStateManager:
    """Manages epistemic state transitions during an episode."""

    def __init__(self, dag: DAG):
        """Initialize with a knowledge graph."""
        self.dag = dag
        self.state = EpistemicState()

    def initialize_from_graph(self):
        """Initialize state from current graph."""
        self.state.kk = set()
        self.state.ku = set()
        self.state.s = set()
        self.state.p = set()

        for node in self.dag.get_all_nodes():
            if node.status == NodeStatus.KNOWN:
                self.state.kk.add(node.concept_id)
            elif node.status == NodeStatus.KNOWN_UNKNOWN:
                self.state.ku.add(node.concept_id)
            elif node.status == NodeStatus.SEED:
                self.state.s.add(node.concept_id)
            elif node.status == NodeStatus.PENDING:
                self.state.p.add(node.concept_id)

    def mark_as_known(self, concept_id: str):
        """Transition a node to KNOWN status."""
        # Remove from other sets
        self.state.ku.discard(concept_id)
        self.state.s.discard(concept_id)
        self.state.p.discard(concept_id)
        
        # Add to KK
        self.state.kk.add(concept_id)
        
        # Update database
        self.dag.update_node_status(concept_id, NodeStatus.KNOWN)

    def mark_as_known_unknown(self, concept_id: str):
        """Transition a node to KNOWN_UNKNOWN status."""
        self.state.s.discard(concept_id)
        self.state.kk.discard(concept_id)
        self.state.p.discard(concept_id)
        
        self.state.ku.add(concept_id)
        self.dag.update_node_status(concept_id, NodeStatus.KNOWN_UNKNOWN)

    def mark_as_seed(self, concept_id: str):
        """Transition a node to SEED status."""
        self.state.kk.discard(concept_id)
        self.state.ku.discard(concept_id)
        self.state.p.discard(concept_id)
        
        self.state.s.add(concept_id)
        self.dag.update_node_status(concept_id, NodeStatus.SEED)

    def mark_as_pending(self, concept_id: str):
        """Transition a node to PENDING status."""
        self.state.kk.discard(concept_id)
        self.state.ku.discard(concept_id)
        self.state.s.discard(concept_id)
        
        self.state.p.add(concept_id)
        self.dag.update_node_status(concept_id, NodeStatus.PENDING)

    def get_state(self) -> EpistemicState:
        """Get current epistemic state."""
        return self.state

    def get_gaps_to_address(self) -> List[str]:
        """Get concept_ids of gaps to address (KU + S + P)."""
        return list(self.state.ku | self.state.s | self.state.p)

    def get_known_concepts(self) -> List[str]:
        """Get all KNOWN concept_ids."""
        return list(self.state.kk)

    def summarize(self) -> str:
        """Get a summary of current epistemic state."""
        total_gaps = len(self.state.ku) + len(self.state.s) + len(self.state.p)
        total_known = len(self.state.kk)
        total = total_gaps + total_known
        
        summary = (
            f"\n=== EPISTEMIC STATE ===\n"
            f"Total nodes: {total}\n"
            f"Known: {total_known}\n"
            f"Gaps remaining: {total_gaps}\n"
            f"  - Known Unknowns (KU): {len(self.state.ku)}\n"
            f"  - SEED nodes (S): {len(self.state.s)}\n"
            f"  - PENDING nodes (P): {len(self.state.p)}\n"
            f"Epistemic closure reached: {self.state.is_closure_reached()}\n"
        )
        return summary
