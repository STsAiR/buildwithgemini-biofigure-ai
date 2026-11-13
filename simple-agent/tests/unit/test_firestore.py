"""Unit tests for Firestore mechanism figure service."""

from app.firestore_service import list_figures, get_figure, search_figures_by_actor


def test_list_figures_seeded() -> None:
    figures = list_figures()
    assert len(figures) >= 3
    ids = [f["id"] for f in figures]
    assert "fig_macrophage_hypoxia" in ids
    assert "fig_car_t_exhaustion" in ids
    assert "fig_synaptic_plasticity" in ids


def test_get_figure() -> None:
    fig = get_figure("fig_macrophage_hypoxia")
    assert fig is not None
    assert fig.get("title") == "Tumor-Associated Macrophage Polarization in Hypoxia"
    assert "Hypoxia" in fig.get("actors", [])


def test_search_figures_by_actor() -> None:
    results = search_figures_by_actor("HIF-1alpha")
    assert len(results) >= 1
    assert any(r["id"] == "fig_macrophage_hypoxia" for r in results)
