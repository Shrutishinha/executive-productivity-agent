<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&height=190&color=gradient&customColorList=12,14,16,18&text=EXECUTIVE%20AI%20AGENT&fontSize=42&fontColor=ffffff&animation=twinkling&fontAlignY=43" width="100%"/>

<br>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=17&duration=2200&pause=700&color=8B5CF6&center=true&vCenter=true&width=850&lines=Processing+business+signals...;Extracting+executive+commitments...;Resolving+deadlines+%26+ownership...;Tracking+actions+with+evidence...;Generating+grounded+executive+intelligence..." />

<br><br>

<img src="https://skillicons.dev/icons?i=python,streamlit,sqlite,pandas&theme=light" />

<br><br>

AI • Automation • Executive Decision Support • Grounded Q&A

</div>

✨ What Problem Does It Solve?

Executives receive important information across multiple channels:

📨 Emails

🗓️ Calendar events

📝 Meeting transcripts

🎙️ Voice notes

Important commitments can easily become scattered, duplicated, delayed, or unclear.

This agent converts that unstructured information into a single source of actionable truth.

Input → Intelligence → Action

Emails ───────┐
Meetings ─────┤
Calendars ────┼──► Extraction ─► Deduplication ─► State Tracking
Voice Notes ──┘                                      │
                                                    ▼
                                      ┌─────────────────────────┐
                                      │ Executive Action Layer  │
                                      ├─────────────────────────┤
                                      │ Daily Brief             │
                                      │ Waiting on Others       │
                                      │ Overdue Actions         │
                                      │ Unassigned Actions      │
                                      │ Completed Commitments   │
                                      │ Grounded Q&A             │
                                      └─────────────────────────┘

🎯 Core Capabilities

Capability

Description

🔎 Commitment Extraction

Identifies promises and actions committed to by Arjun

🤝 Dependency Tracking

Detects actions waiting on Divya, Neha, Raghav, or others

⏰ Deadline Detection

Extracts deadlines from emails, meetings, calendars, and voice notes

🔄 Deadline Resolution

Applies the latest chronological deadline when commitments change

🧩 Cross-Channel Deduplication

Merges multiple references to the same action

🚨 Overdue Detection

Flags incomplete actions whose deadlines have passed

👤 Ownership Detection

Identifies actions with unclear or missing ownership

✅ Completion Tracking

Detects evidence that an action has been completed

📊 Daily Executive Brief

Generates a date-specific action summary

💬 Grounded Q&A

Answers executive questions using only verified source evidence

🔗 Evidence Traceability

Every important answer/action can be traced back to its source

🧠 Intelligence Pipeline

The application follows a structured processing pipeline:

                ┌──────────────────────┐
                │     DATA PACK        │
                │  data_pack.json      │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    DATA LOADER       │
                │ Parse & Normalize    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │     EXTRACTOR        │
                │ Commitments          │
                │ Deadlines            │
                │ Owners               │
                │ Dependencies         │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    DEDUPLICATOR      │
                │ Cross-channel merge  │
                │ Deadline resolution  │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │   STATE MANAGER      │
                │ Pending              │
                │ Completed            │
                │ Overdue              │
                │ Waiting              │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │    SQLite STORE      │
                │ Actions + Evidence   │
                └──────────┬───────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
       ┌─────────────────┐   ┌─────────────────┐
       │ DAILY BRIEF     │   │ EXECUTIVE Q&A  │
       └─────────────────┘   └─────────────────┘

🔍 Key Features

1. Commitment Isolation

The system identifies commitments specifically made by Arjun Malhotra.

Example categories:

Commitment
├── Action
├── Owner
├── Deadline
├── Recipient / Stakeholder
├── Status
├── Source
└── Evidence

This prevents general discussion items from being incorrectly treated as executive commitments.

2. Waiting on Others

The system distinguishes between:

🟢 My Actions

Actions that Arjun needs to complete.

🟡 Waiting on Others

Actions blocked by another person or dependency.

Example:

Action: Receive updated numbers
Owner: Divya Kapoor
Waiting on: Divya Kapoor
Status: Waiting on Others

This allows the executive to immediately see what is blocked without confusing it with their own pending work.

3. Chronological Deadline Resolution

Deadlines can change across channels.

For example:

Original:
Acme proposal → Wednesday 5:00 PM

Later update:
Acme proposal → Thursday 2:00 PM

