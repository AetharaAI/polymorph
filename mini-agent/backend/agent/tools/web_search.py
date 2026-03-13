import asyncio
import os
from urllib.parse import urlparse
import httpx
try:
    from ddgs import DDGS
except ImportError:
    from duckduckgo_search import DDGS


HIGH_TRUST_DOMAINS = {
    "openai.com",
    "platform.openai.com",
    "anthropic.com",
    "docs.anthropic.com",
    "ai.google.dev",
    "cloud.google.com",
    "blog.google",
    "ai.meta.com",
    "llama.com",
    "mistral.ai",
    "docs.mistral.ai",
    "cohere.com",
    "docs.cohere.com",
    "x.ai",
    "huggingface.co",
    "arxiv.org",
    "nature.com",
    "science.org",
    "reuters.com",
    "apnews.com",
    "bbc.com",
    "nytimes.com",
    "ft.com",
    "wsj.com",
    "bloomberg.com",
    "theverge.com",
    "techcrunch.com",
    "docs.anthropic.com",
    "github.com",
}

MEDIUM_TRUST_DOMAINS = {
    "wikipedia.org",
    "en.wikipedia.org",
    "investor.nvidia.com",
    "nvidia.com",
    "developer.nvidia.com",
    "docs.python.org",
    "axios.com",
    "theinformation.com",
    "aljazeera.com",
    "cnbc.com",
    "engadget.com",
    "cnet.com",
    "mit.edu",
    "technologyreview.com",
}

MODEL_RELEASE_TERMS = {
    "model",
    "models",
    "drop",
    "drops",
    "launch",
    "launched",
    "release",
    "released",
    "latest",
    "new",
}

OFFICIAL_MODEL_RELEASE_DOMAINS = [
    "openai.com",
    "anthropic.com",
    "blog.google",
    "cloud.google.com",
    "ai.google.dev",
    "ai.meta.com",
    "llama.com",
    "mistral.ai",
    "cohere.com",
    "x.ai",
    "huggingface.co",
    "developer.nvidia.com",
]


def _host(url: str) -> str:
    host = urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def _source_quality(url: str) -> str:
    host = _host(url)
    if host in HIGH_TRUST_DOMAINS:
        return "HIGH"
    if host in MEDIUM_TRUST_DOMAINS:
        return "MEDIUM"
    return "LOW"


def _is_model_release_query(query: str) -> bool:
    tokens = {t.strip(".,!?").lower() for t in query.split()}
    return len(tokens & MODEL_RELEASE_TERMS) >= 2


def _dedupe_results(items: list[dict]) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for item in items:
        url = item.get("href") or item.get("url") or ""
        if not url:
            continue
        key = url.split("#", 1)[0]
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _quality_rank(url: str) -> int:
    quality = _source_quality(url)
    if quality == "HIGH":
        return 0
    if quality == "MEDIUM":
        return 1
    return 2


async def _ddgs_search(query: str, max_results: int = 5) -> list[dict]:
    def search() -> list[dict]:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=max_results))

    return await asyncio.to_thread(search)


async def web_search(query: str, max_results: int = 5) -> str:
    """Search the web for current information."""
    max_results = max(1, min(int(max_results), 10))
    query = (query or "").strip()
    if not query:
        return "Error: web_search requires a non-empty query."

    results = await _ddgs_search(query, max_results=max_results)

    # For "latest model drops" style requests, run an official-sources-biased pass.
    if _is_model_release_query(query):
        official_query = (
            f"{query} "
            "(site:openai.com OR site:anthropic.com OR site:blog.google OR site:cloud.google.com "
            "OR site:ai.meta.com OR site:llama.com OR site:mistral.ai)"
        )
        official_results = await _ddgs_search(official_query, max_results=max_results)
        results = _dedupe_results(official_results + results)

    # Prefer higher-trust sources first.
    results = sorted(
        _dedupe_results(results),
        key=lambda r: (
            _quality_rank(r.get("href", r.get("url", ""))),
            r.get("title", ""),
        ),
    )[:max_results]

    if not results:
        return "No search results found."

    formatted = []
    low_quality_count = 0
    for i, result in enumerate(results, 1):
        title = result.get("title", "Untitled")
        url = result.get("href", result.get("url", ""))
        snippet = result.get("body", "")
        quality = _source_quality(url)
        if quality == "LOW":
            low_quality_count += 1
        formatted.append(f"{i}. **{title}** [source_quality={quality}]\n   {snippet}\n   {url}")

    if low_quality_count == len(results):
        formatted.append(
            "\nWarning: all returned sources are LOW trust for this query. "
            "Cross-check with official provider announcements."
        )

    return "\n\n".join(formatted)


