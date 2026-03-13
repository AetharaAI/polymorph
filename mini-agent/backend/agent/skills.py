from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "using",
    "when",
    "with",
    "where",
}

PROJECT_ACTION_TOKENS = {
    "build",
    "create",
    "debug",
    "fix",
    "generate",
    "implement",
    "patch",
    "refactor",
    "scaffold",
    "test",
}

PROJECT_OBJECT_TOKENS = {
    "api",
    "app",
    "backend",
    "codebase",
    "docker",
    "frontend",
    "module",
    "playwright",
    "project",
    "repo",
    "service",
    "workspace",
}

PROJECT_SKILLS = {"project-build-governance", "project-execution-loop"}

RESEARCH_INTENT_TOKENS = {
    "citation",
    "citations",
    "evidence",
    "fact",
    "facts",
    "latest",
    "news",
    "research",
    "search",
    "source",
    "sources",
    "verify",
    "web",
}


@dataclass(slots=True)
class SkillEntry:
    name: str
    description: str
    file_path: Path
    tags: tuple[str, ...]
    metadata: dict[str, Any]


@dataclass(slots=True)
class SkillSelection:
    name: str
    file_path: Path
    score: float
    reason: str
    metadata: dict[str, Any]


def _tokenize(value: str) -> set[str]:
    return {
        t
        for t in re.findall(r"[a-z0-9_+.-]+", value.lower())
        if len(t) > 1 and t not in STOPWORDS
    }


def _looks_like_project_request(message_tokens: set[str], raw_message: str) -> bool:
    if message_tokens & PROJECT_ACTION_TOKENS and message_tokens & PROJECT_OBJECT_TOKENS:
        return True

    # Accept direct imperative patterns like "build this API" or "implement this service".
    if re.search(r"\b(build|create|implement|scaffold|debug|fix|patch|generate)\b", raw_message):
        return True

    # Code-ish requests typically include paths/extensions.
    if re.search(r"\b[a-z0-9_./-]+\.(py|ts|tsx|js|jsx|json|yml|yaml|md)\b", raw_message):
        return True

    return False


def _registry_path() -> Path:
    default = Path(__file__).resolve().parents[1] / "SKILLS.md"
    raw = os.getenv("SKILLS_REGISTRY_PATH")
    if not raw:
        return default
    return Path(raw).expanduser()


def _skills_dir_candidates() -> list[Path]:
    env_dirs = os.getenv("SKILLS_DIRS", "").strip()
    if env_dirs:
        return [Path(d).expanduser() for d in env_dirs.split(",") if d.strip()]

    backend_dir = Path(__file__).resolve().parents[1]
    return [backend_dir / "skills", backend_dir / ".skills"]


def _parse_front_matter(raw_text: str) -> tuple[dict[str, Any], str]:
    text = raw_text.lstrip()
    if not text.startswith("---\n"):
        return {}, raw_text

    end_idx = text.find("\n---", 4)
    if end_idx == -1:
        return {}, raw_text

    header = text[4:end_idx].strip()
    body = text[end_idx + 4 :].lstrip("\n")
    metadata: dict[str, Any] = {}
    current_key: str | None = None
    current_items: list[str] = []

    for raw_line in header.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_key:
            current_items.append(stripped[2:].strip())
            metadata[current_key] = current_items[:]
            continue
        if ":" not in line:
            current_key = None
            current_items = []
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            metadata[key] = value.strip("\"'")
            current_key = None
            current_items = []
        else:
            metadata[key] = []
            current_key = key
            current_items = []

    return metadata, body


def _parse_registry_line(line: str, registry_dir: Path) -> SkillEntry | None:
    # Supported examples:
    # - web-research: Verify external claims. (file: skills/research/SKILL.md)
    # - web-research - Verify external claims. (file: skills/research/SKILL.md)
    m = re.search(r"\(file:\s*([^)]+)\)", line, flags=re.IGNORECASE)
    if not m:
        return None

    file_ref = m.group(1).strip()
    left = line[: m.start()].strip().lstrip("-").strip()
    if not left:
        return None

    if ":" in left:
        name, desc = left.split(":", 1)
    elif " - " in left:
        name, desc = left.split(" - ", 1)
    else:
        name, desc = left, ""

    name = name.strip()
    desc = desc.strip()
    if not name:
        return None

    file_path = Path(file_ref).expanduser()
    if not file_path.is_absolute():
        file_path = (registry_dir / file_ref).resolve()

    tags: tuple[str, ...] = tuple(sorted(_tokenize(f"{name} {desc}")))
    return SkillEntry(name=name, description=desc, file_path=file_path, tags=tags, metadata={})


def _scan_registry(registry_path: Path) -> list[SkillEntry]:
    if not registry_path.exists():
        return []

    entries: list[SkillEntry] = []
    registry_dir = registry_path.parent.resolve()
    for raw_line in registry_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or not line.startswith("-"):
            continue
        parsed = _parse_registry_line(line, registry_dir)
        if parsed:
            entries.append(parsed)
    return entries


