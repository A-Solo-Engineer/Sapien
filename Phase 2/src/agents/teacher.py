"""
Teacher agent interface.

From DIDACTIC_SPEC.md §3:
Teacher agent T is a generative model with access to a knowledge domain.
In Generation 0, T is a frontier LLM.
Must be capable of:
- Presenting conceptual material as bounded chunks
- Answering questions with responses that include WHY chains
- Partitioning a topic into an ordered sequence of chunks
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod


@dataclass
class Chunk:
    """A bounded piece of conceptual material from the teacher."""
    content: str  # The actual content
    topic: str  # What topic does this cover
    subtopic: str  # More specific subtopic
    prerequisites: List[str] = None  # Concept IDs of prerequisites
    difficulty: float = 0.5  # 0.0 (easiest) to 1.0 (hardest)
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []


@dataclass
class TeacherResponse:
    """Response from teacher to a question."""
    answer: str  # The answer text
    why_chain: List[Dict[str, Any]]  # Steps: [{"claim": str, "source": str, "certainty": float}]
    confidence: float  # Overall confidence in answer (0.0-1.0)
    new_concepts: List[str] = None  # Concepts introduced in answer
    
    def __post_init__(self):
        if self.new_concepts is None:
            self.new_concepts = []


class TeacherInterface(ABC):
    """Abstract base class for teacher agents."""
    
    @abstractmethod
    def initialize_topic(self, topic: str, domain: str = "general") -> List[Chunk]:
        """
        Partition a topic into an ordered sequence of chunks.
        
        Returns list of Chunks ordered by logical progression.
        """
        pass
    
    @abstractmethod
    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> TeacherResponse:
        """
        Answer a question with WHY chain.
        
        Args:
            question: The learner's question
            context: Optional context about the learning state
        
        Returns:
            TeacherResponse with answer and why_chain
        """
        pass
    
    @abstractmethod
    def explain_concept(self, concept: str) -> Dict[str, Any]:
        """
        Explain a single concept in detail.
        
        Returns dict with:
        - definition: plain language definition
        - why_chain: causal explanation
        - examples: 1-3 concrete examples
        """
        pass


class DefaultTeacher(TeacherInterface):
    """Default teacher stub for MVP testing (returns hardcoded responses)."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize default teacher stub."""
        self.call_count = 0
        self.api_key = api_key
    
    def initialize_topic(self, topic: str, domain: str = "general") -> List[Chunk]:
        """Return mock chunks for topic."""
        return [
            Chunk(
                content=f"Introduction to {topic}",
                topic=topic,
                subtopic="foundational concepts",
                difficulty=0.2,
            ),
            Chunk(
                content=f"Core mechanisms of {topic}",
                topic=topic,
                subtopic="mechanisms",
                prerequisites=[],
                difficulty=0.5,
            ),
            Chunk(
                content=f"Advanced applications of {topic}",
                topic=topic,
                subtopic="applications",
                prerequisites=["mechanisms"],
                difficulty=0.8,
            ),
        ]
    
    def answer_question(self, question: str, context: Optional[Dict[str, Any]] = None) -> TeacherResponse:
        """Return mock answer with why chain."""
        self.call_count += 1
        
        return TeacherResponse(
            answer=f"This is a mock answer to: {question}",
            why_chain=[
                {
                    "claim": "The question addresses a conceptual gap in understanding",
                    "source": "question_analysis",
                    "certainty": 0.95,
                },
                {
                    "claim": "The answer provides direct explanation",
                    "source": "knowledge_base",
                    "certainty": 0.9,
                },
                {
                    "claim": "The explanation connects to foundational concepts",
                    "source": "causal_inference",
                    "certainty": 0.85,
                },
            ],
            confidence=0.9,
            new_concepts=[f"concept_{self.call_count}"],
        )
    
    def explain_concept(self, concept: str) -> Dict[str, Any]:
        """Return mock concept explanation."""
        return {
            "definition": f"Definition of {concept}",
            "why_chain": [
                {"claim": f"{concept} is important because...", "certainty": 0.9}
            ],
            "examples": [
                f"Example 1 of {concept}",
                f"Example 2 of {concept}",
            ],
        }
