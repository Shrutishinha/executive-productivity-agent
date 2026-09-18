import sqlite3
import os
import json
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "executive_agent.db")

METADATA_KEYS = (
    "scheduling_insights",
    "related_calendar_events",
    "resolved_status",
    "resolved_owner",
    "canonical_action",
    "canonical_id",
    "deadline_status",
    "deadline_classification",
    "contradictions_and_updates",
    "sources",
    "owner_type",
    "stakeholder",
    "resolved_deadline",
)


class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Table for deduplicated/resolved action items
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    action_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    owner TEXT,
                    requester_recipient TEXT,
                    category TEXT, -- commitment / waiting / unassigned
                    status TEXT,   -- pending / completed / overdue / waiting
                    initial_deadline TEXT,
                    effective_deadline TEXT,
                    is_unclear_ownership BOOLEAN,
                    completion_timestamp TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    metadata TEXT
                );
            """)
            self._ensure_column(cursor, "actions", "metadata", "TEXT")

            # Table for granular evidence traces
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS evidence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    action_id TEXT NOT NULL,
                    source_type TEXT NOT NULL, -- meeting / email / voice_note / calendar
                    source_id TEXT,
                    timestamp TEXT,
                    snippet TEXT NOT NULL,
                    extracted_deadline TEXT,
                    FOREIGN KEY (action_id) REFERENCES actions (action_id)
                );
            """)
            conn.commit()

    def _ensure_column(self, cursor, table: str, column: str, col_type: str):
        cursor.execute(f"PRAGMA table_info({table})")
        existing = {row[1] for row in cursor.fetchall()}
        if column not in existing:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

    def clear_all(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM evidence;")
            cursor.execute("DELETE FROM actions;")
            conn.commit()

    def save_action(self, action: Dict[str, Any]):
        action_id = action.get("action_id") or action.get("canonical_id")
        title = action.get("title") or action.get("canonical_action") or "Untitled action"
        if not action_id:
            raise ValueError("Cannot persist action without action_id")

        extra = {k: action.get(k) for k in METADATA_KEYS if k in action}
        try:
            metadata_json = json.dumps(extra)
        except (TypeError, ValueError):
            metadata_json = "{}"

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO actions (
                    action_id, title, description, owner, requester_recipient,
                    category, status, initial_deadline, effective_deadline,
                    is_unclear_ownership, completion_timestamp, created_at, updated_at,
                    metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                action_id,
                title,
                action.get("description", ""),
                action.get("owner") if action.get("owner") is not None else "Unassigned",
                action.get("requester_recipient", ""),
                action.get("category", "unassigned"),
                action.get("status", "pending"),
                action.get("initial_deadline") or action.get("initial_deadline_str"),
                action.get("effective_deadline") or action.get("resolved_deadline"),
                1 if action.get("is_unclear_ownership") else 0,
                action.get("completion_timestamp"),
                action.get("created_at"),
                action.get("updated_at"),
                metadata_json
            ))

            # Re-insert evidence traces
            cursor.execute("DELETE FROM evidence WHERE action_id = ?;", (action_id,))
            for ev in action.get("evidence", []) or []:
                if not isinstance(ev, dict):
                    continue
                cursor.execute("""
                    INSERT INTO evidence (action_id, source_type, source_id, timestamp, snippet, extracted_deadline)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    action_id,
                    ev.get("source_type") or "unknown",
                    ev.get("source_id") or "",
                    ev.get("timestamp") or "",
                    ev.get("snippet") or "",
                    ev.get("extracted_deadline")
                ))
            conn.commit()

    def get_all_actions(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM actions ORDER BY effective_deadline ASC;")
            action_rows = cursor.fetchall()

            results = []
            for row in action_rows:
                act = dict(row)
                act["is_unclear_ownership"] = bool(act["is_unclear_ownership"])
                act["initial_deadline_str"] = act.get("initial_deadline")

                raw_meta = act.pop("metadata", None)
                if raw_meta:
                    try:
                        extra = json.loads(raw_meta)
                        if isinstance(extra, dict):
                            act.update(extra)
                    except json.JSONDecodeError:
                        pass

                # Fetch evidence
                cursor.execute("SELECT * FROM evidence WHERE action_id = ? ORDER BY timestamp ASC;", (act["action_id"],))
                ev_rows = cursor.fetchall()
                act["evidence"] = [dict(ev) for ev in ev_rows]
                results.append(act)
            return results

    def get_actions_by_category(self, category: str) -> List[Dict[str, Any]]:
        actions = self.get_all_actions()
        return [a for a in actions if a.get("category") == category]
