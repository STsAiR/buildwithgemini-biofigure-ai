# 🧬 BioFigure AI — Biomedical Mechanism Figure & Abstract Agent

BioFigure AI is an agent-first application designed to help biomedical researchers conceptualize, verify, catalog, and generate publication-grade mechanism diagrams, pathway schematics, and graphical abstracts.

Built on Google Cloud with the **Agent Development Kit (ADK)** and `agents-cli`, the agent connects foundation models to structured databases, long-term memory, scientific literature APIs, code execution sandboxes, and cloud storage.

---

## 🌟 Key Capabilities & Wired Google Cloud Services

The capabilities below are fully implemented and wired into the agent's reasoning loop:

### 1. 🤖 Conversational Agent & Reasoning Loop
* **Foundation Model**: Powered by `gemini-3.8-flash` via Vertex AI.
* **Architecture**: Built using Google ADK with the native **Agent-to-Agent (A2A)** protocol.
* **Orchestration**: Configured to analyze researcher requests, look up scientific literature, manage structured catalog records, execute code, and synthesize visual prompts.

### 2. 🧠 Cross-Session Long-Term Memory (Vertex AI Memory Bank)
* **Read (`PreloadMemoryTool`)**: Injects user preferences, recurring pathways of interest, and prior figure iterations into the conversation context at session start.
* **Write (`generate_memories_callback`)**: Automatically extracts and persists relevant facts, journal style requirements, and project context to the managed Memory Bank service after each turn.

### 3. 🗄️ Biomedical Mechanism Catalog (Google Cloud Firestore)
* **`list_mechanism_figures`**: Browse cataloged figures with keyword filtering across titles, topics, and biological systems.
* **`get_mechanism_figure`**: Retrieve complete structured records, including cellular compartments, molecular actors, causal flow, and synthesized BioRender prompts.
* **`save_mechanism_figure`**: Create or update figure records in Firestore with automated prompt synthesis.
* **`search_figures_by_biological_actor`**: Query figures by specific proteins, receptors, cell types, or therapeutic agents (e.g., PD-1, cGAS-STING, HIF-1α).

### 4. 📚 Literature Grounding (NCBI PubMed API)
* **`search_pubmed_literature`**: Connects directly to the NCBI Entrez E-Utilities API (`esearch` and `esummary`) to search peer-reviewed biomedical literature, retrieving PMIDs, titles, journals, and publication dates to ground proposed mechanisms on published empirical evidence.

### 5. 🎨 Multimodal Image Generation & Asset Storage (Google Cloud Storage)
* **`generate_mechanism_figure_image`**: Generates biomedical figures using Gemini image generation models:
  * `gemini-3.1-flash-lite-image` for rapid schematic preview.
  * `gemini-3-pro-image` for high-resolution publication output.
* **Cloud Storage**: Uploads generated images to a dedicated Cloud Storage bucket and generates public HTTPS URLs.
* **Artifact Tracking**: Persists image bytes to ADK session artifacts and updates the Firestore figure record with the public asset URL.

### 6. 🧪 Isolated Code Sandbox (Agent Engine Sandbox)
* **`AgentEngineSandboxCodeExecutor`**: Safely executes Python code within a managed serverless sandbox on the Agent Engine for kinetic modeling, pathway node calculations, and biological computations.

### 7. 🪟 Agent-First User Interface (A2UI v0.8) & Chat Frontend
* **A2UI v0.8 Schema**: Formats visual responses into declarative UI component trees using `A2uiSchemaManager` and the Basic Catalog (Card, Column, Row, Text, Image).
* **FastAPI Proxy & Chat UI**: A lightweight proxy in `frontend/` that communicates with the deployed agent over A2A and serves a clean web interface that natively renders A2UI cards.

---

## 📋 Features Roadmap & Status

| Feature | Status | Implementation Details |
|---|---|---|
| **Firestore Figure Catalog** | ✅ Implemented | Full CRUD & search via `app/firestore_service.py` |
| **NCBI PubMed Search** | ✅ Implemented | Live E-Utilities integration via `app/pubmed_service.py` |
| **Cloud Storage Image Pipeline** | ✅ Implemented | Dual artifact & GCS upload via `app/image_service.py` |
| **Vertex AI Memory Bank** | ✅ Implemented | Preload tool and post-agent memory callbacks |
| **Agent Engine Code Sandbox** | ✅ Implemented | Managed Python sandbox executor |
| **A2UI v0.8 Card Rendering** | ✅ Implemented | Basic Catalog schema + callback formatting |
| **FastAPI A2A Proxy Frontend** | ✅ Implemented | Standalone client in `frontend/` |
| **Multimodal PDF Paper Parser** | ⏳ Planned, not yet implemented | Direct PDF upload and section extraction |
| **Interactive Pathway Graph Editor**| ⏳ Planned, not yet implemented | SVG / Mermaid graph editing tool |

---

## 🛠️ Project Structure

```
.
├── project_brief.md                 # Project vision, domain scope, and tool coverage
├── simple-agent/                    # Core ADK agent project
│   ├── agents-cli-manifest.yaml     # Agent deployment manifest
│   ├── pyproject.toml               # Python dependencies and UV configuration
│   ├── app/
│   │   ├── agent.py                 # Root agent definition, system prompts, and tools
│   │   ├── a2ui_utils.py            # A2UI after_model_callback formatting
│   │   ├── firestore_service.py     # Firestore catalog operations
│   │   ├── image_service.py         # Image generation and Cloud Storage upload
│   │   ├── pubmed_service.py        # NCBI PubMed literature search
│   │   └── app_utils/               # Memory and session service builders
│   └── tests/unit/                  # Unit test suite (Firestore, Memory, A2UI, Sandbox, PubMed)
└── frontend/                        # Web chat interface
    ├── main.py                      # FastAPI proxy communicating over A2A
    ├── requirements.txt             # Proxy dependencies
    └── static/
        └── index.html               # Chat interface with built-in A2UI renderer
```

---

## 🚀 Getting Started Locally

### Prerequisites

* Python 3.11+
* `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
* Google Cloud SDK (`gcloud`) authenticated with Application Default Credentials:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```

### 1. Run the Agent Playground Locally

To launch the local development playground with the managed Memory Bank connected:

```bash
cd simple-agent
uv run adk web . --port 8080 --reload_agents --memory_service_uri=agentengine://<YOUR_AGENT_ENGINE_ID>
```

### 2. Run the Chat Frontend Locally

In a separate terminal, launch the FastAPI proxy and chat interface:

```bash
cd frontend
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

export AGENT_ENGINE_RESOURCE_NAME="projects/<PROJECT_ID>/locations/<REGION>/reasoningEngines/<AGENT_ENGINE_ID>"
export AGENT_DIRECTORY="app"
export PORT=8081

python main.py
```

### 3. Run the Unit Test Suite

Execute the automated test suite covering all services and tools:

```bash
cd simple-agent
uv run pytest tests/unit/
```
