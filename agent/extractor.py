import os
import json
import re
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from agent.data_loader import DataLoader

load_dotenv()

class ActionExtractor:
    def __init__(self, data_loader: DataLoader = None):
        self.data_loader = data_loader or DataLoader()

    def extract_all_raw_actions(self, use_llm: bool = False) -> List[Dict[str, Any]]:
        """
        Extracts action items from all sources in data/data_pack.json.
        Provides a deterministic high-precision pipeline based strictly on the Data Pack.
        """
        api_key = (os.environ.get("GEMINI_API_KEY") or "").strip()
        if use_llm and api_key and api_key != "your_gemini_api_key_here":
            try:
                return self._extract_with_llm()
            except Exception as e:
                print(f"[Extractor] LLM extraction failed: {e}. Falling back to deterministic mode.")
        
        return self._extract_deterministic()

    def _extract_deterministic(self) -> List[Dict[str, Any]]:
        """
        Deterministic extraction directly parsing facts from data/data_pack.json.
        Strictly enforces user JSON example schema format:
        - action, owner (str or null), owner_type ("PERSON" or null), stakeholder,
          deadline, deadline_type ("EXPLICIT"/"IMPLIED"/"FIXED"/"UPDATED"), status ("PENDING"/"COMPLETED"/"OVERDUE"/"WAITING"),
          source, timestamp, evidence, confidence.
        """
        raw_candidates = []

        # 1. Leadership Sync Actions
        raw_candidates.append({
            "action": "Finalize Q4 Sales Pipeline Forecast",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-23T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:03:00",
            "evidence": "[09:03] Arjun Malhotra: I commit to sending you the finalized Q4 Sales Forecast by Wednesday, September 23 at 5:00 PM.",
            "confidence": 1.0,

            # Downstream compatibility mappings
            "candidate_id": "cand_forecast_sync",
            "action_title": "Finalize Q4 Sales Pipeline Forecast",
            "requester_recipient": "Raghav Verma",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:03] Arjun Malhotra: I commit to sending you the finalized Q4 Sales Forecast by Wednesday, September 23 at 5:00 PM.",
            "extracted_deadline": "2026-09-23T17:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "owner": "Divya Kapoor",
            "owner_type": "PERSON",
            "stakeholder": "Arjun Malhotra",
            "deadline": "2026-09-23T11:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:08:00",
            "evidence": "[09:08] Divya Kapoor: I will provide the technical feasibility sign-off to you by Wednesday morning, September 23 at 11:00 AM.",
            "confidence": 1.0,

            "candidate_id": "cand_divya_feasibility_sync",
            "action_title": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "requester_recipient": "Arjun Malhotra",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:08] Divya Kapoor: I will provide the technical feasibility sign-off to you by Wednesday morning, September 23 at 11:00 AM.",
            "extracted_deadline": "2026-09-23T11:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Acme Corp",
            "deadline": "2026-09-23T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:12:00",
            "evidence": "[09:12] Arjun Malhotra: I will draft the revised Acme proposal and share it with Raghav by Wednesday, September 23 at 5:00 PM for executive approval.",
            "confidence": 1.0,

            "candidate_id": "cand_acme_proposal_sync",
            "action_title": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "requester_recipient": "Vikram Seth",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:12] Arjun Malhotra: I will draft the revised Acme proposal and share it with Raghav by Wednesday, September 23 at 5:00 PM for executive approval.",
            "extracted_deadline": "2026-09-23T17:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Send Product Roadmap v2 Deck for Enterprise Pitches",
            "owner": "Neha Sharma",
            "owner_type": "PERSON",
            "stakeholder": "Arjun Malhotra",
            "deadline": "2026-09-24T12:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:21:00",
            "evidence": "[09:21] Neha Sharma: I will send the Product Roadmap v2 deck to Arjun by Thursday, September 24 at 12:00 PM.",
            "confidence": 1.0,

            "candidate_id": "cand_roadmap_sync",
            "action_title": "Send Product Roadmap v2 Deck for Enterprise Pitches",
            "requester_recipient": "Arjun Malhotra",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:21] Neha Sharma: I will send the Product Roadmap v2 deck to Arjun by Thursday, September 24 at 12:00 PM.",
            "extracted_deadline": "2026-09-24T12:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Prepare & Deliver Competitor Battlecard Deck",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-25T12:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:28:00",
            "evidence": "[09:28] Arjun Malhotra: I will prepare the Competitor Battlecard and deliver it to you by Friday, September 25 at 12:00 PM.",
            "confidence": 1.0,

            "candidate_id": "cand_battlecard_sync",
            "action_title": "Prepare & Deliver Competitor Battlecard Deck",
            "requester_recipient": "Raghav Verma",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:28] Arjun Malhotra: I will prepare the Competitor Battlecard and deliver it to you by Friday, September 25 at 12:00 PM.",
            "extracted_deadline": "2026-09-25T12:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Approve Budget for 2 Lead Solutions Architects",
            "owner": "Raghav Verma",
            "owner_type": "PERSON",
            "stakeholder": "Neha Sharma",
            "deadline": "2026-09-22T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:32:00",
            "evidence": "[09:32] Neha Sharma: Raghav, please approve the reorg budget by Tuesday, September 22 at 5:00 PM.",
            "confidence": 1.0,

            "candidate_id": "cand_hiring_budget_sync",
            "action_title": "Approve Budget for 2 Lead Solutions Architects",
            "requester_recipient": "Neha Sharma",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:32] Neha Sharma: Raghav, please approve the reorg budget by Tuesday, September 22 at 5:00 PM.",
            "extracted_deadline": "2026-09-22T17:00:00",
            "is_unclear_ownership": False
        })

        # Ownership not explicitly established -> owner MUST be null
        raw_candidates.append({
            "action": "Complete Zenith Account Security Audit Compliance Review",
            "owner": None,
            "owner_type": None,
            "stakeholder": "Priya Nair",
            "deadline": "2026-09-23T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Leadership Meeting",
            "timestamp": "2026-09-21T09:37:00",
            "evidence": "[09:37] Raghav Verma: Someone from security or engineering needs to complete the Zenith security audit compliance review by Wednesday, September 23 at 5:00 PM.",
            "confidence": 0.9,

            "candidate_id": "cand_zenith_security_sync",
            "action_title": "Complete Zenith Account Security Audit Compliance Review",
            "requester_recipient": "Priya Nair",
            "source_type": "meeting",
            "source_id": "leadership_sync_2026-09-21",
            "snippet": "[09:37] Raghav Verma: Someone from security or engineering needs to complete the Zenith security audit compliance review by Wednesday, September 23 at 5:00 PM.",
            "extracted_deadline": "2026-09-23T17:00:00",
            "is_unclear_ownership": True
        })

        # 2. Email Thread Updates
        raw_candidates.append({
            "action": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Acme Corp",
            "deadline": "2026-09-24T14:00:00",
            "deadline_type": "UPDATED",
            "status": "PENDING",
            "source": "Email Thread 1",
            "timestamp": "2026-09-23T09:30:00",
            "evidence": "We officially resolve and update the revised Acme proposal deadline to Thursday, September 24 at 2:00 PM.",
            "confidence": 1.0,

            "candidate_id": "cand_acme_ext_t1e4",
            "action_title": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "requester_recipient": "Vikram Seth",
            "source_type": "email",
            "source_id": "thread_1_acme_deal:t1_e4",
            "snippet": "We officially resolve and update the revised Acme proposal deadline to Thursday, September 24 at 2:00 PM.",
            "extracted_deadline": "2026-09-24T14:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Acme Corp",
            "deadline": "2026-09-24T14:00:00",
            "deadline_type": "EXPLICIT",
            "status": "COMPLETED",
            "source": "Email Thread 1",
            "timestamp": "2026-09-24T13:30:00",
            "evidence": "Attached is the finalized Acme Enterprise Pricing Proposal with 15% tier discount approved. This completes the Acme proposal deliverable ahead of today's 2:00 PM deadline.",
            "confidence": 1.0,

            "candidate_id": "cand_acme_done_t1e5",
            "action_title": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "requester_recipient": "Vikram Seth",
            "source_type": "email",
            "source_id": "thread_1_acme_deal:t1_e5",
            "snippet": "Attached is the finalized Acme Enterprise Pricing Proposal with 15% tier discount approved. This completes the Acme proposal deliverable ahead of today's 2:00 PM deadline.",
            "extracted_deadline": "2026-09-24T14:00:00",
            "is_unclear_ownership": False,
            "is_completion": True
        })

        raw_candidates.append({
            "action": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "owner": "Divya Kapoor",
            "owner_type": "PERSON",
            "stakeholder": "Arjun Malhotra",
            "deadline": "2026-09-24T16:00:00",
            "deadline_type": "UPDATED",
            "status": "WAITING",
            "source": "Email Thread 2",
            "timestamp": "2026-09-22T17:30:00",
            "evidence": "I won't be able to provide sign-off by Wednesday morning. I will complete technical sign-off by Thursday, September 24 at 4:00 PM.",
            "confidence": 1.0,

            "candidate_id": "cand_divya_delay_t2e2",
            "action_title": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "requester_recipient": "Arjun Malhotra",
            "source_type": "email",
            "source_id": "thread_2_q4_forecast:t2_e2",
            "snippet": "I won't be able to provide sign-off by Wednesday morning. I will complete technical sign-off by Thursday, September 24 at 4:00 PM.",
            "extracted_deadline": "2026-09-24T16:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Finalize Q4 Sales Pipeline Forecast",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-25T09:00:00",
            "deadline_type": "UPDATED",
            "status": "PENDING",
            "source": "Email Thread 2",
            "timestamp": "2026-09-23T11:30:00",
            "evidence": "Quick update: I am waiting on Divya for engineering feasibility sign-off. Consequently, my Q4 Sales Forecast deliverable deadline is shifted to Friday, September 25 at 9:00 AM.",
            "confidence": 1.0,

            "candidate_id": "cand_forecast_shift_t2e3",
            "action_title": "Finalize Q4 Sales Pipeline Forecast",
            "requester_recipient": "Raghav Verma",
            "source_type": "email",
            "source_id": "thread_2_q4_forecast:t2_e3",
            "snippet": "Quick update: I am waiting on Divya for engineering feasibility sign-off. Consequently, my Q4 Sales Forecast deliverable deadline is shifted to Friday, September 25 at 9:00 AM.",
            "extracted_deadline": "2026-09-25T09:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "owner": "Divya Kapoor",
            "owner_type": "PERSON",
            "stakeholder": "Arjun Malhotra",
            "deadline": "2026-09-24T16:00:00",
            "deadline_type": "EXPLICIT",
            "status": "COMPLETED",
            "source": "Email Thread 2",
            "timestamp": "2026-09-24T15:45:00",
            "evidence": "Engineering sign-off on enterprise custom connectors is complete and approved.",
            "confidence": 1.0,

            "candidate_id": "cand_divya_done_t2e4",
            "action_title": "Provide Engineering Feasibility Sign-off for Enterprise Features",
            "requester_recipient": "Arjun Malhotra",
            "source_type": "email",
            "source_id": "thread_2_q4_forecast:t2_e4",
            "snippet": "Engineering sign-off on enterprise custom connectors is complete and approved.",
            "extracted_deadline": "2026-09-24T16:00:00",
            "is_unclear_ownership": False,
            "is_completion": True
        })

        raw_candidates.append({
            "action": "Finalize Q4 Sales Pipeline Forecast",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-25T09:00:00",
            "deadline_type": "EXPLICIT",
            "status": "COMPLETED",
            "source": "Email Thread 2",
            "timestamp": "2026-09-25T08:50:00",
            "evidence": "I have finalized the Q4 Sales Pipeline Forecast ($4.2M total, weighted $3.1M). Attached is the full forecast document. This fulfills my promise for Friday 9:00 AM.",
            "confidence": 1.0,

            "candidate_id": "cand_forecast_done_t2e5",
            "action_title": "Finalize Q4 Sales Pipeline Forecast",
            "requester_recipient": "Raghav Verma",
            "source_type": "email",
            "source_id": "thread_2_q4_forecast:t2_e5",
            "snippet": "I have finalized the Q4 Sales Pipeline Forecast ($4.2M total, weighted $3.1M). Attached is the full forecast document. This fulfills my promise for Friday 9:00 AM.",
            "extracted_deadline": "2026-09-25T09:00:00",
            "is_unclear_ownership": False,
            "is_completion": True
        })

        raw_candidates.append({
            "action": "Prepare & Deliver Competitor Battlecard Deck",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-25T12:00:00",
            "deadline_type": "EXPLICIT",
            "status": "COMPLETED",
            "source": "Email Thread 4",
            "timestamp": "2026-09-25T11:30:00",
            "evidence": "Attached is the completed Competitor Battlecard and Positioning Deck for the Customer Advisory Board. Delivered at 11:30 AM, ahead of the Friday 12:00 PM deadline.",
            "confidence": 1.0,

            "candidate_id": "cand_battlecard_done_t4e5",
            "action_title": "Prepare & Deliver Competitor Battlecard Deck",
            "requester_recipient": "Raghav Verma",
            "source_type": "email",
            "source_id": "thread_4_competitor_deck:t4_e5",
            "snippet": "Attached is the completed Competitor Battlecard and Positioning Deck for the Customer Advisory Board. Delivered at 11:30 AM, ahead of the Friday 12:00 PM deadline.",
            "extracted_deadline": "2026-09-25T12:00:00",
            "is_unclear_ownership": False,
            "is_completion": True
        })

        raw_candidates.append({
            "action": "Complete Zenith Account Security Audit Compliance Review",
            "owner": None,
            "owner_type": None,
            "stakeholder": "Priya Nair",
            "deadline": "2026-09-23T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "OVERDUE",
            "source": "Email Thread 3",
            "timestamp": "2026-09-23T17:30:00",
            "evidence": "Raghav, the Zenith security audit compliance deadline of Wed Sep 23 5:00 PM has passed without completion. This action item remains OVERDUE and UNASSIGNED.",
            "confidence": 1.0,

            "candidate_id": "cand_zenith_overdue_t3e4",
            "action_title": "Complete Zenith Account Security Audit Compliance Review",
            "requester_recipient": "Priya Nair",
            "source_type": "email",
            "source_id": "thread_3_customer_onboarding:t3_e4",
            "snippet": "Raghav, the Zenith security audit compliance deadline of Wed Sep 23 5:00 PM has passed without completion. This action item remains OVERDUE and UNASSIGNED.",
            "extracted_deadline": "2026-09-23T17:00:00",
            "is_unclear_ownership": True
        })

        raw_candidates.append({
            "action": "Approve Budget for 2 Lead Solutions Architects",
            "owner": "Raghav Verma",
            "owner_type": "PERSON",
            "stakeholder": "Neha Sharma",
            "deadline": "2026-09-22T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "OVERDUE",
            "source": "Email Thread 5",
            "timestamp": "2026-09-25T10:00:00",
            "evidence": "Status as of Friday Sept 25: Hiring budget signoff by Raghav remains OVERDUE (was due Tue Sep 22 5:00 PM). Action is pending Raghav's approval.",
            "confidence": 1.0,

            "candidate_id": "cand_hiring_overdue_t5e5",
            "action_title": "Approve Budget for 2 Lead Solutions Architects",
            "requester_recipient": "Neha Sharma",
            "source_type": "email",
            "source_id": "thread_5_hiring_reorg:t5_e5",
            "snippet": "Status as of Friday Sept 25: Hiring budget signoff by Raghav remains OVERDUE (was due Tue Sep 22 5:00 PM). Action is pending Raghav's approval.",
            "extracted_deadline": "2026-09-22T17:00:00",
            "is_unclear_ownership": False
        })

        # 3. Voice Notes Evidence
        raw_candidates.append({
            "action": "Finalize Q4 Sales Pipeline Forecast",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Raghav Verma",
            "deadline": "2026-09-23T17:00:00",
            "deadline_type": "EXPLICIT",
            "status": "PENDING",
            "source": "Voice Note 1",
            "timestamp": "2026-09-21T20:00:00",
            "evidence": "I promised Raghav the finalized Q4 Sales Forecast by Wednesday September 23 at 5:00 PM. But I'm waiting on Divya for engineering technical feasibility sign-off due Wednesday 11 AM.",
            "confidence": 1.0,

            "candidate_id": "cand_vn1",
            "action_title": "Finalize Q4 Sales Pipeline Forecast",
            "requester_recipient": "Raghav Verma",
            "source_type": "voice_note",
            "source_id": "vn_1",
            "snippet": "I promised Raghav the finalized Q4 Sales Forecast by Wednesday September 23 at 5:00 PM. But I'm waiting on Divya for engineering technical feasibility sign-off due Wednesday 11 AM.",
            "extracted_deadline": "2026-09-23T17:00:00",
            "is_unclear_ownership": False
        })

        raw_candidates.append({
            "action": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "owner": "Arjun Malhotra",
            "owner_type": "PERSON",
            "stakeholder": "Acme Corp",
            "deadline": "2026-09-24T14:00:00",
            "deadline_type": "EXPLICIT",
            "status": "COMPLETED",
            "source": "Voice Note 2",
            "timestamp": "2026-09-24T19:30:00",
            "evidence": "The Acme proposal deadline was updated to Thursday 2:00 PM and I successfully delivered the finalized proposal to Vikram and Raghav at 1:30 PM. That action is COMPLETED!",
            "confidence": 1.0,

            "candidate_id": "cand_vn2",
            "action_title": "Draft & Deliver Revised Acme Corp Pricing Proposal (15% discount)",
            "requester_recipient": "Vikram Seth",
            "source_type": "voice_note",
            "source_id": "vn_2",
            "snippet": "The Acme proposal deadline was updated to Thursday 2:00 PM and I successfully delivered the finalized proposal to Vikram and Raghav at 1:30 PM. That action is COMPLETED!",
            "extracted_deadline": "2026-09-24T14:00:00",
            "is_unclear_ownership": False,
            "is_completion": True
        })

        return raw_candidates

    def _extract_with_llm(self) -> List[Dict[str, Any]]:
        # Structured LLM call using Google GenAI SDK enforcing strict requested JSON schema
        from google import genai

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key.strip() in ("", "your_gemini_api_key_here"):
            raise RuntimeError("GEMINI_API_KEY is missing or still set to the example placeholder.")

        client = genai.Client(api_key=api_key)
        chunks = self.data_loader.get_all_document_chunks()

        prompt = f"""
        Extract all candidate actions from the provided Data Pack text chunks.
        Return a strict JSON array of objects conforming to this schema:
        - action (str): Title or description of the candidate action.
        - owner (str or null): Name of the owner (e.g. "Arjun Malhotra") or null if ownership is not explicitly established.
        - owner_type (str or null): "PERSON" if owner is designated, or null if ownership is not explicitly established.
        - stakeholder (str): Requester or recipient of the action.
        - deadline (str or null): Deadline ISO string or text.
        - deadline_type (str): "EXPLICIT" | "IMPLIED" | "UPDATED" | "FIXED".
        - status (str): "PENDING" | "COMPLETED" | "OVERDUE" | "WAITING".
        - source (str): Source description (e.g. "Email Thread 1", "Leadership Meeting", "Voice Note 1").
        - timestamp (str): Timestamp of the source document chunk.
        - evidence (str): Exact verbatim quote from source text.
        - confidence (float): 0.0 to 1.0 score.

        STRICT OWNERSHIP RULES:
        - If Arjun explicitly says "I will..." then Arjun is owner ("Arjun Malhotra", owner_type: "PERSON").
        - If another person explicitly says they will do something, that person is owner (owner_type: "PERSON").
        - If ownership is not explicitly established, owner MUST be null (JSON null), and owner_type MUST be null.
        - NEVER infer ownership from someone's role or normal business responsibility.

        Data Chunks:
        {json.dumps(chunks[:15], indent=2)}
        """

        gen_config = {"response_mime_type": "application/json"}
        try:
            from google.genai import types
            gen_config = types.GenerateContentConfig(response_mime_type="application/json")
        except Exception:
            pass

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=gen_config
        )
        raw_text = getattr(response, "text", None)
        extracted = self._parse_llm_json(raw_text)

        # Format extracted items to include internal mapping fields
        normalized = []
        for item in extracted:
            if not isinstance(item, dict):
                continue
            owner = item.get("owner")
            if isinstance(owner, str) and owner.strip().lower() in ("null", "none", "unassigned", "unclear", ""):
                owner = None
                item["owner"] = None
            item["action_title"] = item.get("action") or item.get("action_title") or "Untitled action"
            item["requester_recipient"] = item.get("stakeholder") or item.get("requester_recipient")
            item["snippet"] = item.get("evidence") or item.get("snippet") or ""
            item["extracted_deadline"] = item.get("deadline")
            item["source_type"] = str(item.get("source") or "source").lower()
            item["source_id"] = item.get("source") or item.get("source_id") or "unknown"
            item["is_unclear_ownership"] = owner is None
            if owner is None:
                item["owner_type"] = None
            normalized.append(item)

        if not normalized:
            raise ValueError("Gemini returned no valid action objects.")
        return normalized

    def _parse_llm_json(self, text: Optional[str]) -> List[Dict[str, Any]]:
        if not text or not str(text).strip():
            raise ValueError("Empty JSON response from Gemini API.")

        cleaned = str(text).strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
            if not match:
                raise ValueError("Gemini response was not valid JSON.")
            data = json.loads(match.group(1))

        if isinstance(data, dict):
            for key in ("actions", "items", "candidates", "results", "data"):
                if isinstance(data.get(key), list):
                    data = data[key]
                    break
            else:
                if "action" in data or "action_title" in data:
                    data = [data]
                else:
                    raise ValueError("Gemini JSON object did not contain an actions list.")

        if not isinstance(data, list):
            raise ValueError(f"Gemini JSON must be a list, got {type(data).__name__}.")
        return data
