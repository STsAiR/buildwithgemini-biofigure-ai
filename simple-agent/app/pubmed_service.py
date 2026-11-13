"""NCBI PubMed E-Utilities service for searching biomedical literature.

Uses the free public NCBI Entrez E-Utilities API.
Supports optional NCBI_API_KEY from the environment for higher rate limits.
"""

import json
import os
from typing import Any
import urllib.parse
import urllib.request

NCBI_BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed_papers(query: str, max_results: int = 3) -> list[dict[str, Any]]:
    """Search PubMed for biomedical papers and return titles, PMIDs, journal, and publication dates."""
    clean_query = query.strip()
    if not clean_query:
        return []

    api_key = os.getenv("NCBI_API_KEY", "").strip()
    key_param = f"&api_key={api_key}" if api_key else ""

    # 1. Search for matching PMIDs
    term = urllib.parse.quote_plus(clean_query)
    search_url = (
        f"{NCBI_BASE_URL}/esearch.fcgi?db=pubmed&term={term}&retmax={max_results}&retmode=json{key_param}"
    )

    req = urllib.request.Request(search_url, headers={"User-Agent": "BioFigureAI/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            search_data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return [{"error": f"Failed to search PubMed: {str(e)}"}]

    id_list = search_data.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        return []

    # 2. Fetch paper summaries for the PMIDs
    ids_str = ",".join(id_list)
    summary_url = (
        f"{NCBI_BASE_URL}/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json{key_param}"
    )

    req = urllib.request.Request(summary_url, headers={"User-Agent": "BioFigureAI/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            summary_data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return [{"error": f"Failed to fetch PubMed summaries: {str(e)}"}]

    result = summary_data.get("result", {})
    papers = []
    for uid in id_list:
        doc = result.get(uid, {})
        if not doc:
            continue
        authors = [a.get("name") for a in doc.get("authors", []) if a.get("name")]
        papers.append({
            "pmid": uid,
            "title": doc.get("title", ""),
            "journal": doc.get("source", ""),
            "pubdate": doc.get("pubdate", ""),
            "authors": authors[:3],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
        })

    return papers
