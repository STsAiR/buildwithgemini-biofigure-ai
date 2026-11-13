"""Image generation and Cloud Storage service for BioFigure AI.

Generates mechanism figures using Vertex AI image models (gemini-3.1-flash-lite-image
or gemini-3-pro-image) and uploads the result directly to the public GCS bucket.
"""

from datetime import datetime, timezone
import uuid
from typing import Any
from google import genai
from google.cloud import storage
from google.adk.tools import ToolContext
from google.genai import types

from app.firestore_service import get_figure, get_firestore_client, COLLECTION_NAME

PROJECT_ID = "qwiklabs-gcp-04-e67897557cd7"
BUCKET_NAME = "biofigure-figures-e67897557cd7"
DEFAULT_MODEL = "gemini-3.1-flash-lite-image"

# Cache client instances
_genai_client: genai.Client | None = None
_storage_client: storage.Client | None = None


def get_genai_client() -> genai.Client:
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")
    return _genai_client


def get_storage_client() -> storage.Client:
    global _storage_client
    if _storage_client is None:
        _storage_client = storage.Client(project=PROJECT_ID)
    return _storage_client


async def generate_and_store_figure(
    figure_id: str = "",
    prompt: str = "",
    model_choice: str = "gemini-3.1-flash-lite-image",
    tool_context: ToolContext | None = None,
) -> dict[str, Any]:

    """Generates a mechanism figure image and uploads it to the public Cloud Storage bucket.

    Args:
        figure_id: Document ID in Firestore. If provided, fetches the prompt and updates the document.
        prompt: Optional direct prompt. If figure_id is not found or empty, uses this prompt.
        model_choice: 'gemini-3.1-flash-lite-image' (fast preview) or 'gemini-3-pro-image' (publication quality).

    Returns:
        A dictionary with figure_id, image_url, model_used, and generation status.
    """
    final_prompt = prompt.strip()
    figure_data: dict[str, Any] = {}

    if figure_id.strip():
        figure_data = get_figure(figure_id.strip())
        if "error" not in figure_data:
            final_prompt = figure_data.get("recommended_prompt") or final_prompt

    if not final_prompt:
        return {"error": "No valid prompt found or provided for image generation."}

    # Normalize model choice
    model = (
        "gemini-3-pro-image"
        if "pro" in model_choice.lower()
        else "gemini-3.1-flash-lite-image"
    )

    client = get_genai_client()
    response = client.models.generate_content(
        model=model,
        contents=final_prompt,
    )

    # Extract image bytes from response parts
    image_bytes = None
    mime_type = "image/jpeg"
    ext = "jpg"

    if response.candidates and response.candidates[0].content:
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                image_bytes = part.inline_data.data
                mime_type = part.inline_data.mime_type or "image/jpeg"
                if "png" in mime_type:
                    ext = "png"
                break

    if not image_bytes:
        return {"error": "Model response did not contain image data."}

    # 1. Save artifact with tool_context so it appears in Playground's Artifacts panel
    artifact_filename = f"{figure_id or 'figure'}_{int(datetime.now(timezone.utc).timestamp())}.{ext}"
    if tool_context is not None:
        try:
            artifact_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            await tool_context.save_artifact(filename=artifact_filename, artifact=artifact_part)
        except Exception:
            # Gracefully continue if artifact service is not configured in current runner
            pass

    # 2. Upload to public Cloud Storage bucket
    filename = f"figures/{artifact_filename}"
    storage_client = get_storage_client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"


    # Update Firestore record if figure_id was given
    if figure_id.strip() and "error" not in figure_data:
        db = get_firestore_client()
        db.collection(COLLECTION_NAME).document(figure_id.strip()).set(
            {
                "image_url": public_url,
                "model_used": model,
                "status": "generated",
                "generated_at": datetime.now(timezone.utc).isoformat(),
            },
            merge=True,
        )

    return {
        "status": "success",
        "figure_id": figure_id or "adhoc_generation",
        "model_used": model,
        "image_url": public_url,
        "download_url": public_url,
        "message": f"Mechanism figure successfully generated using {model} and stored in Cloud Storage.",
    }
