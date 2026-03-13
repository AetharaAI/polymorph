from __future__ import annotations

from backend.agent.providers import get_provider


def _extract_text_from_response(content_blocks: list) -> str:
    parts: list[str] = []
    for block in content_blocks:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    return "\n".join(part for part in parts if part).strip()


async def summarize_document(text: str, focus: str | None = None) -> str:
    """Summarize a long document using the configured LLM provider."""
    provider = get_provider()

    if len(text) < 1000:
        return text

    max_chunk_size = 40000
    chunks: list[str] = []

    if len(text) > max_chunk_size:
        paragraphs = text.split("\n\n")
        current_chunk = ""
        for para in paragraphs:
            if len(current_chunk) + len(para) > max_chunk_size:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
            else:
                current_chunk += "\n\n" + para if current_chunk else para
        if current_chunk:
            chunks.append(current_chunk)
    else:
        chunks = [text]

    summaries: list[str] = []
    focus_instruction = f"\n\nFocus on: {focus}" if focus else ""

    for i, chunk in enumerate(chunks):
        prompt = f"""Summarize the following text concisely, capturing the key points:{focus_instruction}

{chunk}

Summary:"""

        try:
            response = await provider.generate(
                system="You are a precise technical summarizer.",
                tools=[],
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                max_tokens=1024,
                temperature=0.3,
            )
            summary = _extract_text_from_response(response.content)
            summaries.append(summary or "[No summary text returned]")
        except Exception as exc:
            summaries.append(f"[Error summarizing chunk {i + 1}: {exc}]")

    if len(summaries) > 1:
        final_prompt = f"""Combine these summaries into a single coherent summary:{focus_instruction}

{' '.join(summaries)}

Final Summary:"""

        try:
            response = await provider.generate(
                system="You are a precise technical summarizer.",
                tools=[],
                messages=[{"role": "user", "content": [{"type": "text", "text": final_prompt}]}],
                max_tokens=1024,
                temperature=0.3,
            )
            final_summary = _extract_text_from_response(response.content)
            return final_summary or "\n\n".join(summaries)
        except Exception:
            return "\n\n".join(summaries)

    return summaries[0] if summaries else "Could not generate summary."
