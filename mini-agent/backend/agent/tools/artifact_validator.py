from __future__ import annotations

import ast
import csv
import io
import json
from pathlib import Path
from typing import Any


def _validate_csv(content: str) -> dict[str, Any]:
    reader = csv.reader(io.StringIO(content))
    row_lengths: list[int] = []
    for idx, row in enumerate(reader, start=1):
        row_lengths.append(len(row))
        if idx > 5000:
            break

    if not row_lengths:
        return {"valid": False, "warnings": ["CSV appears empty"]}

    expected = row_lengths[0]
    mismatched = [i + 1 for i, width in enumerate(row_lengths) if width != expected]
    if mismatched:
        return {
            "valid": False,
            "warnings": [
                f"CSV row width mismatch. Expected {expected} columns; mismatched rows include: {mismatched[:8]}"
            ],
        }

    return {"valid": True, "warnings": []}


def _validate_json(content: str) -> dict[str, Any]:
    try:
        json.loads(content)
        return {"valid": True, "warnings": []}
    except Exception as exc:
        return {"valid": False, "warnings": [f"Invalid JSON: {exc}"]}


def _validate_python(content: str) -> dict[str, Any]:
    try:
        ast.parse(content)
        return {"valid": True, "warnings": []}
    except Exception as exc:
        return {"valid": False, "warnings": [f"Invalid Python syntax: {exc}"]}


def _validate_markdown(content: str) -> dict[str, Any]:
    if not content.strip():
        return {"valid": False, "warnings": ["Markdown file is empty"]}

    heading_count = sum(1 for line in content.splitlines() if line.strip().startswith("#"))
    warnings: list[str] = []
    if heading_count == 0 and len(content) > 500:
        warnings.append("Long markdown has no headings; readability may be poor")

    return {"valid": True, "warnings": warnings}


def validate_artifact(filename: str, content: str) -> dict[str, Any]:
    ext = Path(filename).suffix.lower()

    if ext == ".csv":
        result = _validate_csv(content)
        kind = "csv"
    elif ext == ".json":
        result = _validate_json(content)
        kind = "json"
    elif ext == ".py":
        result = _validate_python(content)
        kind = "python"
    elif ext in {".md", ".txt"}:
        result = _validate_markdown(content)
        kind = "markdown"
    else:
        result = {"valid": True, "warnings": ["No validator for this extension; stored as text"]}
        kind = "generic"

    warnings = result.get("warnings") or []
    status = "valid" if result.get("valid") and not warnings else ("warn" if result.get("valid") else "invalid")

    return {
        "status": status,
        "kind": kind,
        "valid": bool(result.get("valid", False)),
        "warnings": warnings,
    }