Completion evidence:
Delivered → Thursday 1:30 PM

The system processes evidence chronologically and uses the latest valid deadline when determining the final state.

This prevents outdated deadlines from incorrectly appearing as overdue.

4. Cross-Channel Deduplication

The same action may appear in:

Meeting transcript
       ↓
Email thread
       ↓
Voice note
       ↓
Calendar

Instead of creating four separate tasks, the system attempts to consolidate them into a single canonical action with multiple evidence references.

                 ┌───────────────┐
                 │ Canonical     │
                 │ Action        │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       Meeting         Email        Voice Note
       Evidence        Evidence      Evidence

🚨 Action State Model

Every action is classified into an operational state:

                 ┌─────────────┐
                 │   ACTION    │
                 └──────┬──────┘
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
      Completed      Pending       Waiting
                        │           on Others
                        │
                        ▼
                     Overdue

Supported States

🟢 Completed

🔵 Pending

🟡 Waiting on Others

🔴 Overdue

⚪ Unassigned

👤 Ownership Resolution

The system explicitly checks whether every action has a clear owner.

For example:

Action:
Zenith security audit compliance review

Owner:
❓ Unassigned

System:
⚠️ Ownership requires clarification

This prevents important actions from disappearing into ambiguous meeting notes.

📊 Daily Executive Action Brief

The Streamlit dashboard provides an executive-level summary for each day in the Data Pack window.

Available dates

21 Sep 2026
22 Sep 2026
23 Sep 2026
24 Sep 2026
25 Sep 2026

The selected day can surface:

┌──────────────────────────────────────────────┐
│           EXECUTIVE ACTION BRIEF             │
├──────────────────────────────────────────────┤
│ 🔴 Overdue                                  │
│ 🟡 Waiting on Others                        │
│ 🔵 Pending                                  │
│ 🟢 Completed                                │
│ ⚪ Unassigned                               │
├──────────────────────────────────────────────┤
│ Today's Commitments                          │
│ Upcoming Deadlines                           │
│ Dependencies                                 │
│ Completion Evidence                          │
└──────────────────────────────────────────────┘

💬 Grounded Executive Q&A

The Executive AI Assistant supports questions such as:

What did I promise Raghav?

What needs action today?

What am I waiting for?

What is overdue?

What is unassigned?

The Q&A layer is designed to remain grounded in the supplied Data Pack rather than generating unsupported information.

Evidence-backed response structure

Question
   ↓
Intent Detection
   ↓
Relevant Actions
   ↓
Source Evidence
   ↓
Grounded Answer
   ↓
Evidence Citation

🔐 Source Grounding & Auditability

A key design principle is:

No source evidence → No factual answer.

The system maintains traceability between an action and its original evidence.

Action
  │
  ├── Source Type
  ├── Source ID
  ├── Timestamp
  ├── Evidence Text
  └── Metadata

This makes the system more suitable for executive workflows where explainability and auditability matter.

🏗️ Project Architecture

executive_productivity_agent/
│
├── 📁 data/
│   └── data_pack.json
│       └── Single source of truth
│
├── 📁 database/
│   ├── __init__.py
│   └── db_manager.py
│       └── SQLite persistence & evidence traces
│
├── 📁 agent/
│   ├── __init__.py
│   ├── data_loader.py
│   │   └── Data parsing & normalization
│   │
│   ├── extractor.py
│   │   └── Commitment & deadline extraction
│   │
│   ├── deduplicator.py
│   │   └── Cross-channel deduplication
│   │
│   ├── state_manager.py
│   │   └── Action state classification
│   │
│   ├── brief_generator.py
│   │   └── Daily executive brief generation
│   │
│   └── qa_engine.py
│       └── Grounded executive Q&A
│
├── 📄 app.py
│   └── Streamlit application
│
├── 📄 requirements.txt
│   └── Python dependencies
│
├── 📄 .env.example
│   └── Environment configuration template
│
└── 📄 README.md
    └── Project documentation

🛠️ Technology Stack

Technology

Purpose

🐍 Python

Core application logic

🎈 Streamlit

Interactive executive dashboard

🗄️ SQLite

Local action & evidence persistence

🤖 Gemini API

Optional AI-assisted extraction

📦 JSON

Source Data Pack

🔍 Deterministic Rules

Reliable extraction/state logic

📊 Pandas

Data processing and transformation

🚀 Getting Started

