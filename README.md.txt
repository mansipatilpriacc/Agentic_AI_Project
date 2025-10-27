Multi-Agent AI System

Project: Multi-Agent AI System (ResearchAgent, WriterAgent, CriticAgent, Orchestrator)

Overview:
This repository contains a modular multi-agent system for automated research, draft generation, and critique/editing. The system is built to orchestrate multiple agents with distinct responsibilities so they can collaborate on content creation and review workflows.

Primary agents:
ResearchAgent: Gathers and structures factual information and references.
WriterAgent: Produces first-draft content from research notes and prompts.
CriticAgent (Editor): Reviews drafts, suggests edits, and enforces style/quality.
Orchestrator: Coordinates the pipeline, passing data between agents and handling retries, logging, and error states.

Features:

Modular agent architecture — easy to add or replace agents.
Clear separation of concerns: research → writing → critique.
Logging and retry mechanisms for robustness.
Configurable prompts, model settings, and output formats.
Pluggable backends for models (local, cloud API, or mock/dummy agents for testing).

Project Structure:
├── agents/
│ ├── research_agent.py
│ ├── writer_agent.py
│ ├── critic_agent.py
│ └── base_agent.py
├── orchestrator.py
├── configs/
│ └── default.yaml
├── examples/
│ └── sample_run.json
├── tests/
├── requirements.txt
└── README.md

Quick Start
Prerequisites

Python 3.9+
pip
(Optional) virtualenv or venv

# create a venv (recommended)
python -m venv .venv
source .venv/bin/activate # macOS / Linux
.\.venv\Scripts\activate # Windows


# install dependencies
pip install -r requirements.txt

Configuration
Edit configs/default.yaml to change agent behavior, model keys, or timeouts. Example config keys:

model:
provider: openai
model_name: gpt-4o
agents:
research:
max_results: 10
writer:
tone: neutral
critic:
enforce_style_guide: true
logging:
level: INFO

Running locally (example)
# Run the orchestrator which executes the pipeline
python orchestrator.py --config configs/default.yaml --task "Benefits of AI in healthcare"

Usage Examples

Single task run (CLI): python orchestrator.py --task "Explain transformers in simple terms"
Programmatic API (Python):

from orchestrator import Orchestrator
orc = Orchestrator(config_path="configs/default.yaml")
result = orc.run(task_title="Benefits of AI in healthcare")
print(result['final_text'])

Output Formats
Agents can emit outputs in multiple formats. Configure orchestrator to write results to:
Plain .txt file
Markdown .md
JSON with metadata (timestamps, agent logs, citations)
Example examples/sample_run.json shows the pipeline output with fields like research_notes, draft, critic_comments, and final_text.


