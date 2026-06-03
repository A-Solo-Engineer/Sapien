"""
Learner agent implementation.

From DIDACTIC_SPEC.md §3:
Learner agent L maintains a knowledge graph G and knowledge gap map.
Must be capable of:
- Evaluating whether a chunk connects to existing graph
- Generating questions that point to genuine gaps
- Committing new nodes and edges to graph
- Computing the Known Unknowns set at any moment
"""

from typing import List, Dict, Optional, Tuple
from uuid import uuid4
from datetime import datetime

from graph.dag import DAG
from graph.schema import Node, NodeStatus, Edge, RelationType, Provenance
from episode.state import EpistemicStateManager
from core.seed import create_seed_node, create_floor_node
from core.why_chain import build_why_chain_from_response, add_why_chain_to_node
from agents.teacher import Chunk, TeacherResponse


class Learner:
    """Learner agent that maintains and updates the knowledge graph."""
    
    def __init__(self, episode_id: str, dag: DAG, topic: str = "unknown"):
        """Initialize learner with a DAG and episode context."""
        self.episode_id = episode_id
        self.dag = dag
        self.topic = topic
        self.state_manager = EpistemicStateManager(dag)
        self.state_manager.initialize_from_graph()
        self.question_counter = 0
    
    def receive_chunk(self, chunk: Chunk) -> Tuple[bool, Optional[str]]:
        """
        Evaluate whether a chunk connects to existing graph.
        
        From DIDACTIC_SPEC.md §6:
        Returns (connected, concept_id or gap_description)
        """
        # Try to find relevant nodes in graph by label similarity
        matching_nodes = self.dag.find_nodes_by_label(chunk.subtopic)
        
        if matching_nodes:
            # Connection found
            for node in matching_nodes:
                if node.status == NodeStatus.KNOWN:
                    # Direct connection to known concept
                    return (True, node.concept_id)
        
        # Check if chunk content matches any existing KNOWN_UNKNOWN nodes
        for ku_id in self.state_manager.state.ku:
            ku_node = self.dag.get_node(ku_id)
            if ku_node and chunk.subtopic.lower() in ku_node.label.lower():
                # This chunk might answer a known gap
                return (True, ku_id)
        
        # No connection found - this is a gap or new domain
        return (False, chunk.subtopic)
    
    def create_node_from_chunk(
        self,
        chunk: Chunk,
        teacher_id: str = "teacher",
    ) -> str:
        """
        Create a node in the graph from teacher's chunk.
        
        Chunks from teacher are KNOWN_UNKNOWN (we know they matter, we don't understand them yet).
        SEED nodes are created later when we discover genuinely new domains through questioning.
        """
        # Chunks from teacher represent gaps we need to address
        # They start as KNOWN_UNKNOWN (identified gaps, not yet understood)
        node = Node(
            label=chunk.subtopic,
            statement=chunk.content[:200],  # Truncate for storage
            status=NodeStatus.KNOWN_UNKNOWN,
            provenance=Provenance(
                teacher_id=teacher_id,
                episode_id=self.episode_id,
                subtopic=chunk.subtopic,
                generation=0,
            ),
            uncertainty=0.7,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        concept_id = self.dag.add_node(node)
        
        # Update epistemic state
        self.state_manager.mark_as_known_unknown(concept_id)
        
        return concept_id
    
    def generate_question(self) -> Optional[str]:
        """
        Generate a question from a gap in the knowledge graph.
        
        From DIDACTIC_SPEC.md §9: must point to genuine gap.
        Returns None if no gaps exist (epistemic closure).
        """
        # Get gaps to address (KU, S, P)
        gaps = self.state_manager.get_gaps_to_address()
        
        if not gaps:
            return None  # No gaps - closure reached
        
        # Pick first gap (simple strategy)
        gap_id = gaps[0]
        gap_node = self.dag.get_node(gap_id)
        
        if gap_node:
            self.question_counter += 1
            suffix = f" (q{self.question_counter})"
            
            # Generate varied questions based on epistemic status
            if gap_node.status == NodeStatus.KNOWN_UNKNOWN:
                # Already identified gap - ask for deeper understanding
                statement_preview = gap_node.statement[:100] if gap_node.statement else "this concept"
                question = f"Why does {gap_node.label} work the way it does? Specifically: {statement_preview}{suffix}"
            elif gap_node.status == NodeStatus.SEED:
                # New domain discovered - ask what it is
                question = f"What is {gap_node.label} and how does it connect to {self.topic}?{suffix}"
            elif gap_node.status == NodeStatus.PENDING:
                # Partially connected - ask about relations
                question = f"How does {gap_node.label} relate to the concepts already learned?{suffix}"
            else:
                # Default fallback
                question = f"What is the detailed explanation of {gap_node.label}?{suffix}"
            
            return question
        
        return None
    
    def integrate_answer(
        self,
        question: str,
        response: TeacherResponse,
        gap_node_id: str,
    ) -> str:
        """
        Integrate teacher's answer into the knowledge graph.
        
        Creates nodes for new concepts and edges between them.
        Builds WHY chain and transitions node status.
        """
        # Build WHY chain from response
        why_chain = build_why_chain_from_response(
            response.answer,
            response.why_chain,
            self.episode_id,
        )
        
        # Get the gap node and add why chain
        gap_node = self.dag.get_node(gap_node_id)
        if gap_node:
            gap_node = add_why_chain_to_node(gap_node, why_chain)
            gap_node.uncertainty = 1.0 - response.confidence  # Invert for uncertainty
            
            # Update the WHY chain in the database
            self.dag.update_node_why_chain(gap_node_id, why_chain)
            
            # Create new nodes for concepts mentioned in answer
            concept_ids = {}
            for concept_label in response.new_concepts:
                new_node = Node(
                    label=concept_label,
                    statement=f"Concept from {question}",
                    status=NodeStatus.KNOWN,
                    provenance=Provenance(
                        teacher_id="teacher",
                        episode_id=self.episode_id,
                        subtopic="answer_integration",
                        generation=0,
                    ),
                    uncertainty=response.confidence,
                )
                new_concept_id = self.dag.add_node(new_node)
                concept_ids[concept_label] = new_concept_id
                self.state_manager.mark_as_known(new_concept_id)
            
            # Create edges from gap to new concepts
            for concept_label, concept_id in concept_ids.items():
                edge = Edge(
                    source_id=gap_node_id,
                    target_id=concept_id,
                    relation=RelationType.USED_IN,
                    strength=response.confidence,
                    established_in=self.episode_id,
                )
                self.dag.add_edge(edge)
            
            # Transition gap node to KNOWN
            self.state_manager.mark_as_known(gap_node_id)
        
        return gap_node_id
    
    def get_current_gaps(self) -> List[str]:
        """Get list of current gap node IDs."""
        return self.state_manager.get_gaps_to_address()
    
    def get_epistemic_state_summary(self) -> str:
        """Get summary of current epistemic state."""
        return self.state_manager.summarize()
