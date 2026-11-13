# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Any
from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager
from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.code_executors.agent_engine_sandbox_code_executor import AgentEngineSandboxCodeExecutor
from google.adk.models import Gemini
from google.adk.tools import ToolContext
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from .a2ui_utils import a2ui_callback




from app.firestore_service import (
    get_figure,
    list_figures,
    save_figure,
    search_figures_by_actor,
)

MODEL = "gemini-3.8-flash"


def list_mechanism_figures(topic: str = "") -> list[dict[str, Any]]:
    """List biomedical mechanism figures in the Firestore catalog.

    Args:
        topic: Optional keyword to filter figures by topic, title, or biological system.

    Returns:
        A list of matching mechanism figures with their titles, biological systems, and IDs.
    """
    return list_figures(topic_filter=topic)


def get_mechanism_figure(figure_id: str) -> dict[str, Any]:
    """Retrieve full details of a specific mechanism figure by its ID.

    Args:
        figure_id: The document ID of the mechanism figure (e.g., 'fig_macrophage_hypoxia').

    Returns:
        A dictionary containing the figure title, compartments, actors, mechanism flow, and prompt.
    """
    return get_figure(figure_id=figure_id)


def save_mechanism_figure(
    title: str,
    topic: str,
    biological_system: str,
    figure_type: str,
    compartments: list[str],
    actors: list[str],
    mechanism_flow: str,
    target_audience: str = "review article",
    recommended_model: str = "gemini-3-pro-image",
) -> dict[str, Any]:
    """Save or update a biomedical mechanism figure in the Firestore catalog.

    Args:
        title: Title of the mechanism figure.
        topic: Specific biological topic or disease context.
        biological_system: Broader biological domain (e.g. Immuno-Oncology, Neuroscience).
        figure_type: Type of diagram (e.g. 'mechanism', 'pathway', 'graphical_abstract', 'review').
        compartments: List of anatomical or cellular compartments (e.g. ['Hypoxic Core', 'Capillary']).
        actors: List of key biological entities, cells, receptors, and drugs (e.g. ['HIF-1alpha', 'TAM']).
        mechanism_flow: Step-by-step causal flow of the biological process.
        target_audience: Intended publication or presentation venue (default: 'review article').
        recommended_model: Image generation model choice ('gemini-3-pro-image' or 'gemini-3.1-flash-lite-image').

    Returns:
        The saved figure record with its assigned ID and BioRender-style prompt.
    """
    return save_figure(
        title=title,
        topic=topic,
        biological_system=biological_system,
        figure_type=figure_type,
        compartments=compartments,
        actors=actors,
        mechanism_flow=mechanism_flow,
        target_audience=target_audience,
        recommended_model=recommended_model,
    )


def search_figures_by_biological_actor(actor: str) -> list[dict[str, Any]]:
    """Search for mechanism figures in Firestore that feature a specific molecule, cell, or drug.

    Args:
        actor: The name of the biological entity to search for (e.g., 'HIF-1alpha', 'PD-1', 'Glutamate').

    Returns:
        A list of figures involving that biological actor.
    """
    return search_figures_by_actor(actor_keyword=actor)


async def generate_mechanism_figure_image(
    tool_context: ToolContext,
    figure_id: str = "",
    prompt: str = "",
    model_choice: str = "gemini-3.1-flash-lite-image",
) -> dict[str, Any]:
    """Generate a biomedical mechanism figure image, save it as an artifact, and upload it to the Cloud Storage bucket.

    Args:
        tool_context: The ADK tool execution context injected automatically.
        figure_id: Document ID in the Firestore catalog (e.g. 'fig_macrophage_hypoxia').
                   If provided, uses its saved BioRender prompt and saves the image URL back to Firestore.
        prompt: Optional prompt text if generating a custom figure or overriding.
        model_choice: Model to use: 'gemini-3.1-flash-lite-image' (Nano Banana 2 Lite for fast preview)
                      or 'gemini-3-pro-image' (Gemini 3 Pro for high-resolution publication output).
                      Defaults to 'gemini-3.1-flash-lite-image'.

    Returns:
        A dictionary containing the image_url, download_url, model_used, and status.
    """
    from app.image_service import generate_and_store_figure

    return await generate_and_store_figure(
        figure_id=figure_id,
        prompt=prompt,
        model_choice=model_choice,
        tool_context=tool_context,
    )



