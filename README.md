# AGENTIC AI FACTORY — Executive Productivity Agent

An end-to-end Executive Productivity Agent built for **Arjun Malhotra, VP Sales**, analyzing multi-channel communication data from **Monday 21 September 2026 to Friday 25 September 2026**.

The system parses transcripts, emails, calendars, and voice notes from `data/data_pack.json`, extracts commitments, deduplicates cross-channel action items, resolves deadline shifts chronologically, flags unassigned ownership, tracks status (Pending, Completed, Overdue, Waiting on Others), generates daily executive action briefs, and powers a grounded executive Q&A engine with 100% source evidence citations.

---

## 🎯 Key Features & Requirements Coverage

1. **Commitment Isolation**: Isolates promises made by Arjun Malhotra to peers and executive leadership.
2. **Waiting on Others**: Separates items Arjun is dependent on (Divya Kapoor, Neha Sharma, Raghav Verma).
3. **Deadline Detection**: Extracts initial and updated deadlines across meetings and emails.
4. **Overdue Item Tracking**: Automatically flags overdue items where the deadline passed without completion evidence.
5. **Cross-Channel Deduplication**: Merges action item occurrences across meeting transcripts, 5 email threads (25 emails), and 2 voice notes.
6. **Chronological Deadline Resolution**: Updates deadlines based on chronological evidence timestamps (e.g. Acme proposal moved from Wed 5 PM to Thu 2 PM).
7. **Flag Unclear Ownership**: Explicitly flags items without a designated owner (e.g., Zenith security audit compliance review).
8. **Completion Tracking**: Identifies resolved/delivered actions (e.g. Acme proposal delivered Thu 1:30 PM).
9. **Daily Executive Action Brief**: Interactive summary view for any selected date in the Data Pack window.
10. **Grounded Executive Q&A**: Answers core questions (*"What did I promise Raghav?"*, *"What needs action today?"*, *"What am I waiting for?"*, *"What is overdue?"*, *"What is unassigned?"*).
11. **Strict Source Grounding**: All answers strictly rely on `data/data_pack.json` with verbatim evidence quotes and file metadata.

---

## 🏗 Project Architecture

```text
executive_productive_agent/
├── data/
│   └── data_pack.json             # Single source of truth containing all 5 data pack components
├── database/
│   ├── __init__.py
│   └── db_manager.py              # SQLite local persistence for actions and source evidence traces
├── agent/
│   ├── __init__.py
│   ├── data_loader.py             # Parses & standardizes data_pack.json into multi-modal text chunks
│   ├── extractor.py              # Candidate extraction (Deterministic demo pipeline + Gemini API fallback)
│   ├── deduplicator.py           # Deduplication & chronological deadline resolution
│   ├── state_manager.py          # Category & status classifier (Pending, Completed, Overdue, Waiting)
│   ├── brief_generator.py        # Compiles daily executive action briefs
│   └── qa_engine.py              # Strictly grounded Q&A engine with source evidence citations
├── app.py                         # Streamlit executive web application
├── requirements.txt               # Python package dependencies
├── .env.example                   # Environment configuration template
└── README.md                      # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+ installed.

### 2. Installation
Clone or navigate to the repository directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup (Optional)
If you wish to enable live Gemini API extraction, copy `.env.example` to `.env` and set your key:
```bash
cp .env.example .env
```
*Note: The application includes a **Deterministic Demo Mode** that runs out-of-the-box using `data/data_pack.json` without requiring an API key.*

### 4. Running the Application
Launch the Streamlit executive web interface:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 📊 Streamlit App Walkthrough

- **📊 Daily Action Brief**: Select any date from Sept 21–25, 2026 to inspect executive metrics, active commitments, waiting items, overdue alerts, and completed tasks.
- **💬 Executive AI Assistant**: Ask questions using interactive buttons or custom queries, receiving markdown answers backed by verbatim evidence quotes.
- **🔍 Action & Evidence Matrix**: Filterable grid of all actions with side-by-side evidence audit traces.
- **📁 Data Pack Inspector**: Browse the raw JSON data pack (people, meeting transcript, calendars, emails, voice notes).
- **⚡ System Audit & Pipeline**: Inspect raw SQLite tables and trigger pipeline re-indexing.