Prerequisites

Python 3.9+

pip

Git

1️⃣ Clone the Repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd executive_productivity_agent

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Configure Environment

Optional Gemini API configuration:

cp .env.example .env

Then add your API key to .env.

No API key is required for Deterministic Demo Mode.

The application can run directly against the supplied data/data_pack.json.

4️⃣ Run the Application

streamlit run app.py

Open:

http://localhost:8501

🖥️ Streamlit Application

The application is organized into multiple executive-focused views.

📊 Daily Action Brief

Select a date to inspect:

Active commitments

Pending actions

Completed actions

Overdue items

Waiting dependencies

Unassigned actions

💬 Executive AI Assistant

Ask natural-language questions and receive grounded responses with evidence.

🔍 Action & Evidence Matrix

Inspect the relationship between:

Action ↔ Owner ↔ Deadline ↔ Status ↔ Source Evidence

📁 Data Pack Inspector

Explore the underlying:

People & email addresses

Leadership Sync transcript

Arjun calendar

Neha calendar

Email threads

Voice notes

⚡ System Audit & Pipeline

Inspect the processing pipeline and SQLite-backed action/evidence records.

🧪 Deterministic Demo Mode

The project includes a deterministic processing path designed to make the application reproducible without depending entirely on an external LLM.

data_pack.json
      ↓
Deterministic Extraction
      ↓
Normalization
      ↓
Deduplication
      ↓
State Resolution
      ↓
SQLite
      ↓
Streamlit

This provides a reliable baseline while keeping optional AI-assisted extraction available.

📌 Example Executive Questions

"What did I promise Raghav?"

"What needs action today?"

"What am I waiting for?"

"What is overdue?"

"What is unassigned?"

"Which deadlines changed?"

"What commitments were completed?"

"Show me actions due today."

🎯 Design Principles

The project is built around five principles:

1. Evidence First

Every important action should have traceable source evidence.

2. Chronology Matters

Later evidence can update earlier commitments and deadlines.

3. One Action, Multiple Sources

Duplicate mentions should resolve into one canonical action.

4. State Over Noise

Executives should see what requires attention rather than raw communication volume.

5. Grounded Answers

The assistant should answer from the supplied evidence rather than inventing business facts.

📈 End-to-End Workflow

       MULTI-MODAL BUSINESS DATA
                  │
                  ▼
        ┌──────────────────┐
        │   DATA LOADER    │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │    EXTRACTOR     │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │  DEDUPLICATION   │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │ DEADLINE / OWNER │
        │    RESOLUTION    │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │  STATE MANAGER   │
        └────────┬─────────┘
                 ▼
        ┌──────────────────┐
        │      SQLITE      │
        └────────┬─────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌───────────────┐  ┌────────────────┐
│ DAILY BRIEFS  │  │ GROUNDED Q&A   │
└───────────────┘  └────────────────┘
        │                 │
        └────────┬────────┘
                 ▼
       EXECUTIVE DECISION SUPPORT

🏆 Assignment Requirements Coverage

Requirement

Implementation

Multi-source Data Pack

✅

Commitment extraction

✅

Deadline extraction

✅

Deadline updates

✅

Cross-channel deduplication

✅

Ownership detection

✅

Waiting-on-others tracking

✅

Overdue detection

✅

Completion detection

✅

Daily executive brief

✅

Grounded Q&A

✅

Source evidence

✅

SQLite persistence

✅

Interactive Streamlit UI

✅

AI-assisted extraction

✅ Optional

Deterministic fallback

✅

Auditability

✅

🔮 Future Enhancements

Potential extensions include:

🔔 Automated deadline reminders

📧 Live email/calendar integrations

🧠 More advanced semantic deduplication

📱 Mobile-friendly executive dashboard

🔐 Role-based access control

📈 Executive workload analytics

🔄 Real-time event ingestion

🤖 Autonomous follow-up generation

📅 Calendar-aware priority ranking

🔗 Enterprise communication integrations

👩‍💻 Built For

AGENTIC AI FACTORY — AIONOS

Executive Productivity Agent

Focus: Agentic AI • Information Extraction • Workflow Automation • Grounded Q&A • Executive Decision Support

⭐ Key Takeaway

This project demonstrates how an agent can transform messy, distributed business communication into a structured executive action layer — identifying what was promised, who owns it, when it is due, what has changed, what is blocked, and what still requires attention.
