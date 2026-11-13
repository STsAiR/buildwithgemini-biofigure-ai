"""Seed script for BioFigure AI mechanism figures Firestore collection.

Hardcodes PROJECT_ID as a string to ensure compatibility with both local
runs and Agent Platform deployments.
"""

from datetime import datetime, timezone
from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-e67897557cd7"
COLLECTION_NAME = "mechanism_figures"

SEED_DATA = [
    {
        "id": "fig_macrophage_hypoxia",
        "title": "Tumor-Associated Macrophage Polarization in Hypoxia",
        "topic": "Hypoxic Tumor Microenvironment & Immunosuppression",
        "biological_system": "Immuno-Oncology",
        "figure_type": "mechanism",
        "compartments": ["Normoxic Capillary", "Hypoxic Tumor Core", "Extracellular Matrix"],
        "actors": ["Hypoxia", "HIF-1alpha", "CCL2", "Monocyte", "M2 TAM", "CD8+ T cell", "anti-PD-1"],
        "mechanism_flow": "Hypoxia stabilizes HIF-1alpha in tumor cells -> tumor cells secrete CCL2/CSF1 -> circulating monocytes extravasate into tumor parenchyma -> monocytes polarize into pro-tumoral M2 TAMs -> M2 TAMs express PD-L1 and arginase-1 to exhaust CD8+ T cells -> anti-PD-1 antibody reverses T cell suppression",
        "target_audience": "Review Article in Nature Immunology",
        "recommended_model": "gemini-3-pro-image",
        "recommended_prompt": (
            "Create a publication-ready biomedical schematic, BioRender-inspired but original.\n"
            "Topic: Tumor-associated macrophage polarization in hypoxic tumor microenvironment.\n"
            "Audience: Review Article.\n"
            "Canvas: landscape 16:9, clean white background.\n"
            "Compartments: Normoxic Capillary, Hypoxic Tumor Core, Extracellular Matrix.\n"
            "Main visual elements: Tumor cells, Hypoxia gradient, HIF-1alpha, CCL2 gradient, Monocyte, M2 Macrophage, CD8+ T cell, anti-PD-1 antibody.\n"
            "Mechanism flow: Hypoxia stabilizes HIF-1alpha -> CCL2/CSF1 secretion -> monocyte extravasation -> M2 polarization -> T cell exhaustion -> anti-PD-1 therapeutic restoration.\n"
            "Labels to include exactly: Hypoxia, HIF-1alpha, CCL2, M2 TAM, CD8+ T Cell, anti-PD-1.\n"
            "Style: ultra-high-resolution, print-ready, crisp vector-like shapes, soft scientific color palette, consistent line weight, clear directional arrows, generous whitespace, large readable labels.\n"
            "Avoid: photorealistic rendering, 3D glossy plastic, brand logos, copied BioRender icons, fake tiny labels, dark backgrounds."
        ),
        "status": "ready_for_generation",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "id": "fig_car_t_exhaustion",
        "title": "CAR-T Cell Exhaustion and Reversal via Immune Checkpoint Blockade",
        "topic": "Adoptive Cell Therapy & Checkpoint Inhibition",
        "biological_system": "Cellular Immunology",
        "figure_type": "review",
        "compartments": ["Tumor Stroma", "T Cell Membrane", "T Cell Nucleus"],
        "actors": ["CAR-T Cell", "Tumor Antigen (CD19)", "PD-1", "PD-L1", "TOX", "anti-PD-1", "Granzyme B"],
        "mechanism_flow": "Continuous CAR activation by CD19 induces chronic signaling -> upregulation of transcription factor TOX -> surface expression of exhaustion markers PD-1 and TIM-3 -> PD-L1 engagement inhibits cytotoxicity and cytokine release -> anti-PD-1 checkpoint inhibitor blocks inhibitory axis restoring Granzyme B secretion",
        "target_audience": "Grant Proposal & Cancer Cell Review",
        "recommended_model": "gemini-3-pro-image",
        "recommended_prompt": (
            "Create a publication-ready biomedical schematic, BioRender-inspired but original.\n"
            "Topic: CAR-T cell exhaustion and checkpoint reversal.\n"
            "Audience: Cancer Cell Review.\n"
            "Canvas: landscape 16:9, clean white background.\n"
            "Compartments: Tumor Stroma, T Cell Membrane, T Cell Nucleus.\n"
            "Main visual elements: CAR-T cell, CD19 expressing lymphoma cell, TOX transcription factor, PD-1/PD-L1 complex, anti-PD-1 mAb, Granzyme B vesicles.\n"
            "Mechanism flow: Chronic CD19 ligation -> nuclear TOX induction -> PD-1 upregulation -> functional exhaustion -> anti-PD-1 rescue.\n"
            "Labels to include exactly: CAR Receptor, CD19, TOX, PD-1, PD-L1, Granzyme B.\n"
            "Style: ultra-high-resolution, print-ready, crisp vector-like shapes, soft scientific color palette, consistent line weight, clear directional arrows, generous whitespace, large readable labels.\n"
            "Avoid: photorealistic rendering, 3D glossy plastic, brand logos, copied BioRender icons, fake tiny labels, dark backgrounds."
        ),
        "status": "ready_for_generation",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "id": "fig_synaptic_plasticity",
        "title": "NMDA Receptor-Dependent Long-Term Potentiation (LTP)",
        "topic": "Synaptic Plasticity & Memory Encoding",
        "biological_system": "Molecular Neuroscience",
        "figure_type": "pathway",
        "compartments": ["Presynaptic Bouton", "Synaptic Cleft", "Postsynaptic Dendritic Spine"],
        "actors": ["Glutamate", "AMPA Receptor", "NMDA Receptor", "Mg2+ Block", "Ca2+ Influx", "CaMKII", "AMPA Exocytosis"],
        "mechanism_flow": "Presynaptic action potential triggers glutamate release -> initial AMPA receptor activation depolarizes postsynaptic membrane -> depolarization expels Mg2+ block from NMDA receptor pore -> Ca2+ enters dendritic spine via NMDA receptor -> Ca2+ binds calmodulin to activate CaMKII -> phosphorylation drives exocytosis of additional AMPA receptors into postsynaptic density enhancing synaptic strength",
        "target_audience": "Neuroscience Textbook & Journal Article",
        "recommended_model": "gemini-3.1-flash-lite-image",
        "recommended_prompt": (
            "Create a publication-ready biomedical schematic, BioRender-inspired but original.\n"
            "Topic: NMDA receptor-dependent Long-Term Potentiation (LTP) at the CA3-CA1 hippocampal synapse.\n"
            "Audience: Journal Article.\n"
            "Canvas: landscape 16:9, clean white background.\n"
            "Compartments: Presynaptic Bouton, Synaptic Cleft, Postsynaptic Dendritic Spine.\n"
            "Main visual elements: Synaptic vesicles, Glutamate neurotransmitter, AMPA receptor, NMDA receptor with Mg2+ ion, Calcium influx, CaMKII kinase, Postsynaptic density.\n"
            "Mechanism flow: Glutamate release -> AMPA depolarization -> Mg2+ unblocking -> Ca2+ entry -> CaMKII activation -> AMPA insertion.\n"
            "Labels to include exactly: Glutamate, AMPAR, NMDAR, Mg2+, Ca2+, CaMKII.\n"
            "Style: ultra-high-resolution, print-ready, crisp vector-like shapes, soft scientific color palette, consistent line weight, clear directional arrows, generous whitespace, large readable labels.\n"
            "Avoid: photorealistic rendering, 3D glossy plastic, brand logos, copied BioRender icons, fake tiny labels, dark backgrounds."
        ),
        "status": "ready_for_generation",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
]


def seed_database() -> None:
    """Connect to Firestore and insert seed mechanism figures."""
    print(f"Connecting to Firestore for project: '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    for item in SEED_DATA:
        doc_id = item["id"]
        data = {k: v for k, v in item.items() if k != "id"}
        collection_ref.document(doc_id).set(data)
        print(f"✓ Seeded figure: '{doc_id}' - {item['title']}")

    print(f"\nSuccessfully seeded {len(SEED_DATA)} figures into collection '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    seed_database()