async def tavily_search(query: str, max_results: int = 5) -> str:
    """Search the web via Tavily for higher-recall research cross-checking."""
    api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not api_key:
        return "Error: TAVILY_API_KEY is not configured."

    max_results = max(1, min(int(max_results), 10))
    query = (query or "").strip()
    if not query:
        return "Error: tavily_search requires a non-empty query."
    payload = {
        "api_key": api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": "advanced",
        "include_answer": False,
        "include_raw_content": False,
    }
    if _is_model_release_query(query):
        payload["include_domains"] = OFFICIAL_MODEL_RELEASE_DOMAINS

    timeout = httpx.Timeout(
        timeout=float(os.getenv("TAVILY_TIMEOUT_SECONDS", "45")),
        connect=10.0,
        read=45.0,
    )
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.post("https://api.tavily.com/search", json=payload)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        return f"Error: Tavily search failed: {exc}"

    results = data.get("results") if isinstance(data, dict) else None
    if not isinstance(results, list) or not results:
        return "No search results found."

    filtered: list[dict] = [r for r in results if isinstance(r, dict)]
    filtered.sort(
        key=lambda r: (
            _quality_rank(r.get("url", "")),
            r.get("title", ""),
        )
    )

    formatted = []
    for i, item in enumerate(filtered[:max_results], 1):
        if not isinstance(item, dict):
            continue
        title = item.get("title") or "Untitled"
        url = item.get("url") or ""
        snippet = item.get("content") or item.get("snippet") or ""
        quality = _source_quality(url)
        formatted.append(f"{i}. **{title}** [source_quality={quality}]\n   {snippet}\n   {url}")

    if not formatted:
        return "No search results found."
    return "\n\n".join(formatted)


async def brave_search(query: str, max_results: int = 5) -> str:
    """Search the web via Brave Search API."""
    api_key = (
        os.getenv("BRAVE_API_KEY", "").strip()
        or os.getenv("BRAVE_SEARCH_API_KEY", "").strip()
    )
    if not api_key:
        return "Error: BRAVE API key is not configured."

    max_results = max(1, min(int(max_results), 10))
    query = (query or "").strip()
    if not query:
        return "Error: brave_search requires a non-empty query."

    params = {"q": query, "count": max_results}
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }
    timeout = httpx.Timeout(timeout=30.0, connect=10.0, read=25.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            resp = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                params=params,
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        return f"Error: Brave search failed: {exc}"

    web = data.get("web") if isinstance(data, dict) else None
    results = web.get("results") if isinstance(web, dict) else None
    if not isinstance(results, list) or not results:
        return "No search results found."

    results = sorted(
        [r for r in results if isinstance(r, dict)],
        key=lambda r: (
            _quality_rank(r.get("url", "")),
            r.get("title", ""),
        ),
    )[:max_results]

    formatted = []
    for i, item in enumerate(results, 1):
        title = item.get("title") or "Untitled"
        url = item.get("url") or ""
        snippet = item.get("description") or item.get("snippet") or ""
        quality = _source_quality(url)
        formatted.append(f"{i}. **{title}** [source_quality={quality}]\n   {snippet}\n   {url}")

    if not formatted:
        return "No search results found."
    return "\n\n".join(formatted)
