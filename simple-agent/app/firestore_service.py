"""Firestore service for BioFigure AI mechanism figure catalog.

Project ID is explicitly hardcoded to prevent Agent Platform runtime
resolution to project numbers which causes Firestore client errors.
"""

from datetime import datetime, timezone
import uuid
from typing import Any
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-e67897557cd7"
COLLECTION_NAME = "mechanism_figures"

# Global Firestore client instance
_db: firestore.Client | None = None


def get_firestore_client() -> firestore.Client:
    """Returns a Firestore client configured with the explicit project ID."""
    global _db
    if _db is None:
        _db = firestore.Client(project=PROJECT_ID)
    return _db


def list_figures(topic_filter: str = "") -> list[dict[str, Any]]:
    """List mechanism figures from Firestore, optionally filtered by keyword."""
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()
    results = []
    filter_lower = topic_filter.lower().strip()

    for doc in docs:
        data = doc.to_dict() or {}
        data["id"] = doc.id
        if not filter_lower:
            results.append(data)
        else:
            title = data.get("title", "").lower()
            topic = data.get("topic", "").lower()
            bio_sys = data.get("biological_system", "").lower()
            if filter_lower in title or filter_lower in topic or filter_lower in bio_sys:
                results.append(data)

    return results


def get_figure(figure_id: str) -> dict[str, Any]:
    """Retrieve a single mechanism figure by document ID."""
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(figure_id)
    doc = doc_ref.get()
    if not doc.exists:
        return {"error": f"Figure with ID '{figure_id}' not found."}
    data = doc.to_dict() or {}
    data["id"] = doc.id
    return data


def save_figure(
    title: str,
    topic: str,
    biological_system: str,
    figure_type: str,
    compartments: list[str],
    actors: list[str],
    mechanism_flow: str,
    target_audience: str = "review article",
    recommended_model: str = "gemini-3-pro-image",
    figure_id: str = "",
) -> dict[str, Any]:
    """Save or update a mechanism figure record in Firestore."""
    db = get_firestore_client()
    doc_id = figure_id.strip() if figure_id.strip() else f"fig_{uuid.uuid4().hex[:8]}"

    # Synthesize BioRender-style prompt structure
    elements_str = ", ".join(actors)
    labels_str = ", ".join(actors[:6])
    recommended_prompt = (
        f"Create a publication-ready biomedical schematic, BioRender-inspired but original.\n"
        f"Topic: {title}.\n"
        f"Audience: {target_audience}.\n"
        f"Canvas: landscape 16:9, clean white background.\n"
        f"Compartments: {', '.join(compartments)}.\n"
        f"Main visual elements: {elements_str}.\n"
        f"Mechanism flow: {mechanism_flow}.\n"
        f"Labels to include exactly: {labels_str}.\n"
        f"Style: ultra-high-resolution, print-ready, crisp vector-like shapes, soft scientific color palette, consistent line weight, clear directional arrows, generous whitespace, large readable labels.\n"
        f"Avoid: photorealistic rendering, 3D glossy plastic, brand logos, copied BioRender icons, fake tiny labels, dark backgrounds."
    )

    doc_data = {
        "title": title,
        "topic": topic,
        "biological_system": biological_system,
        "figure_type": figure_type,
        "compartments": compartments,
        "actors": actors,
        "mechanism_flow": mechanism_flow,
        "target_audience": target_audience,
        "recommended_model": recommended_model,
        "recommended_prompt": recommended_prompt,
        "status": "ready_for_generation",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)
    doc_ref.set(doc_data, merge=True)
    doc_data["id"] = doc_id
    return doc_data


def search_figures_by_actor(actor_keyword: str) -> list[dict[str, Any]]:
    """Search for mechanism figures containing a specific molecule, cell, or target."""
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()
    keyword = actor_keyword.lower().strip()
    matching_figures = []

    for doc in docs:
        data = doc.to_dict() or {}
        data["id"] = doc.id
        actors = [a.lower() for a in data.get("actors", [])]
        if any(keyword in actor for actor in actors) or keyword in data.get("mechanism_flow", "").lower():
            matching_figures.append(data)

    return matching_figures
