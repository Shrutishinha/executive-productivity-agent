import streamlit as st
import os
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv

from agent.data_loader import DataLoader
from agent.extractor import ActionExtractor
from agent.deduplicator import ActionDeduplicator
from agent.state_manager import StateManager
from agent.brief_generator import DailyBriefGenerator
from agent.qa_engine import GroundedQAEngine
from database.db_manager import DatabaseManager

load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="EXECUTIVE PRODUCTIVITY AGENT | Arjun Malhotra",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Executive CSS Styling (Clean, non-decorative, high legibility)
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Executive Header */
    .header-container {
        background-color: #1e293b;
        border-bottom: 2px solid #334155;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }
    .header-title {
        color: #f8fafc;
        font-size: 26px;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .header-subtitle {
        color: #38bdf8;
        font-size: 15px;
        font-weight: 600;
        margin-top: 4px;
    }

    /* Metric Cards */
    .metric-card-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .metric-card-val {
        font-size: 32px;
        font-weight: 800;
        margin: 2px 0;
    }
    .metric-card-lbl {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
    }

    /* Item Card */
    .item-card {
        background: #1e293b;
        border-left: 4px solid #38bdf8;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .item-title {
        font-size: 16px;
        font-weight: 700;
        color: #f8fafc;
    }
    .item-meta {
        font-size: 13px;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Status Badges */
    .badge-completed { background: #064e3b; color: #34d399; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-overdue { background: #7f1d1d; color: #fca5a5; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-waiting { background: #78350f; color: #fde047; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-pending { background: #1e3a8a; color: #93c5fd; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
    .badge-unassigned { background: #4c1d95; color: #ddd6fe; padding: 2px 8px; border-radius: 4px; font-weight: 600; font-size: 11px; }
</style>
""", unsafe_allow_html=True)


# Initialize Pipeline & Persistence
@st.cache_resource
def get_db_manager():
    return DatabaseManager()

def run_pipeline(use_llm: bool = False):
    loader = DataLoader()
    extractor = ActionExtractor(loader)
    deduplicator = ActionDeduplicator()
    state_mgr = StateManager()

    # 1. Extract raw action candidates
    raw_candidates = extractor.extract_all_raw_actions(use_llm=use_llm)
    
    # 2. Resolution layer (merging, deadline resolution, calendar context)
    deduped_actions = deduplicator.deduplicate_and_resolve(raw_candidates)

    # 3. Process states
    final_actions = state_mgr.process_actions_state(deduped_actions)

    # 4. Save into SQLite
    db = get_db_manager()
    db.clear_all()
    for act in final_actions:
        db.save_action(act)

    return final_actions

def _evidence_line(ev: Dict[str, Any]) -> str:
    ts = ev.get("timestamp") or "n/a"
    src_type = str(ev.get("source_type") or "source").upper()
    src_id = ev.get("source_id") or ""
    snippet = ev.get("snippet") or ""
    src_id_part = f" ({src_id})" if src_id else ""
    return f"- **[{ts}] {src_type}{src_id_part}**: *\"{snippet}\"*"

# Ensure actions loaded
db = get_db_manager()
try:
    if st.session_state.pop("force_pipeline", False):
        mode_llm = st.session_state.get("use_llm_mode", False)
        actions = run_pipeline(use_llm=mode_llm)
        st.session_state["pipeline_ok"] = True
    else:
        actions = db.get_all_actions()
        if not actions:
            actions = run_pipeline(use_llm=False)
except (FileNotFoundError, ValueError) as e:
    st.error(f"Failed to load Data Pack / pipeline: {e}")
    st.stop()

# TOP HEADER
st.markdown("""
<div class="header-container">
    <div class="header-title">EXECUTIVE PRODUCTIVITY AGENT</div>
    <div class="header-subtitle">Arjun Malhotra | Week of 21–25 September 2026</div>
</div>
""", unsafe_allow_html=True)

# Sidebar Controls
with st.sidebar:
    st.header("Executive View Date")
    selected_date = st.selectbox(
        "Select Target Date:",
        ["2026-09-25", "2026-09-24", "2026-09-23", "2026-09-22", "2026-09-21"],
        format_func=lambda x: f"{x} ({['Mon','Tue','Wed','Thu','Fri'][int(x.split('-')[2])-21]})"
    )

    st.markdown("---")
    st.subheader("System Mode")
    
    has_api_key = bool(os.environ.get("GEMINI_API_KEY") and os.environ.get("GEMINI_API_KEY").strip() != "your_gemini_api_key_here")
    
    extraction_mode = st.radio(
        "Extraction Pipeline Mode:",
        ["Deterministic Demo (Offline)", "Live Gemini LLM API"],
        index=0 if not has_api_key else 0
    )
    use_llm_selected = (extraction_mode == "Live Gemini LLM API")
    st.session_state["use_llm_mode"] = use_llm_selected

    if use_llm_selected:
        if has_api_key:
            st.success("🔑 GEMINI_API_KEY Detected")
        else:
            st.warning("⚠️ No valid GEMINI_API_KEY in .env. Will fall back to Deterministic mode if invoked.")
    else:
        st.success("🟢 Deterministic Demo Mode Active")
        st.caption("Data source: `data/data_pack.json` ONLY")

    if st.session_state.pop("pipeline_ok", False):
        st.success("Pipeline executed successfully!")

    if st.button("🔄 Re-run Pipeline"):
        st.session_state["force_pipeline"] = True
        st.rerun()

# Date-scoped status (persisted rows are week-resolved; view date reclassifies overdue/completed)
view_eval_ts = f"{selected_date}T23:59:59"
actions = StateManager().process_actions_state(actions, view_eval_ts)

# Compute Summary Metrics for Selected Date
brief_gen = DailyBriefGenerator()
brief = brief_gen.generate_brief_for_date(actions, selected_date)

count_my_actions = len(brief["my_actions"])
count_waiting = len(brief["waiting_on_others"])
count_due_today = len(brief["due_today"])
count_overdue = len(brief["overdue"])
count_unassigned = len(brief["unclear_ownership"])

# TOP SUMMARY METRICS (5 Metric Cards)
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f'<div class="metric-card-container"><div class="metric-card-val" style="color: #38bdf8;">{count_my_actions}</div><div class="metric-card-lbl">My Actions</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card-container"><div class="metric-card-val" style="color: #fde047;">{count_waiting}</div><div class="metric-card-lbl">Waiting on Others</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card-container"><div class="metric-card-val" style="color: #60a5fa;">{count_due_today}</div><div class="metric-card-lbl">Due Today</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card-container"><div class="metric-card-val" style="color: #fca5a5;">{count_overdue}</div><div class="metric-card-lbl">Overdue</div></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card-container"><div class="metric-card-val" style="color: #c084fc;">{count_unassigned}</div><div class="metric-card-lbl">Unclear Ownership</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# THE 6 REQUIRED TABS
tab_brief, tab_all, tab_waiting, tab_unclear, tab_qa, tab_sources = st.tabs([
    "1. Daily Brief",
    "2. All Actions",
    "3. Waiting on Others",
    "4. Unclear Ownership",
    "5. Q&A",
    "6. Sources"
])

# ==========================================
# TAB 1: DAILY BRIEF
# ==========================================
with tab_brief:
    st.markdown(brief["markdown"])

# ==========================================
# TAB 2: ALL ACTIONS
# ==========================================
with tab_all:
    st.subheader("All Resolved Action Items")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        cat_filter = st.multiselect("Filter Category:", ["commitment", "waiting", "unassigned"], default=["commitment", "waiting", "unassigned"])
    with col_f2:
        status_filter = st.multiselect("Filter Status:", ["completed", "overdue", "pending", "waiting"], default=["completed", "overdue", "pending", "waiting"])

    filtered_actions = [
        a for a in actions
        if a.get("category") in cat_filter and a.get("status") in status_filter
    ]

    table_data = []
    for a in filtered_actions:
        owner_val = a.get("owner") if a.get("owner") not in (None, "Unassigned") else "null (Unassigned)"
        table_data.append({
            "Action Title": a.get("title") or a.get("canonical_action"),
            "Owner": owner_val,
            "Stakeholder": a.get("requester_recipient", "N/A"),
            "Category": str(a.get("category") or "").upper(),
            "Status": str(a.get("status") or "").upper(),
            "Initial Deadline": a.get("initial_deadline_str") or a.get("initial_deadline") or "N/A",
            "Effective Deadline": a.get("effective_deadline") or "N/A",
            "Evidence Count": len(a.get("evidence") or [])
        })

    df = pd.DataFrame(table_data, columns=[
        "Action Title", "Owner", "Stakeholder", "Category", "Status",
        "Initial Deadline", "Effective Deadline", "Evidence Count"
    ])
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("Action Evidence Audit Traces & Calendar Context")
    for a in filtered_actions:
        owner_val = a.get("owner") if a.get("owner") not in (None, "Unassigned") else "null (Unassigned)"
        status_label = str(a.get("status") or "pending").upper()
        with st.expander(f"📌 {a.get('title')} — Owner: {owner_val} | Status: {status_label}"):
            st.write(f"**Initial Deadline:** `{a.get('initial_deadline_str') or a.get('initial_deadline')}` | **Effective Deadline:** `{a.get('effective_deadline')}`")
            st.write("**Verbatim Source Evidence:**")
            for ev in a.get("evidence") or []:
                st.write(_evidence_line(ev))
            for insight in a.get("scheduling_insights") or []:
                st.info(f"📅 {insight}")

# ==========================================
# TAB 3: WAITING ON OTHERS
# ==========================================
with tab_waiting:
    st.subheader("Actions Waiting on Others")
    st.caption("Actions owned by peers where Arjun is dependent for deliverables.")

    waiting_list = [
        a for a in actions
        if a.get("category") == "waiting" or (
            a.get("owner") and a.get("owner") not in ("Arjun Malhotra", "Unassigned", None)
        )
    ]

    if not waiting_list:
        st.info("No actions waiting on others.")
    else:
        for act in waiting_list:
            st.markdown(f"""
            <div class="item-card" style="border-left-color: #fde047;">
                <div style="display: flex; justify-content: space-between;">
                    <div class="item-title">{act.get('title')}</div>
                    <span class="badge-{act.get('status') or 'pending'}">{str(act.get('status') or '').upper()}</span>
                </div>
                <div class="item-meta">
                    Owner: <b>{act.get('owner')}</b> | Stakeholder: <b>{act.get('requester_recipient','N/A')}</b> | Effective Deadline: <b>{act.get('effective_deadline')}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("📌 Source Evidence"):
                for ev in act.get("evidence") or []:
                    st.write(_evidence_line(ev))

# ==========================================
# TAB 4: UNCLEAR OWNERSHIP
# ==========================================
with tab_unclear:
    st.subheader("Unclear Ownership / Unassigned Action Items")
    st.caption("Actions identified in Data Pack where ownership was not explicitly established.")

    unclear_list = [
        a for a in actions
        if a.get("category") == "unassigned" or a.get("is_unclear_ownership") or a.get("owner") in (None, "Unassigned")
    ]

    if not unclear_list:
        st.info("No unclear ownership items.")
    else:
        for act in unclear_list:
            st.markdown(f"""
            <div class="item-card" style="border-left-color: #c084fc;">
                <div style="display: flex; justify-content: space-between;">
                    <div class="item-title">{act.get('title')}</div>
                    <span class="badge-unassigned">UNCLEAR OWNERSHIP (null)</span>
                </div>
                <div class="item-meta">
                    Stakeholder: <b>{act.get('requester_recipient','N/A')}</b> | Effective Deadline: <b>{act.get('effective_deadline')}</b> | Status: <b>{str(act.get('status') or '').upper()}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("📌 Flagged Source Quotes"):
                for ev in act.get("evidence") or []:
                    st.write(_evidence_line(ev))

# ==========================================
# TAB 5: Q&A
# ==========================================
with tab_qa:
    st.subheader("💬 Grounded Executive Q&A Assistant")
    st.caption("Answers are strictly restricted to data/data_pack.json facts with verbatim evidence citations.")

    qa_engine = GroundedQAEngine()

    st.markdown("**Quick Executive Queries:**")
    q_cols1 = st.columns(4)
    q_cols2 = st.columns(3)
    selected_query = None

    if q_cols1[0].button("🤝 What did I promise Raghav?"):
        selected_query = "What did I promise Raghav?"
    if q_cols1[1].button("📅 What needs action today?"):
        selected_query = "What needs action today?"
    if q_cols1[2].button("⏳ What am I waiting for?"):
        selected_query = "What am I waiting for?"
    if q_cols1[3].button("🚨 What is overdue?"):
        selected_query = "What is overdue?"

    if q_cols2[0].button("❓ What is unassigned?"):
        selected_query = "What is unassigned?"
    if q_cols2[1].button("📩 What did Divya send me?"):
        selected_query = "What did Divya send me?"
    if q_cols2[2].button("🗓️ Pending Action Meetings?"):
        selected_query = "What meetings do I have related to the pending actions?"

    if selected_query:
        st.session_state["qa_query"] = selected_query

    custom_query = st.text_input("Or enter your custom question:", key="qa_query")

    if custom_query:
        result = qa_engine.answer_question(custom_query, actions, selected_date)
        st.markdown("---")
        st.markdown(result["answer_markdown"])

# ==========================================
# TAB 6: SOURCES
# ==========================================
with tab_sources:
    st.subheader("📁 Data Pack Raw Sources (`data/data_pack.json`)")
    st.caption("Raw source inspector for people, leadership meeting transcript, calendars, emails, and voice notes.")

    loader = DataLoader()

    dp_subtab1, dp_subtab2, dp_subtab3, dp_subtab4, dp_subtab5 = st.tabs([
        "People Directory",
        "Leadership Meeting Transcript",
        "Calendars",
        "Email Threads (5)",
        "Voice Notes (2)"
    ])

    with dp_subtab1:
        st.json(loader.get_people())
    with dp_subtab2:
        lm = loader.get_leadership_meeting() or {}
        st.markdown(f"### {lm.get('title') or 'Leadership Meeting'} ({lm.get('date') or 'n/a'})")
        st.text_area("Transcript Text", lm.get("transcript") or "", height=300, disabled=True)
    with dp_subtab3:
        st.json(loader.get_calendars())
    with dp_subtab4:
        st.json(loader.get_email_threads())
    with dp_subtab5:
        st.json(loader.get_voice_notes())
