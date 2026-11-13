# 🔥 Cadent Gas | Predictive Pipeline Leakage Intelligence Console

> Shifting utility gas networks from reactive customer complaints to proactive, AI-driven asset integrity. Built with Streamlit, LangChain, LangSmith, and Google Material Design 3.0.

---

## 💡 The Story & Motivation

Traditional gas distribution networks (like Cadent Gas managing over 500,000+ pipeline assets) have historically relied on a reactive workflow: a pipe joint corrodes, gas escapes underground, and field crews are only dispatched *after* a member of the public smells gas and makes an emergency call. 

By that point, public safety and regulatory compliance are already under immense pressure. 

For this assignment, I wanted to build something that bridges **Generative AI architecture** with a real-world, life-critical problem. This dashboard analyzes **Minimum Night Flow (MNF) SCADA pressure drops** and **pipe metallurgy/age** (e.g., 50+ year Cast Iron vs. modern Polyethylene) to flag high-risk leaks *days before* a surface odor threshold or hazardous incident ever occurs.

---

## 🛠️ Tech Stack & Architecture

* **Orchestration & LLM:** LangChain paired with OpenAI (`gpt-4o-mini`).
* **Deterministic Structured Outputs:** Pydantic (`with_structured_output`) to enforce strict JSON schemas for risk scoring, breach time windows, and work orders—avoiding fragile text parsing.
* **Zero-Code Observability:** Full LangSmith tracing configured entirely via environment variables (`LANGSMITH_TRACING`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`) for real-time latency and token monitoring without cluttering business logic.
* **User Interface & Design System:** Python Streamlit styled from the ground up using **Google Material Design 3.0 (Material You)** principles—light-mode surface containers, semantic tonal status pills, and clear visual hierarchy.
* **Data & Visualization:** Pandas for sensor telemetry processing and **Plotly** for interactive pressure-decay charts and 24-hour asset trend curves.

---

## ✨ Key Features

1. **Clean Pre-Scan Telemetry Readiness:** Greets operators with a professional system status summary before executing heavy model inference.
2. **Session State Persistence (`st.session_state`):** Ensures UI interactions, filters, and tab switches don't reset your active AI predictions.
3. **Interactive Severity Filtering & CSV Export:** Filter assets instantly by risk tier (`CRITICAL`, `ELEVATED`, `NORMAL`) and download work-order schedules for field teams with one click.
4. **Asset Drill-Down & Crew Dispatch Simulator:** Select any pipeline segment to inspect its 24-hour pressure decay profile and authorize preventive crew dispatches in real-time.

---
