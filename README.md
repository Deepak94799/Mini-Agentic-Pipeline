# Submission-ready Mini Agentic Pipeline

This repository is a submission-ready package for an agentic pipeline assignment. It includes:
- Retriever (keyword + FAISS-capable retriever)
- Reasoner (OpenAI ChatCompletion + prompt templates)
- Actor (CSV lookup + optional FastAPI wrapper)
- Planner/Controller orchestrator
- Enhanced logging & per-query latency metrics
- Evaluation scripts and demo materials

## Quick setup (Windows-friendly)

1. Unzip folder and open a PowerShell terminal in the project root.
2. (Optional but recommended) create a virtualenv:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Put your OpenAI key in `.env` (project root):
   ```text
   OPENAI_API_KEY=sk-...
   ```
5. Run demo:
   ```powershell
   python run_demo.py
   ```

## Files of interest
- `run_demo.py` — runs test queries and writes `outputs/logs.json` and `outputs/latency_report.csv`
- `evaluation/run_evaluation.py` — runs tests and generates quality notes template
- `demo/script.txt` — suggested narration for a 5–8 minute demo video
- `demo/slides.md` — simple slide deck to use while recording
- `src/` — core implementation (retriever, reasoner, actor, planner)
- `data/prices.csv` — CSV acting as the tool backing store
- `prompts/` — prompt templates (v1, v2, v3)

## Design decisions (short)
- FAISS is supported but optional (Windows may not install native faiss); pipeline falls back to keyword retriever.
- Prompt versions are stored under `prompts/` and used by the Reasoner; v1 is simple answer-from-KB, v2 is planner JSON, v3 is strict tool-call JSON.
- Actor tool is a CSV lookup validated with Pydantic; a FastAPI wrapper is included as `src/api_actor.py` to demo REST API behavior.
- The Reasoner uses OpenAI ChatCompletion and text-embedding-3-small (for embeddings) when `OPENAI_API_KEY` is present.

## Known limitations
- FAISS installation on Windows can be challenging; fallback to keyword retriever is included.
- The demo video is not recorded (you must record using the `demo/` materials).