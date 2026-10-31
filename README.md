cat > README.md <<'EOF'
# ✨ DevFest Buddy — Your AI-Powered Conference Assistant

> From Gemini to Agents: Building Intelligent Workflows  
> A hands-on demo for DevFest Raipur 2026

Imagine you're attending a developer conference.

There are multiple sessions, overlapping time slots, different topics, and limited time. You want to find the sessions that match your interests—but you also need to make sure your schedule makes sense.

What if you could simply tell an AI assistant what you're interested in and let it help you build a schedule?

Meet **DevFest Buddy** — a small AI agent built with Google's Agent Development Kit (ADK) and Gemini.

---

## 🚀 The Problem

Conference schedules can be difficult to navigate:

- Which sessions match my interests?
- What can I attend between 10 AM and 12 PM?
- Are any of my selected sessions overlapping?
- Is my final schedule actually valid?

A regular chatbot can suggest sessions in a conversation. But an agent can go a step further: it can use tools to search structured data, validate a schedule, and bring the results together.

That's the idea behind this demo.

## 💡 What DevFest Buddy Does

DevFest Buddy helps attendees explore a sample conference agenda and validate a session plan.

It can:

1. **Understand your goal** — identify your topics of interest and available time.
2. **Find relevant sessions** — search the sample agenda using a tool.
3. **Validate your schedule** — check selected sessions for time conflicts.
4. **Explain the result** — return session details and tell you whether the schedule is valid.

The agent uses the sample agenda included in this repository. It should not invent session details.

## 🧠 How It Works

```text
Your Request
     │
     ▼
Gemini Model
     │
     ▼
ADK Agent
     │
     ├── find_sessions()
     │       └── Search the sample agenda
     │
     ├── validate_schedule()
     │       └── Check for overlapping sessions
     │
     ▼
Final Response
Relevant sessions + schedule validation
