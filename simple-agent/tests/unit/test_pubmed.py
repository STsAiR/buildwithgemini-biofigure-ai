"""Unit test for NCBI PubMed search service."""

from app.pubmed_service import search_pubmed_papers


def test_search_pubmed_papers() -> None:
    results = search_pubmed_papers("HIF1A macrophage", max_results=2)
    assert isinstance(results, list)
    assert len(results) > 0
    first = results[0]
    assert "pmid" in first
    assert "title" in first
    assert "url" in first
    assert "https://pubmed.ncbi.nlm.nih.gov/" in first["url"]