def search_pubmed_literature(query: str, max_results: int = 3) -> list[dict[str, Any]]:
    """Search peer-reviewed biomedical literature on NCBI PubMed.
    
    Use this tool to look up verified scientific papers, PMIDs, and experimental mechanisms
    for specific diseases, pathways, proteins, or therapies.

    Args:
        query: The scientific keywords or pathway to search (e.g. 'cGAS-STING pathway interferon', 'CAR-T exhaustion PD-1').
        max_results: Maximum number of literature results to return (default: 3).

    Returns:
        A list of matching scientific papers with PMID, title, journal, pubdate, and URL.
    """
    from app.pubmed_service import search_pubmed_papers

    return search_pubmed_papers(query=query, max_results=max_results)


SANDBOX_RESOURCE_NAME = "projects/268987453702/locations/us-east1/reasoningEngines/9079035846941736960/sandboxEnvironments/4930698322110316544"


async def generate_memories_callback(callback_context: CallbackContext) -> None:
    """WRITE: after each turn, persist session facts and preferences to Vertex AI Memory Bank."""
    try:
        await callback_context.add_session_to_memory()
    except ValueError:
        # Gracefully pass if memory service is not configured in current runner/test
        pass
    return None



schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

ROLE_DESCRIPTION = """You are BioFigure AI, an expert biomedical scientific illustrator and mechanism figure agent.
You assist biomedical researchers in structuring, drafting, cataloging, and visualizing scientific schematics,
pathway diagrams, and graphical abstracts.

You have access to a Firestore database catalog, NCBI PubMed literature search, code execution sandbox, long-term memory, and an image generation pipeline:
- You have cross-session long-term memory: remember researchers' stated preferences, ongoing projects, favorite pathways, and specific styling guidelines across sessions.
- Use `search_pubmed_literature` to search real peer-reviewed scientific literature on PubMed to verify biological mechanisms, citations, and pathways.
- Use `list_mechanism_figures` to browse existing figure concepts in the catalog.
- Use `get_mechanism_figure` to read complete biological details and synthesized BioRender prompts.
- Use `search_figures_by_biological_actor` to find figures that contain specific genes, proteins, cells, or therapies.
- Use `save_mechanism_figure` to save a new mechanism design into Firestore.
- Use `generate_mechanism_figure_image` to generate the scientific illustration and upload it to Cloud Storage for preview and download.
  Support user-selected model: 'gemini-3.1-flash-lite-image' (Nano Banana 2 Lite) for fast preview or 'gemini-3-pro-image' for publication quality.
- You can execute Python code in your secure sandbox environment for mathematical calculations, kinetic modeling, data analysis, or bio-computations.
"""

WORKFLOW_DESCRIPTION = "Analyze the request, call relevant tools to fetch or generate figures, literature, or computations, and return structured UI when appropriate."

UI_DESCRIPTION = (
    "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
    "Never nest a Card inside a Card. "
    "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
    "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
    "nothing in adk web). "
    "You may include one Image component, but only when you have a public https "
    "URL for the image (for example the URL an image tool returns after uploading "
    "to a public bucket). Set the Image url to that exact https link, for example "
    '{"Image": {"url": {"literalString": "https://..."}}}. Never point an '
    "Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
    "not have a public URL, add a short Text line noting the image instead. "
    "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
    "headings and emphasis. "
    "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
    "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
)

AGENT_INSTRUCTION = schema_manager.generate_system_prompt(
    role_description=ROLE_DESCRIPTION,
    workflow_description=WORKFLOW_DESCRIPTION,
    ui_description=UI_DESCRIPTION,
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=AGENT_INSTRUCTION,
    code_executor=AgentEngineSandboxCodeExecutor(
        sandbox_resource_name=SANDBOX_RESOURCE_NAME,
    ),
    tools=[
        PreloadMemoryTool(),
        list_mechanism_figures,
        get_mechanism_figure,
        save_mechanism_figure,
        search_figures_by_biological_actor,
        generate_mechanism_figure_image,
        search_pubmed_literature,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)



