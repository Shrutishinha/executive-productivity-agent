from typing import List, Dict, Any
from agent.deadline_resolver import DeadlineResolver


class StateManager:
    def __init__(self, reference_date: str = "2026-09-25T17:00:00"):
        self.reference_date = reference_date
        self.deadline_resolver = DeadlineResolver()

    def process_actions_state(self, actions: List[Dict[str, Any]], ref_timestamp: str = None) -> List[Dict[str, Any]]:
        eval_time = ref_timestamp or self.reference_date
        processed = []

        for act in actions:
            act_copy = dict(act)

            # 1. Determine Category (owner may be JSON null / DB NULL)
            owner = act_copy.get("owner")
            is_unclear = bool(act_copy.get("is_unclear_ownership", False))
            owner_name = owner.strip() if isinstance(owner, str) else owner

            if (
                is_unclear
                or owner_name in (None, "", "Unassigned", "None", "null")
                or (isinstance(owner_name, str) and owner_name.lower() == "unclear")
            ):
                category = "unassigned"
            elif owner_name == "Arjun Malhotra":
                category = "commitment"
            else:
                category = "waiting"

            act_copy["category"] = category

            # 2. Determine Status relative to evaluation timestamp
            comp_dt = self.deadline_resolver.to_datetime(act_copy.get("completion_timestamp"))
            eval_dt = self.deadline_resolver.to_datetime(eval_time)
            eff_deadline = act_copy.get("effective_deadline") or act_copy.get("resolved_deadline")

            if comp_dt and eval_dt and comp_dt <= eval_dt:
                status = "completed"
            else:
                deadline_class = self.deadline_resolver.classify_action_deadline(
                    eff_deadline, eval_time, is_completed=False
                )
                if deadline_class == "overdue":
                    status = "overdue"
                elif category == "waiting":
                    status = "waiting"
                else:
                    status = "pending"

            act_copy["status"] = status
            processed.append(act_copy)

        return processed
