import json
import os
from typing import Dict, Any, List
from agent.deadline_resolver import DeadlineResolver

DATA_PACK_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "data_pack.json")


class DataLoader:
    def __init__(self, file_path: str = DATA_PACK_PATH):
        self.file_path = file_path
        self._deadline_resolver = DeadlineResolver()
        self.raw_data = self._load_json()

    def _load_json(self) -> Dict[str, Any]:
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Data pack file not found at {self.file_path}")
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in data pack at {self.file_path}: {e.msg} "
                f"(line {e.lineno}, column {e.colno})"
            ) from e

        if not isinstance(data, dict):
            raise ValueError(f"Data pack root must be a JSON object, got {type(data).__name__}")
        return data

    def get_people(self) -> List[Dict[str, str]]:
        people = self.raw_data.get("people", [])
        return people if isinstance(people, list) else []

    def get_leadership_meeting(self) -> Dict[str, Any]:
        lm = self.raw_data.get("leadership_meeting", {})
        return lm if isinstance(lm, dict) else {}

    def get_calendars(self) -> Dict[str, List[Dict[str, Any]]]:
        calendars = self.raw_data.get("calendars", {})
        return calendars if isinstance(calendars, dict) else {}

    def get_email_threads(self) -> List[Dict[str, Any]]:
        threads = self.raw_data.get("email_threads", [])
        return threads if isinstance(threads, list) else []

    def get_voice_notes(self) -> List[Dict[str, Any]]:
        notes = self.raw_data.get("voice_notes", [])
        return notes if isinstance(notes, list) else []

    def get_all_document_chunks(self) -> List[Dict[str, Any]]:
        """
        Flattens all data sources into a standardized list of text chunks
        with metadata (source_type, source_id, timestamp, text).
        """
        chunks = []

        # 1. Leadership meeting
        lm = self.get_leadership_meeting()
        if lm:
            chunks.append({
                "source_type": "meeting",
                "source_id": "leadership_sync_2026-09-21",
                "title": lm.get("title"),
                "timestamp": self._deadline_resolver.compose_timestamp(lm.get("date"), lm.get("time")),
                "text": lm.get("transcript") or ""
            })

        # 2. Email threads
        for thread in self.get_email_threads():
            if not isinstance(thread, dict):
                continue
            thread_id = thread.get("thread_id")
            subject = thread.get("subject")
            emails = thread.get("emails", [])
            if not isinstance(emails, list):
                continue
            for email in emails:
                if not isinstance(email, dict):
                    continue
                chunks.append({
                    "source_type": "email",
                    "source_id": f"{thread_id}:{email.get('email_id')}",
                    "title": f"Email: {subject}",
                    "sender": email.get("sender"),
                    "recipients": email.get("recipients"),
                    "timestamp": email.get("timestamp"),
                    "text": email.get("body") or ""
                })

        # 3. Voice notes
        for vn in self.get_voice_notes():
            if not isinstance(vn, dict):
                continue
            chunks.append({
                "source_type": "voice_note",
                "source_id": vn.get("voice_note_id"),
                "title": f"Voice Note ({vn.get('date')})",
                "speaker": vn.get("speaker"),
                "timestamp": vn.get("timestamp"),
                "text": vn.get("transcript") or ""
            })

        # 4. Calendars
        for person, events in self.get_calendars().items():
            if not isinstance(events, list):
                continue
            for ev in events:
                if not isinstance(ev, dict):
                    continue
                chunks.append({
                    "source_type": "calendar",
                    "source_id": f"calendar_{person}_{ev.get('date')}",
                    "title": f"Calendar: {ev.get('event')}",
                    "person": person,
                    "timestamp": self._deadline_resolver.compose_timestamp(ev.get("date"), ev.get("time")),
                    "text": (
                        f"Event: {ev.get('event')}, Date: {ev.get('date')}, "
                        f"Time: {ev.get('time')}, Attendees: {', '.join(ev.get('attendees', []) or [])}"
                    )
                })

        return chunks
