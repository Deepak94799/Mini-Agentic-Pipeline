# Slide 1 - Title
Mini Agentic Pipeline - Demo

# Slide 2 - Objective
- Retrieve KB context
- Reason & decide using LLM
- Execute tool actions (CSV/REST)
- Produce trace & evaluation

# Slide 3 - Architecture
Retriever -> Reasoner -> Planner -> Actor (tool)

# Slide 4 - Demo commands
- pip install -r requirements.txt
- set OPENAI_API_KEY in .env
- python run_demo.py

# Slide 5 - Evaluation artifacts
- outputs/logs.json
- outputs/latency_report.csv
- outputs/evaluation_notes.json

# Slide 6 - Limitations & Next Steps
- FAISS on Windows fallback
- Add richer agents, memory, web search tool

# Slide 7 - Thank you
Contact: (put your info)