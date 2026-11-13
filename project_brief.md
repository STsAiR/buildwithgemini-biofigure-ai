# My agent: BioFigure AI (Biomedical Mechanism Figure & Abstract Agent)

One-liner: A conversational and multimodal scientific figure agent that helps biomedical researchers turn research papers (PDF), hypotheses (text), and hand-drawn drafts (images) into publication-ready scientific mechanism figures and graphical abstracts with a catalog of generated figures.

Tool coverage:
- Memory: Remembers research domain, target journal style preferences (e.g., Nature/Cell color palettes, vector vs raster), recurring molecular actors/pathways, and past figure iterations across sessions.
- Tools: Multimodal mechanism extraction (parsing text, PDF papers, and draft images), BioRender-style prompt synthesis (structured biological layout, actors, compartments, and causal flow based on biorender-mechanism-figures-skill), and Gemini image generation tool.
- Catalog/UI: Catalog of generated figures rendered as interactive A2UI cards displaying image previews, figure legends, metadata, and direct download links.
- Image gen: Generates publication-quality biomedical mechanism diagrams, pathway schematics, and graphical abstracts using user-selectable Gemini image generation models: Nano Banana 2 Lite (gemini-3.1-flash-lite-image) for fast preview or Gemini 3 Pro (gemini-3-pro-image) for high-resolution publication output.
- Sandbox: Optional code sandbox execution for diagram layout calculations or SVG/Mermaid flow graph generation.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch (pick what fits): Multimodal PDF/image parsing tool, Cloud Storage bucket for asset storage and download links, code sandbox for pathway node plotting.
