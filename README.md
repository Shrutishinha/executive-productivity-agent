
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&height=210&color=gradient&customColorList=12,14,16,18&text=EXECUTIVE%20AI%20AGENT&fontSize=44&fontColor=ffffff&animation=twinkling&fontAlignY=42" width="100%"/>

<br>
### 🧠 From scattered business communication → structured executive action

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=17&duration=2200&pause=700&color=8B5CF6&center=true&vCenter=true&width=900&lines=Processing+business+signals...;Extracting+executive+commitments...;Resolving+ownership+%26+deadlines...;Detecting+duplicates+%26+dependencies...;Tracking+actions+with+evidence...;Generating+grounded+executive+intelligence..." />

<br><br>
<br><br>

<img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/> <img src="https://img.shields.io/badge/SQLite-Persistence-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/> <img src="https://img.shields.io/badge/Gemini-Optional%20AI-8E75B2?style=for-the-badge&logo=google&logoColor=white"/>

<br><br>

<img src="https://img.shields.io/badge/AGENTIC_AI-8B5CF6?style=flat-square"/> <img src="https://img.shields.io/badge/GROUNDED_Q%26A-6366F1?style=flat-square"/> <img src="https://img.shields.io/badge/EVIDENCE_FIRST-7C3AED?style=flat-square"/> <img src="https://img.shields.io/badge/AUDITABLE-22C55E?style=flat-square"/> <img src="https://img.shields.io/badge/DETERMINISTIC_FALLBACK-F59E0B?style=flat-square"/>

<br><br>
<img src="https://skillicons.dev/icons?i=python,streamlit,sqlite,pandas&theme=light" />

<br><br>

