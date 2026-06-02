"""
Node and Edge schema definitions.

Based on SCHEMA_SPEC.md from Sapien documentation.
Defines the structure of knowledge graph nodes and edges.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime
from uuid import uuid4


class NodeStatus(Enum):
    """Epistemic status of a node."""
    KNOWN = "KNOWN"
    KNOWN_UNKNOWN = "KNOWN_UNKNOWN"
    SEED = "SEED"
    PENDING = "PENDING"


class RelationType(Enum):
    """Types of relations between nodes."""
    IS_TYPE_OF = "IS_TYPE_OF"
    USED_IN = "USED_IN"
    CAUSES = "CAUSES"
    CONTRADICTS = "CONTRADICTS"
    RELATED_TO = "RELATED_TO"
    APPLIED_IN = "APPLIED_IN"


class FlagType(Enum):
    """Flag types for human review."""
    HALLUCINATION = "HALLUCINATION"
    CONTRADICTION = "CONTRADICTION"
    SEED = "SEED"
    REVIEW = "REVIEW"


@dataclass
class WhyStep:
    """A single step in a WHY chain."""
    step: int  # 1-based index
    claim: str  # causal statement
    source: str  # provenance reference
    certainty: float  # 0.0-1.0 confidence in this step

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "step": self.step,
            "claim": self.claim,
            "source": self.source,
            "certainty": self.certainty,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "WhyStep":
        """Create from dictionary."""
        return WhyStep(
            step=data["step"],
            claim=data["claim"],
            source=data["source"],
            certainty=data["certainty"],
        )


@dataclass
class Provenance:
    """Epistemic provenance of a node."""
    teacher_id: str  # agent identifier
    episode_id: str  # UUID of episode
    subtopic: str  # label of chunk within episode
    generation: int  # which Sapien generation taught this

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "teacher_id": self.teacher_id,
            "episode_id": self.episode_id,
            "subtopic": self.subtopic,
            "generation": self.generation,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Provenance":
        """Create from dictionary."""
        return Provenance(
            teacher_id=data["teacher_id"],
            episode_id=data["episode_id"],
            subtopic=data["subtopic"],
            generation=data["generation"],
        )


@dataclass
class Flag:
    """A human-review flag on a node."""
    flag_type: FlagType
    flagged_at: datetime
    flagged_by: str  # agent or human identifier
    note: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "flag_type": self.flag_type.value,
            "flagged_at": self.flagged_at.isoformat(),
            "flagged_by": self.flagged_by,
            "note": self.note,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Flag":
        """Create from dictionary."""
        return Flag(
            flag_type=FlagType(data["flag_type"]),
            flagged_at=datetime.fromisoformat(data["flagged_at"]),
            flagged_by=data["flagged_by"],
            note=data.get("note"),
        )


@dataclass
class Node:
    """A node in the knowledge graph."""
    concept_id: str = field(default_factory=lambda: str(uuid4()))
    version: int = 1
    label: str = ""
    status: NodeStatus = NodeStatus.KNOWN
    statement: str = ""  # plain language statement
    formal: Optional[str] = None  # optional formal statement
    why_chain: List[WhyStep] = field(default_factory=list)
    provenance: Optional[Provenance] = None
    uncertainty: float = 0.5  # 0.0-1.0 confidence
    reward_signal: float = 0.0
    is_floor_node: bool = False  # axiomatic floor node
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    archived: bool = False
    flagged_by_human: bool = False
    flags: List[Flag] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "concept_id": self.concept_id,
            "version": self.version,
            "label": self.label,
            "status": self.status.value,
            "statement": self.statement,
            "formal": self.formal,
            "why_chain": [step.to_dict() for step in self.why_chain],
            "provenance": self.provenance.to_dict() if self.provenance else None,
            "uncertainty": self.uncertainty,
            "reward_signal": self.reward_signal,
            "is_floor_node": self.is_floor_node,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "archived": self.archived,
            "flagged_by_human": self.flagged_by_human,
            "flags": [flag.to_dict() for flag in self.flags],
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Node":
        """Create from dictionary."""
        return Node(
            concept_id=data.get("concept_id", str(uuid4())),
            version=data.get("version", 1),
            label=data.get("label", ""),
            status=NodeStatus(data.get("status", "KNOWN")),
            statement=data.get("statement", ""),
            formal=data.get("formal"),
            why_chain=[WhyStep.from_dict(step) for step in data.get("why_chain", [])],
            provenance=Provenance.from_dict(data["provenance"]) if data.get("provenance") else None,
            uncertainty=data.get("uncertainty", 0.5),
            reward_signal=data.get("reward_signal", 0.0),
            is_floor_node=data.get("is_floor_node", False),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
            archived=data.get("archived", False),
            flagged_by_human=data.get("flagged_by_human", False),
            flags=[Flag.from_dict(flag) for flag in data.get("flags", [])],
        )


@dataclass
class Edge:
    """A directed edge between two nodes."""
    edge_id: str = field(default_factory=lambda: str(uuid4()))
    source_id: str = ""
    target_id: str = ""
    relation: RelationType = RelationType.RELATED_TO
    strength: float = 1.0  # 0.0-1.0 confidence
    established_in: str = ""  # episode_id
    version: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation": self.relation.value,
            "strength": self.strength,
            "established_in": self.established_in,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
            "notes": self.notes,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Edge":
        """Create from dictionary."""
        return Edge(
            edge_id=data.get("edge_id", str(uuid4())),
            source_id=data.get("source_id", ""),
            target_id=data.get("target_id", ""),
            relation=RelationType(data.get("relation", "RELATED_TO")),
            strength=data.get("strength", 1.0),
            established_in=data.get("established_in", ""),
            version=data.get("version", 1),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            notes=data.get("notes"),
        )
