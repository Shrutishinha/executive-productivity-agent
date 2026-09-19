# 🤖 AGENTIC AI FACTORY — Executive Productivity Agent

> **An AI-powered Executive Productivity Agent that transforms messy multi-channel business communication into structured, actionable executive intelligence.**

Built for **Arjun Malhotra, VP Sales**, this system analyzes meetings, emails, calendars, and voice notes from **Monday, 21 September 2026 → Friday, 25 September 2026** to identify commitments, deadlines, dependencies, ownership, completion status, and overdue actions.

The agent combines **deterministic processing, structured state management, SQLite persistence, and grounded AI-powered Q&A** to provide an auditable executive workflow.

---

## ✨ What Problem Does It Solve?

Executives receive important information across multiple channels:

* 📨 Emails
* 🗓️ Calendar events
* 📝 Meeting transcripts
* 🎙️ Voice notes

Important commitments can easily become scattered, duplicated, delayed, or unclear.

This agent converts that unstructured information into a **single source of actionable truth**.

### Input → Intelligence → Action

```text
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
```

---

# 🎯 Core Capabilities

| Capability                         | Description                                                          |
| ---------------------------------- | -------------------------------------------------------------------- |
| 🔎 **Commitment Extraction**       | Identifies promises and actions committed to by Arjun                |
| 🤝 **Dependency Tracking**         | Detects actions waiting on Divya, Neha, Raghav, or others            |
| ⏰ **Deadline Detection**           | Extracts deadlines from emails, meetings, calendars, and voice notes |
| 🔄 **Deadline Resolution**         | Applies the latest chronological deadline when commitments change    |
| 🧩 **Cross-Channel Deduplication** | Merges multiple references to the same action                        |
| 🚨 **Overdue Detection**           | Flags incomplete actions whose deadlines have passed                 |
| 👤 **Ownership Detection**         | Identifies actions with unclear or missing ownership                 |
| ✅ **Completion Tracking**          | Detects evidence that an action has been completed                   |
| 📊 **Daily Executive Brief**       | Generates a date-specific action summary                             |
| 💬 **Grounded Q&A**                | Answers executive questions using only verified source evidence      |
| 🔗 **Evidence Traceability**       | Every important answer/action can be traced back to its source       |

---

# 🧠 Intelligence Pipeline

The application follows a structured processing pipeline:

```text
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
```
