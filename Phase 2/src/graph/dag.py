"""
DAG (Knowledge Graph) implementation using SQLite.

Implements persistent storage for nodes and edges as per SCHEMA_SPEC.md.
Provides query interface for episode state management.
"""

import sqlite3
import json
from pathlib import Path
from typing import List, Optional, Dict, Any, Set
from datetime import datetime
from uuid import uuid4

from .schema import Node, Edge, NodeStatus, RelationType, WhyStep, Provenance, Flag, FlagType


class DAG:
    """Directed Acyclic Graph for knowledge storage using SQLite."""

    def __init__(self, db_path: str = "knowledge_graph.db"):
        """Initialize DAG with SQLite backend."""
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    concept_id TEXT PRIMARY KEY,
                    version INTEGER,
                    label TEXT,
                    status TEXT,
                    statement TEXT,
                    formal TEXT,
                    why_chain TEXT,
                    provenance TEXT,
                    uncertainty REAL,
                    reward_signal REAL,
                    is_floor_node BOOLEAN,
                    created_at TEXT,
                    updated_at TEXT,
                    archived BOOLEAN,
                    flagged_by_human BOOLEAN,
                    flags TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    edge_id TEXT PRIMARY KEY,
                    source_id TEXT,
                    target_id TEXT,
                    relation TEXT,
                    strength REAL,
                    established_in TEXT,
                    version INTEGER,
                    created_at TEXT,
                    notes TEXT,
                    FOREIGN KEY(source_id) REFERENCES nodes(concept_id),
                    FOREIGN KEY(target_id) REFERENCES nodes(concept_id)
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_nodes_status ON nodes(status)
            """)
            conn.commit()

    def add_node(self, node: Node) -> str:
        """Add a node to the graph. Returns the concept_id."""
        if not node.provenance:
            raise ValueError("Node must have provenance information")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO nodes 
                (concept_id, version, label, status, statement, formal, why_chain,
                 provenance, uncertainty, reward_signal, is_floor_node, created_at,
                 updated_at, archived, flagged_by_human, flags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                node.concept_id,
                node.version,
                node.label,
                node.status.value,
                node.statement,
                node.formal,
                json.dumps([step.to_dict() for step in node.why_chain]),
                json.dumps(node.provenance.to_dict()) if node.provenance else None,
                node.uncertainty,
                node.reward_signal,
                node.is_floor_node,
                node.created_at.isoformat(),
                node.updated_at.isoformat(),
                node.archived,
                node.flagged_by_human,
                json.dumps([flag.to_dict() for flag in node.flags]),
            ))
            conn.commit()
        return node.concept_id

    def get_node(self, concept_id: str) -> Optional[Node]:
        """Retrieve a node by concept_id."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM nodes WHERE concept_id = ?", (concept_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_node(row)

    def update_node_status(self, concept_id: str, new_status: NodeStatus):
        """Update a node's status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE nodes SET status = ?, updated_at = ? WHERE concept_id = ?",
                (new_status.value, datetime.now().isoformat(), concept_id),
            )
            conn.commit()

    def add_edge(self, edge: Edge):
        """Add an edge to the graph."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO edges
                (edge_id, source_id, target_id, relation, strength,
                 established_in, version, created_at, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                edge.edge_id,
                edge.source_id,
                edge.target_id,
                edge.relation.value,
                edge.strength,
                edge.established_in,
                edge.version,
                edge.created_at.isoformat(),
                edge.notes,
            ))
            conn.commit()

    def get_edges_from(self, source_id: str) -> List[Edge]:
        """Get all edges originating from a node."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM edges WHERE source_id = ?", (source_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_edge(row) for row in rows]

    def get_edges_to(self, target_id: str) -> List[Edge]:
        """Get all edges pointing to a node."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM edges WHERE target_id = ?", (target_id,)
            )
            rows = cursor.fetchall()
            return [self._row_to_edge(row) for row in rows]

    def get_nodes_by_status(self, status: NodeStatus) -> List[Node]:
        """Get all nodes with a specific status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM nodes WHERE status = ?", (status.value,)
            )
            rows = cursor.fetchall()
            return [self._row_to_node(row) for row in rows]

    def get_all_nodes(self) -> List[Node]:
        """Get all nodes in the graph."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM nodes WHERE archived = 0")
            rows = cursor.fetchall()
            return [self._row_to_node(row) for row in rows]

    def get_all_edges(self) -> List[Edge]:
        """Get all edges in the graph."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM edges")
            rows = cursor.fetchall()
            return [self._row_to_edge(row) for row in rows]

    def _row_to_node(self, row: tuple) -> Node:
        """Convert database row to Node object."""
        (concept_id, version, label, status, statement, formal, why_chain,
         provenance, uncertainty, reward_signal, is_floor_node, created_at,
         updated_at, archived, flagged_by_human, flags) = row

        why_chain_list = [WhyStep.from_dict(step) for step in json.loads(why_chain or "[]")]
        prov = Provenance.from_dict(json.loads(provenance)) if provenance else None
        flags_list = [Flag.from_dict(flag) for flag in json.loads(flags or "[]")]

        return Node(
            concept_id=concept_id,
            version=version,
            label=label,
            status=NodeStatus(status),
            statement=statement,
            formal=formal,
            why_chain=why_chain_list,
            provenance=prov,
            uncertainty=uncertainty,
            reward_signal=reward_signal,
            is_floor_node=is_floor_node,
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(updated_at),
            archived=archived,
            flagged_by_human=flagged_by_human,
            flags=flags_list,
        )

    def _row_to_edge(self, row: tuple) -> Edge:
        """Convert database row to Edge object."""
        (edge_id, source_id, target_id, relation, strength, established_in,
         version, created_at, notes) = row

        return Edge(
            edge_id=edge_id,
            source_id=source_id,
            target_id=target_id,
            relation=RelationType(relation),
            strength=strength,
            established_in=established_in,
            version=version,
            created_at=datetime.fromisoformat(created_at),
            notes=notes,
        )

    def get_why_chain_depth(self, concept_id: str) -> int:
        """Get the depth of the WHY chain for a node."""
        node = self.get_node(concept_id)
        if not node:
            return 0
        return len(node.why_chain)

    def find_nodes_by_label(self, label_substring: str) -> List[Node]:
        """Find nodes by label substring."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT * FROM nodes WHERE label LIKE ?",
                (f"%{label_substring}%",),
            )
            rows = cursor.fetchall()
            return [self._row_to_node(row) for row in rows]

    def clear(self):
        """Clear all data from the graph (useful for testing)."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM edges")
            conn.execute("DELETE FROM nodes")
            conn.commit()