![Status](https://img.shields.io/badge/Status-Working%20Prototype-8B5CF6?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Grounded%20Q%26A-6366F1?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Agentic-7C3AED?style=for-the-badge)
![Data](https://img.shields.io/badge/Data-Multi--Source-9333EA?style=for-the-badge)

<br>

**AI • Automation • Executive Decision Support • Information Extraction • Grounded Q&A**

</div>

---

# 🚀 Executive AI Agent

> **A grounded executive productivity agent that converts messy, distributed business communication into a structured action layer.**

Executives rarely receive information in one place.

Important commitments can be distributed across:

* 📨 Emails
* 🗓️ Calendar events
* 📝 Meeting transcripts
* 🎙️ Voice notes

The result is information overload, duplicated commitments, changing deadlines, unclear ownership, and actions that are easy to miss.

**Executive AI Agent transforms these scattered signals into one evidence-backed operational view.**

---

# ⚡ What It Does

```text
                    MULTI-SOURCE BUSINESS SIGNALS
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
           Emails           Meetings         Calendars
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                         Voice Notes
                               │
                               ▼
                    ┌────────────────────┐
                    │   AI + RULE ENGINE │
                    └─────────┬──────────┘
                              ▼
                ┌─────────────────────────┐
                │ Extract • Normalize      │
                │ Deduplicate • Resolve    │
                │ Track • Verify           │
                └────────────┬────────────┘
                             ▼
                   ┌───────────────────┐
                   │ ACTION INTELLIGENCE│
                   └─────────┬─────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
     Daily Brief        Action Matrix      Grounded Q&A
          │                  │                  │
          └──────────────────┼──────────────────┘
                             ▼
                  EXECUTIVE DECISION SUPPORT
```

---

# 🎯 Core Capabilities

| Capability                         | What the Agent Does                                        |
| ---------------------------------- | ---------------------------------------------------------- |
| 🔎 **Commitment Extraction**       | Identifies concrete commitments and actions                |
| 👤 **Ownership Resolution**        | Determines who is responsible for an action                |
| 🤝 **Dependency Tracking**         | Detects actions waiting on other people                    |
| ⏰ **Deadline Detection**           | Extracts dates and times from multiple sources             |
| 🔄 **Deadline Resolution**         | Uses later valid evidence when deadlines change            |
| 🧩 **Cross-Channel Deduplication** | Consolidates repeated references to the same action        |
| 🚨 **Overdue Detection**           | Identifies incomplete actions past their resolved deadline |
| ✅ **Completion Detection**         | Uses evidence to determine whether an action was completed |
| ⚠️ **Ambiguity Detection**         | Flags actions with unclear ownership or intent             |
| 📊 **Daily Executive Brief**       | Converts action data into a date-specific summary          |
| 💬 **Grounded Q&A**                | Answers questions using verified Data Pack evidence        |
| 🔗 **Evidence Traceability**       | Links actions back to their source evidence                |

---

# 🧠 Intelligence Pipeline

The system separates **information extraction**, **entity/action resolution**, and **state management**.

```text
┌──────────────────────────┐
│      DATA PACK           │
│    data_pack.json        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      DATA LOADER         │
│ Parse • Normalize • Map  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       EXTRACTOR          │
│ Actions • Owners         │
│ Deadlines • Dependencies │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      RESOLUTION          │
│ Deduplication            │
│ Deadline Updates         │
│ Ownership Resolution     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      STATE MANAGER       │
│ Pending • Waiting        │
│ Completed • Overdue      │
│ Unassigned               │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       SQLITE STORE       │
│ Actions + Evidence       │
└────────────┬─────────────┘
             │
        ┌────┴─────┐
        ▼          ▼
┌─────────────┐ ┌──────────────┐
│ DAILY BRIEF │ │ GROUNDED Q&A │
└─────────────┘ └──────────────┘
```

---

# 🔍 How the Agent Thinks

## 1. Commitment Isolation

The system focuses on **actionable commitments**, rather than treating every sentence in a meeting or email as a task.

```text
Commitment
│
├── Action
├── Owner
├── Deadline
├── Stakeholder
├── Status
├── Source
└── Evidence
```

This helps separate:

```text
Discussion
   ❌
   ↓
"Maybe we should review the proposal."

Commitment
   ✅
   ↓
"Arjun will send the revised proposal by Thursday."
```

---

## 2. Ownership & Dependency Resolution

The agent distinguishes between actions that belong to the executive and actions blocked by someone else.

### My Action

```text
Action: Send revised proposal
Owner:  Arjun Malhotra
State:  Pending
```

### Waiting on Others

```text
Action: Receive updated numbers
Owner:  Divya Kapoor
Waiting on: Divya Kapoor
State:  Waiting on Others
```

This allows the executive to see **what they need to do** separately from **what they are waiting to receive**.

---

# ⏰ 3. Chronological Deadline Resolution

Business commitments can evolve over time.

Example:

```text
09:00 AM
Original deadline
Acme proposal → Wednesday 5:00 PM

        ↓

02:00 PM
Updated commitment
Acme proposal → Thursday 2:00 PM

        ↓

01:30 PM Thursday
Completion evidence
Acme proposal → Delivered
```

The system processes evidence chronologically.

### Resolution principle

```text
Earlier evidence
       ↓
Later evidence
       ↓
Updated canonical action
       ↓
Final operational state
```

This prevents obsolete deadlines from incorrectly triggering overdue states.

---

# 🧩 4. Cross-Channel Deduplication

A single action can appear in several communication channels.

```text
Meeting Transcript
        │
        ▼
    ┌───────────┐
    │           │
Email ───────► │ Canonical │ ◄──── Voice Note
    │           │  Action   │
Calendar ────► │           │
    │           └───────────┘
    │
    ▼
Multiple Evidence References
```

Instead of creating four independent tasks, the system attempts to consolidate them into:

> **One canonical action + multiple supporting evidence records**

---

# 🚦 Action State Model

Every action is resolved into an operational state.

```text
                         ┌─────────────┐
                         │    ACTION   │
                         └──────┬──────┘
                                │
          ┌─────────────┬───────┼──────────────┐
          ▼             ▼       ▼              ▼
      Completed      Pending  Waiting       Unassigned
                              on Others
                                │
                                ▼
                             Overdue
```

| State                    | Meaning                                                  |
| ------------------------ | -------------------------------------------------------- |
| 🟢 **Completed**         | Verified completion evidence exists                      |
| 🔵 **Pending**           | Active action that is not yet overdue                    |
| 🟡 **Waiting on Others** | Progress depends on another person                       |
| 🔴 **Overdue**           | Resolved deadline has passed without completion evidence |
| ⚪ **Unassigned**         | No reliable owner has been identified                    |

---

# 👤 Ownership Resolution

Ambiguous ownership is explicitly surfaced rather than silently ignored.

Example:

```text
Action:
Zenith security audit compliance review

Owner:
❓ Unassigned

System:
⚠️ Ownership requires clarification
```

This prevents important actions from disappearing inside meeting notes.

---

# 📊 Daily Executive Brief

The Streamlit dashboard converts the underlying action database into a date-specific executive view.

### Available Data Pack Dates

```text
21 Sep 2026
22 Sep 2026
23 Sep 2026
24 Sep 2026
25 Sep 2026
```

### Daily View

```text
╭────────────────────────────────────────────╮
│          EXECUTIVE ACTION BRIEF            │
├────────────────────────────────────────────┤
│ 🔴 Overdue                                 │
│ 🟡 Waiting on Others                       │
│ 🔵 Pending                                 │
│ 🟢 Completed                               │
│ ⚪ Unassigned                              │
├────────────────────────────────────────────┤
│ Today's Commitments                        │
│ Upcoming Deadlines                         │
│ Dependencies                               │
│ Completion Evidence                        │
╰────────────────────────────────────────────╯
```

The goal is simple:

> **Surface what requires attention without forcing the executive to read every source.**

---

# 💬 Grounded Executive Q&A

The assistant supports natural-language questions such as:

```text
"What did I promise Raghav?"

"What needs action today?"

"What am I waiting for?"

"What is overdue?"

"What is unassigned?"

"Which deadlines changed?"

"What commitments were completed?"
```

### Q&A Pipeline

```text
User Question
      │
      ▼
Intent Detection
      │
      ▼
Relevant Actions
      │
      ▼
Evidence Retrieval
      │
      ▼
Grounded Answer
      │
      ▼
Source Evidence
```

The Q&A layer is designed to answer from the supplied **Data Pack and resolved action records**, rather than inventing unsupported business facts.

---

# 🔐 Evidence-First Architecture

One of the core principles of the system is:

> **No supporting evidence → No factual business claim.**

Each action maintains a traceable relationship with its originating evidence.

```text
ACTION
  │
  ├── Action ID
  ├── Owner
  ├── Deadline
  ├── Status
  │
  └── Evidence
       ├── Source Type
       ├── Source ID
       ├── Timestamp
       ├── Evidence Text
       └── Metadata
```

This makes the system more explainable and auditable than a purely generative assistant.

---

# 🏗️ Project Architecture

```text
executive_productivity_agent/
│
├── 📁 data/
│   └── data_pack.json
│
├── 📁 database/
│   ├── __init__.py
│   └── db_manager.py
│
├── 📁 agent/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── extractor.py
│   ├── deduplicator.py
│   ├── state_manager.py
│   ├── brief_generator.py
│   └── qa_engine.py
│
├── 📄 app.py
├── 📄 requirements.txt
├── 📄 .env.example
└── 📄 README.md
```

### Module Responsibilities

| Module               | Responsibility                                      |
| -------------------- | --------------------------------------------------- |
| `data_loader.py`     | Parse and normalize source data                     |
| `extractor.py`       | Extract actions, deadlines, owners and dependencies |
| `deduplicator.py`    | Consolidate repeated actions                        |
| `state_manager.py`   | Resolve operational state                           |
| `brief_generator.py` | Generate daily executive summaries                  |
| `qa_engine.py`       | Answer grounded executive questions                 |
| `db_manager.py`      | Persist actions and evidence                        |
| `app.py`             | Streamlit interface                                 |

---

# 🛠️ Technology Stack

| Technology                 | Role                                    |
| -------------------------- | --------------------------------------- |
| 🐍 **Python**              | Core application and agent logic        |
| 🎈 **Streamlit**           | Interactive executive dashboard         |
| 🗄️ **SQLite**             | Action and evidence persistence         |
| 🤖 **Gemini API**          | Optional AI-assisted extraction         |
| 📦 **JSON**                | Structured source Data Pack             |
| 🔍 **Deterministic Rules** | Reproducible state and resolution logic |
| 📊 **Pandas**              | Data processing and transformation      |

---

# 🤖 AI + Deterministic Hybrid Design

The project intentionally does **not** depend entirely on an LLM.

```text
             DATA PACK
                 │
        ┌────────┴────────┐
        ▼                 ▼
 Deterministic        Optional AI
    Logic             Assistance
        │                 │
        └────────┬────────┘
                 ▼
          Normalized Actions
                 │
                 ▼
        Deterministic State
           Resolution
                 │
                 ▼
             SQLite
                 │
        ┌────────┴────────┐
        ▼                 ▼
    Daily Brief       Grounded Q&A
```

### Why this architecture?

| Approach               | Role                                         |
| ---------------------- | -------------------------------------------- |
| Deterministic logic    | Reproducibility, state resolution, deadlines |
| AI-assisted extraction | Flexible interpretation of unstructured text |
| SQLite                 | Persistent structured state                  |
| Evidence layer         | Traceability and grounding                   |

This creates a more controlled workflow than using an LLM as the sole source of truth.

---

# 🧪 Deterministic Demo Mode

The project includes a deterministic processing path that can run without an external LLM.

```text
data_pack.json
      ↓
Deterministic Extraction
      ↓
Normalization
      ↓
Deduplication
      ↓
Deadline / Owner Resolution
      ↓
State Classification
      ↓
SQLite
      ↓
Streamlit
```

### Benefits

* Reproducible demo
* No API dependency
* Easier debugging
* Explainable state transitions
* Consistent assignment evaluation

---

# 🖥️ Streamlit Application

The dashboard is organized around the executive workflow.

### 📊 Daily Action Brief

Inspect:

* Today's commitments
* Pending actions
* Completed actions
* Overdue actions
* Waiting dependencies
* Unassigned actions
* Upcoming deadlines

### 💬 Executive AI Assistant

Ask natural-language questions and retrieve evidence-backed answers.

### 🔍 Action & Evidence Matrix

Inspect:

```text
Action
  ↕
Owner
  ↕
Deadline
  ↕
Status
  ↕
Source Evidence
```

### 📁 Data Pack Inspector

Explore:

* People & email addresses
* Leadership Sync
* Arjun's calendar
* Neha's calendar
* Email threads
* Voice notes

### ⚡ System Audit

Inspect:

* Processing pipeline
* Resolved actions
* State transitions
* SQLite records
* Evidence references

---

# 🚀 Getting Started

## Prerequisites

* Python 3.9+
* pip
* Git

## 1. Clone

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd executive_productivity_agent
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Environment

Optional Gemini configuration:

```bash
cp .env.example .env
```

Add the API key to `.env` if AI-assisted extraction is enabled.

> **No API key is required for Deterministic Demo Mode.**

## 4. Run

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# 📌 Example Executive Queries

```text
"What did I promise Raghav?"

"What needs action today?"

"What am I waiting for?"

"What is overdue?"

"What is unassigned?"

"Which deadlines changed?"

"What commitments were completed?"

"Show me actions due today."
```

---

# 🔄 End-to-End Workflow

```text
┌──────────────────────────────┐
│  MULTI-MODAL BUSINESS DATA   │
│ Emails • Meetings • Calendar │
│ Voice Notes                  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│         DATA LOADER          │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│          EXTRACTOR           │
│ Actions • Owners • Deadlines │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│       DEDUPLICATION          │
│     Canonical Actions        │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│   DEADLINE / OWNER RESOLVER  │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│        STATE MANAGER         │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│            SQLITE            │
│     Actions + Evidence       │
└──────────────┬───────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌───────────────┐ ┌───────────────┐
│ DAILY BRIEFS  │ │ GROUNDED Q&A  │
└───────┬───────┘ └───────┬───────┘
        │                 │
        └────────┬────────┘
                 ▼
      EXECUTIVE ACTION LAYER
```

---

# 📋 Assignment Requirements Coverage

| Requirement                 | Implementation |
| --------------------------- | :------------: |
| Multi-source Data Pack      |        ✅       |
| Commitment extraction       |        ✅       |
| Deadline extraction         |        ✅       |
| Deadline updates            |        ✅       |
| Cross-channel deduplication |        ✅       |
| Ownership detection         |        ✅       |
| Waiting-on-others tracking  |        ✅       |
| Overdue detection           |        ✅       |
| Completion detection        |        ✅       |
| Daily executive brief       |        ✅       |
| Grounded Q&A                |        ✅       |
| Source evidence             |        ✅       |
| SQLite persistence          |        ✅       |
| Interactive Streamlit UI    |        ✅       |
| AI-assisted extraction      |   ✅ Optional   |
| Deterministic fallback      |        ✅       |
| Auditability                |        ✅       |

---

# 🧭 Design Principles

### 01 — Evidence First

Every important action should have traceable supporting evidence.

### 02 — Chronology Matters

Later evidence can modify earlier commitments, deadlines, or completion state.

### 03 — One Action, Multiple Sources

Repeated references should resolve into a canonical action rather than multiple duplicate tasks.

### 04 — State Over Noise

The executive interface prioritizes operational state over raw communication volume.

### 05 — Grounded Answers

The assistant should answer from verified project evidence instead of fabricating business facts.

### 06 — Deterministic Where It Matters

Critical state transitions should remain reproducible and inspectable.

---

# 🔮 Future Enhancements

```text
🔔 Automated Deadline Reminders
📧 Live Email & Calendar Integrations
🧠 Semantic Action Deduplication
📱 Mobile Executive Dashboard
🔐 Role-Based Access Control
📈 Executive Workload Analytics
🔄 Real-Time Event Ingestion
🤖 Autonomous Follow-Up Generation
📅 Calendar-Aware Prioritization
🔗 Enterprise Communication Integrations
```

---

# 🏆 Why This Project Matters

Most productivity tools store tasks.

**This system focuses on reconstructing the task from business context.**

It attempts to answer:

```text
WHAT happened?
       ↓
WHAT was promised?
       ↓
WHO owns it?
       ↓
WHEN is it due?
       ↓
DID the deadline change?
       ↓
IS someone blocking it?
       ↓
WAS it completed?
       ↓
WHERE is the evidence?
```

The result is an **evidence-backed executive action layer** rather than another raw task list.

---

<div align="center">

## 👩‍💻 Built For

### **AGENTIC AI FACTORY — AIONOS**

**Executive Productivity Agent**

<br>

`Agentic AI` • `Information Extraction` • `Workflow Automation` • `Grounded Q&A` • `Executive Decision Support`

<br>

<img src="https://capsule-render.vercel.app/api?type=waving&height=100&section=footer&color=gradient&customColorList=12,14,16,18"/>

</div>
