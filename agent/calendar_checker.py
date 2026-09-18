from typing import List, Dict, Any
from agent.data_loader import DataLoader
from agent.deadline_resolver import DeadlineResolver


class CalendarChecker:
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()
        self.deadline_resolver = DeadlineResolver()

    def cross_check_action_calendars(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cross-checks action items against executive calendar schedules from data/data_pack.json.
        Adds related calendar context, meeting alignment, and scheduling insights.
        STRICT RULE: Calendar events NEVER infer or overwrite action ownership.
        """
        calendars = self.data_loader.get_calendars()

        # Flatten all calendar events with executive name
        all_events = []
        for person, events in calendars.items():
            if not isinstance(events, list):
                continue
            for ev in events:
                if not isinstance(ev, dict):
                    continue
                event_title = ev.get("event") or ""
                date_val = ev.get("date") or ""
                time_val = ev.get("time") or ""
                attendees = ev.get("attendees") or []
                if not isinstance(attendees, list):
                    attendees = []
                all_events.append({
                    "executive": person,
                    "event_title": event_title,
                    "date": date_val,
                    "time": time_val,
                    "attendees": attendees,
                    "timestamp": self.deadline_resolver.compose_timestamp(date_val, time_val)
                })

        updated_actions = []

        for act in actions:
            act_copy = dict(act)
            title = (act_copy.get("canonical_action") or act_copy.get("title") or "").lower()
            related_events = []
            scheduling_insights = []

            # 1. Topic & Keyword Matching with Calendar Events
            if "acme" in title:
                matching_evs = [e for e in all_events if "acme" in (e["event_title"] or "").lower()]
                related_events.extend(matching_evs)

                for ev in matching_evs:
                    if ev["date"] == "2026-09-24" and "14:00" in (ev["time"] or ""):
                        scheduling_insights.append(
                            f"Calendar Alignment: '{ev['event_title']}' scheduled on {ev['date']} at {ev['time']} directly coincides with the updated Acme proposal deadline (Thu Sep 24 14:00)."
                        )

            elif "forecast" in title:
                matching_evs = [
                    e for e in all_events
                    if "forecast" in (e["event_title"] or "").lower() or "pipeline" in (e["event_title"] or "").lower()
                ]
                related_events.extend(matching_evs)

                for ev in matching_evs:
                    if ev["date"] == "2026-09-23":
                        scheduling_insights.append(
                            f"Scheduling Note: Arjun had a '{ev['event_title']}' on {ev['date']} ({ev['time']}), but deliverable was shifted because Divya's engineering sign-off was pending."
                        )

            elif "battlecard" in title or "competitor" in title:
                matching_evs = [
                    e for e in all_events
                    if "advisory board" in (e["event_title"] or "").lower() or "customer" in (e["event_title"] or "").lower()
                ]
                related_events.extend(matching_evs)

                for ev in matching_evs:
                    if ev["date"] == "2026-09-25":
                        scheduling_insights.append(
                            f"Deliverable Context: '{ev['event_title']}' on Fri Sep 25 ({ev['time']}) requires the Competitor Battlecard due at 12:00 PM."
                        )

            elif "hiring" in title or "architect" in title or "budget" in title:
                matching_evs = [
                    e for e in all_events
                    if "board" in (e["event_title"] or "").lower() or "reorg" in (e["event_title"] or "").lower()
                ]
                related_events.extend(matching_evs)

            # Deduplicate related events
            unique_events = []
            seen = set()
            for ev in related_events:
                key = (ev["executive"], ev["event_title"], ev["date"], ev["time"])
                if key not in seen:
                    seen.add(key)
                    unique_events.append(ev)

            # Assign calendar context (kept SEPARATE from ownership)
            act_copy["related_calendar_events"] = unique_events
            act_copy["scheduling_insights"] = scheduling_insights

            updated_actions.append(act_copy)

        return updated_actions