def _scan_skill_dirs() -> list[SkillEntry]:
    entries: list[SkillEntry] = []
    for directory in _skills_dir_candidates():
        if not directory.exists():
            continue
        for path in sorted(directory.rglob("*")):
            if not path.is_file():
                continue
            if path.name not in {"SKILL.md", "SKILLS.md"} and path.suffix.lower() != ".md":
                continue

            stem = path.parent.name if path.name in {"SKILL.md", "SKILLS.md"} else path.stem
            name = stem.replace("_", "-").strip() or path.stem
            try:
                raw_text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            metadata, body = _parse_front_matter(raw_text)
            head = body[:800]
            desc = str(metadata.get("description") or "").strip()
            if not desc:
                desc_line = next((ln.strip("# ").strip() for ln in head.splitlines() if ln.strip()), "")
                desc = desc_line[:180]
            entry_name = str(metadata.get("name") or name).strip() or name
            tag_items = metadata.get("tags") if isinstance(metadata.get("tags"), list) else []
            tags: tuple[str, ...] = tuple(sorted(_tokenize(f"{entry_name} {desc} {' '.join(tag_items)}")))
            entries.append(
                SkillEntry(
                    name=entry_name,
                    description=desc,
                    file_path=path.resolve(),
                    tags=tags,
                    metadata=metadata,
                )
            )
    return entries


def _load_entries() -> list[SkillEntry]:
    registry_entries = _scan_registry(_registry_path())
    if registry_entries:
        return registry_entries
    return _scan_skill_dirs()


def _score_skill(entry: SkillEntry, message_tokens: set[str], raw_message: str) -> tuple[float, str]:
    score = 0.0
    reason_parts: list[str] = []

    name_lower = entry.name.lower()
    explicit_name_match = False
    if name_lower and name_lower in raw_message:
        explicit_name_match = True
        score += 5.0
        reason_parts.append("name match")

    # Prevent build/governance skills from hijacking non-project prompts.
    if entry.name.lower() in PROJECT_SKILLS and not explicit_name_match:
        if not _looks_like_project_request(message_tokens, raw_message):
            return 0.0, ""

    if entry.name.lower() == "verification-and-sourcing":
        if message_tokens & RESEARCH_INTENT_TOKENS:
            score += 1.0
            reason_parts.append("research intent")

    desc_tokens = _tokenize(entry.description)
    overlap = len((desc_tokens | set(entry.tags)) & message_tokens)
    if overlap:
        score += float(overlap)
        reason_parts.append(f"{overlap} keyword overlap")

    if score <= 0:
        return 0.0, ""

    return score, ", ".join(reason_parts)


def select_relevant_skills(user_message: str) -> list[SkillSelection]:
    if os.getenv("SKILLS_ENABLED", "true").strip().lower() not in {"1", "true", "yes", "on"}:
        return []

    entries = _load_entries()
    if not entries:
        return []

    message_lower = user_message.lower()
    message_tokens = _tokenize(message_lower)
    min_score = float(os.getenv("SKILLS_MIN_SCORE", "1"))
    max_skills = max(1, int(os.getenv("SKILLS_MAX_ACTIVE", "3")))

    scored: list[SkillSelection] = []
    for entry in entries:
        score, reason = _score_skill(entry, message_tokens, message_lower)
        if score < min_score:
            continue
        scored.append(
            SkillSelection(
                name=entry.name,
                file_path=entry.file_path,
                score=score,
                reason=reason or "heuristic match",
                metadata=entry.metadata,
            )
        )

    scored.sort(key=lambda s: s.score, reverse=True)
    return scored[:max_skills]


def build_skills_prompt(user_message: str) -> tuple[str, list[SkillSelection]]:
    selected = select_relevant_skills(user_message)
    if not selected:
        return "", []

    max_total_chars = max(800, int(os.getenv("SKILLS_MAX_TOTAL_CHARS", "4000")))

    blocks: list[str] = [
        "## Relevant Skill Metadata",
        "Treat this as authoritative skill front matter. Use it to decide whether a skill applies. Do not infer missing rules from model memory.",
    ]

    total_chars = sum(len(b) for b in blocks)
    included: list[SkillSelection] = []
    for sel in selected:
        if not sel.file_path.exists():
            continue
        metadata = dict(sel.metadata or {})
        if not metadata:
            try:
                metadata, _ = _parse_front_matter(sel.file_path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                metadata = {}
        description = str(metadata.get("description") or sel.reason or "n/a").strip()
        trigger = str(metadata.get("trigger") or metadata.get("intent") or metadata.get("when") or "n/a").strip()
        tags = metadata.get("tags") if isinstance(metadata.get("tags"), list) else []
        tools = metadata.get("tools") if isinstance(metadata.get("tools"), list) else []
        section = (
            f"### Skill: {sel.name}\n"
            f"File: {sel.file_path}\n"
            f"Why selected: {sel.reason}\n\n"
            f"- description: {description}\n"
            f"- trigger: {trigger}\n"
            f"- tags: {', '.join(str(item) for item in tags) if tags else 'n/a'}\n"
            f"- tools: {', '.join(str(item) for item in tools) if tools else 'n/a'}"
        )
        projected = total_chars + len(section)
        if projected > max_total_chars and included:
            break
        blocks.append(section)
        total_chars = projected
        included.append(sel)

    if not included:
        return "", []

    return "\n\n".join(blocks), included
