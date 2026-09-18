import re
from datetime import datetime, timedelta
from typing import Optional

# Data Pack Reference Week Boundaries
# Monday 21 September 2026 to Friday 25 September 2026
WEEK_START = datetime(2026, 9, 21)
WEEK_END = datetime(2026, 9, 25)

WEEKDAY_MAP = {
    "monday": "2026-09-21",
    "tuesday": "2026-09-22",
    "wednesday": "2026-09-23",
    "thursday": "2026-09-24",
    "friday": "2026-09-25",
    "saturday": "2026-09-26",
    "sunday": "2026-09-27"
}


class DeadlineResolver:
    def __init__(self, reference_week_start: datetime = WEEK_START):
        self.ref_start = reference_week_start

    def to_datetime(self, value: Optional[str]) -> Optional[datetime]:
        """Parse ISO-like timestamps used across the Data Pack and pipeline."""
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.lower() in ["none", "null", "n/a", "no deadline"]:
            return None

        if text.endswith("Z"):
            text = text[:-1]
        if text.endswith("+00:00"):
            text = text[:-6]
        if "T" not in text and " " in text:
            text = text.replace(" ", "T", 1)

        if re.match(r"^\d{4}-\d{2}-\d{2}$", text):
            text = f"{text}T17:00:00"

        # Truncate fractional seconds / unexpected suffixes for fromisoformat
        m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", text)
        if m and len(text) > 19 and not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$", text):
            if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+", text):
                try:
                    return datetime.fromisoformat(text)
                except ValueError:
                    text = m.group(1)
            else:
                text = m.group(1)

        try:
            return datetime.fromisoformat(text)
        except ValueError:
            try:
                return datetime.strptime(text[:16], "%Y-%m-%dT%H:%M")
            except ValueError:
                return None

    def to_iso(self, value: Optional[str]) -> Optional[str]:
        dt = self.to_datetime(value)
        return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None

    def compose_timestamp(self, date_str: Optional[str], time_str: Optional[str]) -> str:
        """Build a valid ISO timestamp from calendar date + 'HH:MM - HH:MM' / AM-PM ranges."""
        date_part = (date_str or "2026-09-21").strip()
        start_raw = "09:00"
        if time_str:
            start_raw = str(time_str).split(" - ")[0].strip()
        time_part = self._extract_time_str(start_raw.lower()) or "09:00:00"
        composed = f"{date_part}T{time_part}"
        normalized = self.to_iso(composed)
        return normalized or f"{date_part}T09:00:00"

    def parse_relative_deadline(self, deadline_expr: Optional[str], source_timestamp: str = "2026-09-21T09:00:00") -> Optional[str]:
        """
        Converts relative date expressions (e.g. 'tomorrow', 'Wednesday morning', 'Thursday 2:00 PM', 'Friday EOD', 'today')
        to absolute ISO 8601 timestamps within the Data Pack week of Sept 21-25, 2026.
        """
        if not deadline_expr:
            return None
        expr = str(deadline_expr).strip()
        if not expr or expr.lower() in ["none", "null", "n/a", "no deadline"]:
            return None

        # If already in ISO format (e.g., 2026-09-23T17:00:00 or 2026-09-23), validate and return
        iso_existing = self.to_iso(expr)
        if iso_existing and re.match(r"^\d{4}-\d{2}-\d{2}", expr):
            return iso_existing

        expr_lower = expr.lower()

        source_dt = self.to_datetime(source_timestamp) or datetime(2026, 9, 21, 9, 0)

        # 1. Parse 'today', 'tomorrow', 'yesterday'
        if "today" in expr_lower:
            target_date = source_dt.date()
            time_str = self._extract_time_str(expr_lower) or "17:00:00"
            return f"{target_date.isoformat()}T{time_str}"

        if "tomorrow" in expr_lower:
            target_date = source_dt.date() + timedelta(days=1)
            time_str = self._extract_time_str(expr_lower) or "17:00:00"
            return f"{target_date.isoformat()}T{time_str}"

        if "yesterday" in expr_lower:
            target_date = source_dt.date() - timedelta(days=1)
            time_str = self._extract_time_str(expr_lower) or "17:00:00"
            return f"{target_date.isoformat()}T{time_str}"

        # 2. Parse named weekdays (Monday .. Friday)
        for day_name, iso_date in WEEKDAY_MAP.items():
            if day_name in expr_lower:
                time_str = self._extract_time_str(expr_lower) or "17:00:00"
                return f"{iso_date}T{time_str}"

        # Unparseable relative text must not silently become Friday EOD
        return None

    def _extract_time_str(self, text: str) -> Optional[str]:
        """Extracts time component or defaults based on qualifiers (morning, EOD, noon, etc.)."""
        text = (text or "").lower().replace(".", "")

        # Prefer explicit 12-hour times so "September 23 at 5:00 PM" does not capture the day number
        m = re.search(r"\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)\b", text)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2)) if m.group(2) else 0
            meridiem = m.group(3)
            if meridiem == "pm" and hour < 12:
                hour += 12
            elif meridiem == "am" and hour == 12:
                hour = 0
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return f"{hour:02d}:{minute:02d}:00"

        m24 = re.search(r"\b([01]?\d|2[0-3]):([0-5]\d)(?::([0-5]\d))?\b", text)
        if m24:
            hour = int(m24.group(1))
            minute = int(m24.group(2))
            second = int(m24.group(3)) if m24.group(3) else 0
            return f"{hour:02d}:{minute:02d}:{second:02d}"

        if "morning" in text:
            return "11:00:00"
        if "noon" in text or "midday" in text:
            return "12:00:00"
        if "afternoon" in text:
            return "16:00:00"
        if "eod" in text or "end of day" in text or "close of business" in text:
            return "17:00:00"
        if "evening" in text:
            return "19:00:00"

        return None

    def classify_action_deadline(self, deadline_iso: Optional[str], evaluation_timestamp: str, is_completed: bool = False) -> str:
        """
        Classifies an action's deadline status into one of 4 strict buckets:
        - overdue
        - due_today
        - upcoming
        - no_deadline
        """
        deadline_dt = self.to_datetime(deadline_iso)
        if deadline_dt is None:
            return "no_deadline"

        if is_completed:
            return "completed"

        eval_dt = self.to_datetime(evaluation_timestamp) or datetime(2026, 9, 25, 23, 59, 59)

        if deadline_dt.date() == eval_dt.date():
            return "due_today"
        if deadline_dt < eval_dt:
            return "overdue"
        return "upcoming"
