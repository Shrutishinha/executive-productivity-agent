from typing import List, Dict, Any, Optional
from agent.deadline_resolver import DeadlineResolver

class DailyBriefGenerator:
    def __init__(self, deadline_resolver: DeadlineResolver = None):
        self.deadline_resolver = deadline_resolver or DeadlineResolver()

    def generate_brief_for_date(self, actions: List[Dict[str, Any]], date_str: str = "2026-09-25") -> Dict[str, Any]:
        """
        Compiles a structured 7-section daily executive brief for Arjun Malhotra for target date_str (YYYY-MM-DD):
        1. OVERDUE
        2. DUE TODAY
        3. MY ACTIONS
        4. WAITING ON OTHERS
        5. UNCLEAR OWNERSHIP
        6. UPCOMING
        7. RECENTLY COMPLETED
        """
        eval_timestamp = f"{date_str}T23:59:59"

        overdue_section = []
        due_today_section = []
        my_actions_section = []
        waiting_on_others_section = []
        unclear_ownership_section = []
        upcoming_section = []
        recently_completed_section = []

        for act in actions:
            # Extract standard attributes
            action_title = act.get("canonical_action") or act.get("title") or act.get("action")
            owner = act.get("resolved_owner") if "resolved_owner" in act else act.get("owner")
            if owner == "Unassigned":
                owner = None
            stakeholder = act.get("stakeholder") or act.get("requester_recipient") or "N/A"
            deadline = act.get("resolved_deadline") or act.get("effective_deadline")
            
            status_raw = (act.get("resolved_status") or act.get("status") or "PENDING").upper()
            eval_dt = self.deadline_resolver.to_datetime(eval_timestamp)
            comp_dt = self.deadline_resolver.to_datetime(act.get("completion_timestamp"))
            is_completed = bool(comp_dt and eval_dt and comp_dt <= eval_dt)

            # Classify deadline relative to date_str
            deadline_class = self.deadline_resolver.classify_action_deadline(
                deadline, eval_timestamp, is_completed
            )

            # Primary source & evidence quote
            sources_list = act.get("sources") or act.get("evidence") or []
            first_src = sources_list[0] if sources_list else {}
            src_tag = first_src.get("source") or first_src.get("source_id") or "Data Pack"
            evidence_quote = first_src.get("evidence") or first_src.get("snippet") or "Source evidence in Data Pack."

            item_dict = {
                "action": action_title,
                "owner": owner,
                "stakeholder": stakeholder,
                "deadline": deadline,
                "status": status_raw,
                "source": src_tag,
                "evidence": evidence_quote,
                "sources_all": sources_list,
                "scheduling_insights": act.get("scheduling_insights", [])
            }

            # Categorize into 7 sections
            if is_completed:
                recently_completed_section.append(item_dict)
            else:
                if deadline_class == "overdue":
                    overdue_section.append(item_dict)
                elif deadline_class == "due_today":
                    due_today_section.append(item_dict)
                elif deadline_class == "upcoming":
                    upcoming_section.append(item_dict)

                if owner == "Arjun Malhotra":
                    my_actions_section.append(item_dict)
                elif owner is not None:
                    waiting_on_others_section.append(item_dict)
                else:
                    unclear_ownership_section.append(item_dict)

        # Build Markdown Representation
        markdown_text = self._build_markdown_brief(
            date_str, overdue_section, due_today_section, my_actions_section,
            waiting_on_others_section, unclear_ownership_section, upcoming_section,
            recently_completed_section
        )

        return {
            "date": date_str,
            "executive": "Arjun Malhotra, VP Sales",
            "overdue": overdue_section,
            "due_today": due_today_section,
            "my_actions": my_actions_section,
            "waiting_on_others": waiting_on_others_section,
            "unclear_ownership": unclear_ownership_section,
            "upcoming": upcoming_section,
            "recently_completed": recently_completed_section,
            "summary_text": f"Daily Brief for Arjun Malhotra ({date_str}): {len(overdue_section)} Overdue | {len(due_today_section)} Due Today | {len(my_actions_section)} My Actions | {len(waiting_on_others_section)} Waiting | {len(unclear_ownership_section)} Unassigned | {len(recently_completed_section)} Completed",
            "markdown": markdown_text,

            # Backward compatibility fields for Streamlit app UI
            "commitments": my_actions_section,
            "overdue_items": overdue_section,
            "unassigned_items": unclear_ownership_section,
            "completed_items": recently_completed_section
        }

    def _build_markdown_brief(
        self, date_str: str,
        overdue: List[Dict[str, Any]],
        due_today: List[Dict[str, Any]],
        my_actions: List[Dict[str, Any]],
        waiting: List[Dict[str, Any]],
        unclear: List[Dict[str, Any]],
        upcoming: List[Dict[str, Any]],
        completed: List[Dict[str, Any]]
    ) -> str:
        lines = [
            f"# DAILY EXECUTIVE ACTION BRIEF — ARJUN MALHOTRA",
            f"**Target View Date:** `{date_str}` | **Role:** VP Sales | **Data Pack Window:** Sept 21–25, 2026\n",
            "---"
        ]

        def render_section(title: str, items: List[Dict[str, Any]], icon: str = "📌"):
            lines.append(f"\n## {icon} {title} ({len(items)})\n")
            if not items:
                lines.append("*No items in this section for selected date.*\n")
                return

            for idx, item in enumerate(items, 1):
                owner_str = f"**Owner:** `{item['owner']}`" if item['owner'] else "**Owner:** `UNCLEAR / UNASSIGNED (null)`"
                lines.append(f"### {idx}. {item['action']}")
                lines.append(f"- {owner_str} | **Stakeholder:** `{item['stakeholder']}` | **Status:** `{item['status']}`")
                lines.append(f"- **Deadline:** `{item['deadline']}`")
                lines.append(f"- **Source:** `{item['source']}`")
                lines.append(f"- **Evidence:** *\"{item['evidence']}\"*")
                
                for insight in item.get("scheduling_insights", []):
                    lines.append(f"- **Calendar Context:** {insight}")
                lines.append("")

        render_section("1. OVERDUE", overdue, "🚨")
        render_section("2. DUE TODAY", due_today, "📅")
        render_section("3. MY ACTIONS", my_actions, "🎯")
        render_section("4. WAITING ON OTHERS", waiting, "⏳")
        render_section("5. UNCLEAR OWNERSHIP", unclear, "❓")
        render_section("6. UPCOMING", upcoming, "📆")
        render_section("7. RECENTLY COMPLETED", completed, "✅")

        lines.append("\n---\n*System Rule: Strictly grounded in data/data_pack.json facts with zero invented facts.*")

        return "\n".join(lines)
