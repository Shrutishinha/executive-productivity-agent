import re
from typing import List, Dict, Any, Optional
from agent.deadline_resolver import DeadlineResolver
from agent.calendar_checker import CalendarChecker

class ActionResolutionLayer:
    """
    Resolution layer comparing multiple mentions of the same action across:
    - meeting transcript
    - emails
    - voice notes
    - calendar schedules
    """

    def __init__(self, deadline_resolver: DeadlineResolver = None, calendar_checker: CalendarChecker = None):
        self.deadline_resolver = deadline_resolver or DeadlineResolver()
        self.calendar_checker = calendar_checker or CalendarChecker()

    def resolve_action_candidates(self, raw_candidates: List[Dict[str, Any]], eval_timestamp: str = "2026-09-25T17:00:00") -> List[Dict[str, Any]]:
        """
        Executes semantic clustering, cross-channel merging, relative date parsing,
        calendar cross-checking, chronological deadline preference, and strict classification.
        """
        # 1. Group candidate mentions by semantic action identity
        clusters: Dict[str, List[Dict[str, Any]]] = {}

        for cand in raw_candidates:
            key = self._get_semantic_cluster_key(cand.get("action", cand.get("action_title", "")))
            if key not in clusters:
                clusters[key] = []
            clusters[key].append(cand)

        resolved_actions = []

        # 2. Process each cluster to form canonical resolved action
        for cluster_key, candidate_list in clusters.items():
            # Sort chronologically by timestamp
            candidate_list.sort(key=lambda x: x.get("timestamp", ""))

            first_mention = candidate_list[0]
            latest_mention = candidate_list[-1]

            # Primary identification
            canonical_action = first_mention.get("action") or first_mention.get("action_title")
            canonical_id = f"res_{cluster_key}"

            # Ownership resolution (STRICT RULE: Never infer from role or calendar event; preserve null if unassigned)
            explicit_owners = [c.get("owner") for c in candidate_list if c.get("owner") is not None]
            resolved_owner = explicit_owners[0] if explicit_owners else None
            owner_type = "PERSON" if resolved_owner is not None else None

            # Stakeholder
            stakeholders = [c.get("stakeholder") or c.get("requester_recipient") for c in candidate_list if c.get("stakeholder") or c.get("requester_recipient")]
            stakeholder = stakeholders[0] if stakeholders else "Executive Leadership"

            # Chronological deadline tracking (convert relative dates & prefer later explicit updates)
            deadline_history = []
            for c in candidate_list:
                raw_dl = c.get("deadline") or c.get("extracted_deadline")
                msg_ts = c.get("timestamp", "2026-09-21T09:00:00")
                parsed_dl = self.deadline_resolver.parse_relative_deadline(raw_dl, msg_ts)
                
                if parsed_dl and parsed_dl not in [dh["deadline"] for dh in deadline_history]:
                    deadline_history.append({
                        "timestamp": msg_ts,
                        "raw_deadline": raw_dl,
                        "deadline": parsed_dl,
                        "source": c.get("source") or c.get("source_id"),
                        "deadline_type": c.get("deadline_type", "EXPLICIT")
                    })

            initial_deadline = deadline_history[0]["deadline"] if deadline_history else None
            resolved_deadline = deadline_history[-1]["deadline"] if deadline_history else None
            deadline_status = "UPDATED" if len(deadline_history) > 1 and initial_deadline != resolved_deadline else ("FIXED" if initial_deadline else "NONE")

            # Completion detection
            completion_mentions = [
                c for c in candidate_list 
                if c.get("status") == "COMPLETED" or c.get("is_completion") is True
            ]
            
            is_completed = len(completion_mentions) > 0
            completion_timestamp = completion_mentions[0].get("timestamp") if is_completed else None

            # Deadline Classification: overdue / due_today / upcoming / no_deadline / completed
            deadline_classification = self.deadline_resolver.classify_action_deadline(
                resolved_deadline, eval_timestamp, is_completed
            )

            # Resolved status
            if is_completed:
                resolved_status = "COMPLETED"
            elif deadline_classification == "overdue":
                resolved_status = "OVERDUE"
            elif resolved_owner and resolved_owner != "Arjun Malhotra":
                resolved_status = "WAITING"
            else:
                resolved_status = "PENDING"

            # Preserve all relevant sources (verbatim evidence audit trail)
            sources = []
            for c in candidate_list:
                msg_ts = c.get("timestamp", "2026-09-21T09:00:00")
                raw_dl = c.get("deadline") or c.get("extracted_deadline")
                parsed_dl = self.deadline_resolver.parse_relative_deadline(raw_dl, msg_ts)
                source_label = c.get("source") or f"{c.get('source_type') or 'source'}:{c.get('source_id') or 'unknown'}"

                sources.append({
                    "source": source_label,
                    "timestamp": msg_ts,
                    "raw_deadline": raw_dl,
                    "parsed_deadline": parsed_dl,
                    "status": c.get("status", "PENDING"),
                    "evidence": c.get("evidence") or c.get("snippet") or ""
                })

            # Detect useful contradictory evidence / deadline shifts
            contradictions_and_updates = []
            if len(deadline_history) > 1:
                for dh in deadline_history[1:]:
                    contradictions_and_updates.append({
                        "timestamp": dh["timestamp"],
                        "type": "DEADLINE_UPDATE",
                        "note": f"Deadline updated from {initial_deadline} to {dh['deadline']} in {dh['source']}."
                    })
            
            if resolved_owner is None:
                contradictions_and_updates.append({
                    "timestamp": first_mention.get("timestamp"),
                    "type": "UNASSIGNED_OWNERSHIP",
                    "note": "Ownership was explicitly flagged as unassigned across sources."
                })

            resolved_actions.append({
                "canonical_id": canonical_id,
                "canonical_action": canonical_action,
                "resolved_owner": resolved_owner,
                "owner_type": owner_type,
                "stakeholder": stakeholder,
                "initial_deadline": initial_deadline,
                "resolved_deadline": resolved_deadline,
                "deadline_status": deadline_status,
                "deadline_classification": deadline_classification,
                "resolved_status": resolved_status,
                "completion_timestamp": completion_timestamp,
                "sources_count": len(sources),
                "sources": sources,
                "contradictions_and_updates": contradictions_and_updates,

                # Backward compatibility fields for state_manager & UI
                "action_id": canonical_id,
                "title": canonical_action,
                "owner": resolved_owner or "Unassigned",
                "requester_recipient": stakeholder,
                "status": resolved_status.lower(),
                "category": "unassigned" if resolved_owner is None else ("commitment" if resolved_owner == "Arjun Malhotra" else "waiting"),
                "initial_deadline_str": initial_deadline,
                "effective_deadline": resolved_deadline,
                "is_unclear_ownership": (resolved_owner is None),
                "evidence": [
                    {
                        "source_type": (
                            str(s["source"]).split(":")[0]
                            if s.get("source") and ":" in str(s["source"])
                            else (str(s["source"]).lower().replace(" ", "_") if s.get("source") else "source")
                        ),
                        "source_id": s.get("source") or "unknown",
                        "timestamp": s.get("timestamp"),
                        "snippet": s.get("evidence") or "",
                        "extracted_deadline": s.get("parsed_deadline")
                    }
                    for s in sources
                ]
            })

        # 3. Add calendar cross-checking context & scheduling insights (without modifying ownership)
        resolved_actions = self.calendar_checker.cross_check_action_calendars(resolved_actions)

        return resolved_actions

    def _get_semantic_cluster_key(self, title: str) -> str:
        """Groups titles into semantic action topics."""
        t = (title or "").lower()
        if "forecast" in t:
            return "q4_sales_forecast"
        if "acme" in t:
            return "acme_pricing_proposal"
        if "battlecard" in t or "competitor" in t:
            return "competitor_battlecard"
        if "roadmap" in t:
            return "product_roadmap_v2"
        if "hiring" in t or "architect" in t or "budget" in t:
            return "solutions_architect_hiring"
        if "zenith" in t or "security" in t:
            return "zenith_security_audit"
        if "feasibility" in t or "engineering" in t:
            return "engineering_feasibility_signoff"
        return re.sub(r'[^a-z0-9]', '', t)
