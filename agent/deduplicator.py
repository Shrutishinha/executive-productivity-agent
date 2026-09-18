from typing import List, Dict, Any
from agent.resolution_layer import ActionResolutionLayer

class ActionDeduplicator:
    def __init__(self):
        self.resolution_layer = ActionResolutionLayer()

    def deduplicate_and_resolve(self, raw_candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Delegates to ActionResolutionLayer to merge semantically identical actions,
        prefer later explicit updates, track completion, and retain source evidence history.
        """
        return self.resolution_layer.resolve_action_candidates(raw_candidates)
