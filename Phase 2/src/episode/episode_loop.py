"""
Didactic Episode Loop implementation.

From DIDACTIC_SPEC.md §5-6:
Implements the main loop of a didactic episode:
- Initialize state
- Receive chunks from teacher
- Generate questions from gaps
- Integrate answers
- Detect epistemic closure
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
import json

from graph.dag import DAG
from graph.schema import NodeStatus
from agents.teacher import TeacherInterface
from agents.learner import Learner
from core.seed import initialize_floor_nodes
from core.why_chain import is_deep_why_chain, compute_why_chain_depth


@dataclass
class EpisodeConfig:
    """Configuration for a didactic episode."""
    topic: str
    domain: str = "general"
    max_iterations: int = 20
    max_questions: int = 10
    require_deep_chains: bool = False  # Require depth >= 3


@dataclass
class EpisodeLog:
    """Log entry for episode execution."""
    timestamp: datetime
    event: str
    details: dict
    
    def __str__(self) -> str:
        return f"[{self.timestamp.isoformat()}] {self.event}: {json.dumps(self.details, default=str)}"


class DidacticEpisode:
    """
    Main didactic episode orchestrator.
    
    From DIDACTIC_SPEC.md:
    E = ⟨ τ, T, L, V, H, G₀, Δ ⟩
    Where:
    - τ: topic
    - T: teacher agent
    - L: learner agent
    - V: verifier (not implemented in MVP)
    - H: human supervisor (not implemented in MVP)
    - G₀: initial graph
    - Δ: transition function
    """
    
    def __init__(
        self,
        config: EpisodeConfig,
        teacher: TeacherInterface,
        dag: DAG,
    ):
        """Initialize episode."""
        self.config = config
        self.teacher = teacher
        self.dag = dag
        self.episode_id = str(uuid4())
        self.learner = Learner(self.episode_id, dag, config.topic)
        self.logs: List[EpisodeLog] = []
        self.question_count = 0
        self.iteration_count = 0
    
    def _log(self, event: str, details: dict = None):
        """Log an episode event."""
        if details is None:
            details = {}
        log = EpisodeLog(datetime.now(), event, details)
        self.logs.append(log)
        print(f"  {log}")
    
    def initialize(self):
        """
        Initialize episode.
        
        From DIDACTIC_SPEC.md §6: initialization steps.
        """
        self._log("episode_started", {"episode_id": self.episode_id, "topic": self.config.topic})
        
        # Initialize floor nodes (axiomatic floor)
        initialize_floor_nodes(self.dag, self.episode_id)
        self._log("floor_initialized", {"floor_nodes": 4})
        
        # Get initial chunks from teacher
        chunks = self.teacher.initialize_topic(self.config.topic, self.config.domain)
        self._log("chunks_received", {"chunk_count": len(chunks)})
        
        # Process each chunk
        for chunk in chunks:
            concept_id = self.learner.create_node_from_chunk(chunk)
            self._log("chunk_processed", {
                "subtopic": chunk.subtopic,
                "concept_id": concept_id,
            })
        
        # Print initial state
        print("\n" + self.learner.get_epistemic_state_summary())
    
    def run(self) -> bool:
        """
        Execute the main episode loop.
        
        From DIDACTIC_SPEC.md §6: while KU ≠ ∅ or chunks remain
        Returns True if episodic closure reached, False if max iterations exceeded.
        """
        print(f"\n=== STARTING DIDACTIC EPISODE ===")
        print(f"Topic: {self.config.topic}")
        print(f"Max iterations: {self.config.max_iterations}")
        print(f"Max questions: {self.config.max_questions}\n")
        
        self.initialize()
        
        print(f"\n=== MAIN EPISODE LOOP ===\n")
        
        # Main loop
        while self.iteration_count < self.config.max_iterations:
            self.iteration_count += 1
            print(f"\n--- Iteration {self.iteration_count} ---")
            
            # Check for epistemic closure
            if self.learner.state_manager.state.is_closure_reached():
                self._log("epistemic_closure", {"iteration": self.iteration_count})
                print(f"\n✓ EPISTEMIC CLOSURE REACHED")
                return True
            
            # Generate question from gap
            question = self.learner.generate_question()
            if not question:
                self._log("no_gaps", {"iteration": self.iteration_count})
                print("No gaps remaining")
                break
            
            # Check question limit
            if self.question_count >= self.config.max_questions:
                self._log("question_limit_reached", {"question_count": self.question_count})
                print(f"Question limit ({self.config.max_questions}) reached")
                break
            
            self.question_count += 1
            self._log("question_generated", {
                "question": question[:100],
                "question_num": self.question_count,
            })
            print(f"Question {self.question_count}: {question}")
            
            # Get answer from teacher
            response = self.teacher.answer_question(question)
            self._log("answer_received", {
                "confidence": response.confidence,
                "why_chain_length": len(response.why_chain),
            })
            print(f"Answer confidence: {response.confidence:.1%}")
            print(f"WHY chain length: {len(response.why_chain)} steps")
            
            # Get gap node and integrate answer
            gaps = self.learner.get_current_gaps()
            if gaps:
                gap_id = gaps[0]
                integrated_id = self.learner.integrate_answer(question, response, gap_id)
                
                gap_node = self.dag.get_node(integrated_id)
                if gap_node:
                    self._log("answer_integrated", {
                        "concept_id": integrated_id,
                        "why_chain_depth": compute_why_chain_depth(gap_node),
                        "is_deep": is_deep_why_chain(gap_node),
                    })
                    print(f"✓ Answer integrated into node {integrated_id}")
                    print(f"  WHY chain depth: {compute_why_chain_depth(gap_node)}")
            
            # Print current state
            print(self.learner.get_epistemic_state_summary())
        
        # Episode terminated without closure
        self._log("episode_terminated", {
            "iteration": self.iteration_count,
            "reason": "max_iterations",
        })
        print(f"\n✗ Episode terminated (max iterations reached)")
        return False
    
    def get_summary(self) -> dict:
        """Get final episode summary."""
        gap_count = len(self.learner.get_current_gaps())
        known_count = len(self.learner.state_manager.state.kk)
        
        return {
            "episode_id": self.episode_id,
            "topic": self.config.topic,
            "total_iterations": self.iteration_count,
            "total_questions": self.question_count,
            "total_nodes": len(self.dag.get_all_nodes()),
            "known_concepts": known_count,
            "remaining_gaps": gap_count,
            "closure_reached": gap_count == 0,
            "events_logged": len(self.logs),
        }
    
    def print_summary(self):
        """Print episode summary."""
        summary = self.get_summary()
        print(f"\n=== EPISODE SUMMARY ===")
        print(f"Episode ID: {summary['episode_id']}")
        print(f"Topic: {summary['topic']}")
        print(f"Iterations: {summary['total_iterations']}/{self.config.max_iterations}")
        print(f"Questions: {summary['total_questions']}/{self.config.max_questions}")
        print(f"Total nodes: {summary['total_nodes']}")
        print(f"Known concepts: {summary['known_concepts']}")
        print(f"Remaining gaps: {summary['remaining_gaps']}")
        print(f"Closure reached: {summary['closure_reached']}")
        print(f"Events logged: {summary['events_logged']}")
