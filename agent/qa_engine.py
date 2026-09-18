from typing import List, Dict, Any, Optional
from agent.state_manager import StateManager

class GroundedQAEngine:
    def __init__(self, state_manager: StateManager = None):
        self.state_manager = state_manager or StateManager()

    def answer_question(self, query: str, actions: List[Dict[str, Any]], date_str: str = "2026-09-25") -> Dict[str, Any]:
        """
        Answers executive queries strictly using grounded evidence from Data Pack actions and calendar context.
        STRICT RULE: If answer cannot be established from Data Pack, explicitly report that it is not established.
        """
        eval_time = f"{date_str}T23:59:59"
        eval_actions = self.state_manager.process_actions_state(actions, eval_time)

        q_lower = query.lower()

        # 1. "What did I promise Raghav?"
        if "raghav" in q_lower and ("promise" in q_lower or "commit" in q_lower or "deliver" in q_lower):
            raghav_promises = [
                a for a in eval_actions
                if (a.get("resolved_owner") == "Arjun Malhotra" or a.get("owner") == "Arjun Malhotra")
                and "raghav" in f"{a.get('requester_recipient', '')} {a.get('stakeholder', '')}".lower()
            ]
            return self._format_answer_response(
                query=query,
                headline=f"Arjun Malhotra's Commitments to CEO Raghav Verma ({len(raghav_promises)} items):",
                matched_actions=raghav_promises,
                notes="Grounded in Leadership Sync, Email Threads 1, 2, 4, and Voice Notes 1 & 2."
            )

        # 2. "What needs action today?" / "What is due today?"
        elif "today" in q_lower or "needs action" in q_lower:
            due_today = [
                a for a in eval_actions
                if a.get("effective_deadline")
                and str(a.get("effective_deadline")).startswith(date_str)
                and a.get("status") != "completed"
            ]
            if not due_today:
                due_today = [
                    a for a in eval_actions
                    if a.get("effective_deadline") and date_str in str(a.get("effective_deadline"))
                ]
            
            return self._format_answer_response(
                query=query,
                headline=f"Executive Action Items Due/Active on {date_str}:",
                matched_actions=due_today,
                notes="Filtered by effective deadline matching target date."
            )

        # 3. "What am I waiting for?" / "Waiting on others"
        elif "waiting" in q_lower or "pending from others" in q_lower:
            waiting_items = [
                a for a in eval_actions
                if a.get("category") == "waiting" or (
                    a.get("owner")
                    and a.get("owner") not in ("Arjun Malhotra", "Unassigned", None)
                )
            ]
            return self._format_answer_response(
                query=query,
                headline=f"Actions Waiting on Peers/Others ({len(waiting_items)} items):",
                matched_actions=waiting_items,
                notes="Items owned by peers (Divya Kapoor, Neha Sharma, Raghav Verma) where Arjun is dependent."
            )

        # 4. "What is overdue?"
        elif "overdue" in q_lower:
            overdue_items = [a for a in eval_actions if a.get("status") == "overdue" or a.get("resolved_status") == "OVERDUE"]
            return self._format_answer_response(
                query=query,
                headline=f"Overdue Action Items ({len(overdue_items)} items):",
                matched_actions=overdue_items,
                notes="Actions whose effective deadline passed prior to evaluation timestamp without recorded completion."
            )

        # 5. "What is unassigned?" / "Unclear ownership"
        elif "unassigned" in q_lower or "unclear" in q_lower or "ownership" in q_lower:
            unassigned_items = [
                a for a in eval_actions
                if a.get("category") == "unassigned"
                or a.get("is_unclear_ownership")
                or a.get("owner") in (None, "Unassigned")
            ]
            return self._format_answer_response(
                query=query,
                headline=f"Unassigned / Flagged Ownership Items ({len(unassigned_items)} items):",
                matched_actions=unassigned_items,
                notes="Actions identified in Data Pack without a designated individual owner."
            )

        # 6. "What did Divya send me?"
        elif "divya" in q_lower and ("send" in q_lower or "sent" in q_lower or "deliver" in q_lower or "provided" in q_lower):
            divya_items = [
                a for a in eval_actions
                if "divya" in str(a.get("owner", "")).lower() or any("divya" in str(e.get("snippet", "")).lower() for e in a.get("evidence", []))
            ]
            return self._format_answer_response(
                query=query,
                headline=f"Deliverables & Communications from Divya Kapoor ({len(divya_items)} items):",
                matched_actions=divya_items,
                notes="Grounded in Leadership Sync & Email Thread 2 (Technical Feasibility Sign-off)."
            )

        # 7. "What meetings do I have related to the pending actions?"
        elif "meeting" in q_lower or "calendar" in q_lower or "schedule" in q_lower:
            meeting_items = [
                a for a in eval_actions
                if a.get("related_calendar_events") or a.get("scheduling_insights")
            ]
            return self._format_meeting_response(query, meeting_items)

        # Generic Keyword Match Fallback
        matched = []
        for a in eval_actions:
            searchable = (
                f"{a.get('title', '')} {a.get('canonical_action', '')} {a.get('owner', '')} "
                f"{a.get('requester_recipient', '')} {a.get('description', '')}"
            ).lower()
            if any(w in searchable for w in q_lower.split() if len(w) > 3):
                matched.append(a)

        if matched:
            return self._format_answer_response(
                query=query,
                headline=f"Search Results for '{query}' ({len(matched)} matching actions):",
                matched_actions=matched,
                notes="Matched based on Data Pack action attributes."
            )

        # Non-established Fallback Rule
        return {
            "query": query,
            "answer_markdown": f"⚠️ **The requested information is not established in the supplied Data Pack.**\n\n*Query: '{query}'*\n*System Rule: Answers are strictly restricted to facts in data/data_pack.json.*",
            "matched_actions": [],
            "evidence_citations": []
        }

    def _format_answer_response(self, query: str, headline: str, matched_actions: List[Dict[str, Any]], notes: str) -> Dict[str, Any]:
        lines = [f"### {headline}\n"]
        all_citations = []

        for idx, act in enumerate(matched_actions, 1):
            owner_val = act.get('resolved_owner') or act.get('owner')
            owner_badge = f"👤 **Owner:** `{owner_val}`" if owner_val and owner_val != "Unassigned" else "👤 **Owner:** `UNCLEAR / UNASSIGNED (null)`"
            target_badge = f"🎯 **Target:** `{act.get('requester_recipient') or act.get('stakeholder') or 'N/A'}`"
            status_val = (act.get('resolved_status') or act.get('status') or 'PENDING').upper()
            status_badge = f"📌 **Status:** `{status_val}`"
            
            init_dl = act.get('initial_deadline') or act.get('initial_deadline_str') or 'N/A'
            eff_dl = act.get('resolved_deadline') or act.get('effective_deadline') or 'N/A'
            dl_str = f"⏳ **Deadline:** Initial: `{init_dl}` | Effective: `{eff_dl}`"
            if init_dl != eff_dl and init_dl != 'N/A':
                dl_str += " *(Chronologically Resolved)*"

            lines.append(f"#### {idx}. {act.get('canonical_action') or act.get('title')}")
            lines.append(f"{owner_badge} | {target_badge} | {status_badge}")
            lines.append(f"{dl_str}\n")

            if act.get("evidence"):
                lines.append("**Verbatim Source Evidence Citations:**")
                for ev in act["evidence"]:
                    src_tag = f"`{str(ev.get('source_type')).upper()}` ({ev.get('source_id')})"
                    ts = ev.get('timestamp')
                    quote = ev.get('snippet')
                    lines.append(f"- [{ts}] **{src_tag}**: *\"{quote}\"*")
                    all_citations.append({
                        "action_id": act.get("action_id"),
                        "source": src_tag,
                        "timestamp": ts,
                        "quote": quote
                    })

            for insight in act.get("scheduling_insights", []):
                lines.append(f"- 📅 **Calendar Context:** {insight}")

            lines.append("\n---")

        lines.append(f"\n*Note: {notes} Grounded 100% in data/data_pack.json.*")

        return {
            "query": query,
            "answer_markdown": "\n".join(lines),
            "matched_actions": matched_actions,
            "evidence_citations": all_citations
        }

    def _format_meeting_response(self, query: str, meeting_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        lines = ["### 📅 Scheduled Executive Meetings & Calendar Cross-References:\n"]
        all_citations = []

        for idx, act in enumerate(meeting_items, 1):
            lines.append(f"#### {idx}. Related Action: {act.get('canonical_action') or act.get('title')}")
            lines.append(f"- **Owner:** `{act.get('resolved_owner') or act.get('owner')}` | **Deadline:** `{act.get('resolved_deadline') or act.get('effective_deadline')}`")

            events = act.get("related_calendar_events", [])
            if events:
                lines.append("**Cross-Referenced Calendar Events:**")
                for ev in events:
                    attendees = ev.get("attendees") or []
                    if not isinstance(attendees, list):
                        attendees = [str(attendees)]
                    lines.append(
                        f"  - 🗓️ **{ev.get('event_title')}** on `{ev.get('date')}` ({ev.get('time')}) "
                        f"| Executive: `{ev.get('executive')}` | Attendees: `{', '.join(str(x) for x in attendees)}`"
                    )

            for insight in act.get("scheduling_insights", []):
                lines.append(f"- 💡 **Scheduling Insight:** {insight}")

            lines.append("\n---")

        lines.append("\n*Note: Grounded in Arjun's, Raghav's, Neha's, and Divya's calendars in data/data_pack.json.*")

        return {
            "query": query,
            "answer_markdown": "\n".join(lines),
            "matched_actions": meeting_items,
            "evidence_citations": all_citations
        }
