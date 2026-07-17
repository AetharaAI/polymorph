from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from backend.agent.providers.factory import get_vision_provider, get_vision_verifier_provider, vision_routing_metadata
from backend.agent.tools import file_ops

DEFAULT_PADDLE_DOC_ORI_DIR = "/home/cory/.paddlex/official_models/PP-LCNet_x1_0_doc_ori"
DEFAULT_PADDLE_TEXTLINE_ORI_DIR = "/home/cory/.paddlex/official_models/PP-LCNet_x1_0_textline_ori"
DEFAULT_PADDLE_UVDOC_DIR = "/home/cory/.paddlex/official_models/UVDoc"
DEFAULT_PADDLE_DET_DIR = "/home/cory/.paddlex/official_models/PP-OCRv5_server_det"
DEFAULT_PADDLE_REC_DIR = "/home/cory/.paddlex/official_models/en_PP-OCRv5_mobile_rec"
DEFAULT_GLM_OCR_DIR = "/home/cory/models/GLM-OCR"


def _strip_fences(text: str) -> str:
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    return cleaned.strip()


def _extract_file_id(raw_ref: str) -> str:
    value = (raw_ref or "").strip()
    if value.startswith("attachment://"):
        return value[len("attachment://"):].strip()
    return value


def _file_label(file_path: Path) -> str:
    parts = file_path.name.split("_", 1)
    return parts[1] if len(parts) > 1 else file_path.name


def _base_question(question: str | None, original_name: str) -> str:
    prompt = (question or "").strip()
    if prompt:
        return prompt
    return (
        f"Inspect this image ({original_name}) and identify visible state, text, warnings, "
        "errors, controls, diagrams, and anything relevant to the user request."
    )


def _system_prompt(output_format: str) -> str:
    if output_format == "structured":
        return (
            "You are PolyMorph Perceptor, a visual inspection specialist. "
            "Analyze the provided image carefully and return JSON only. "
            "Use this exact shape: "
            '{"summary": string, "visible_text": string[], "ui_state": object, "uncertainties": string[]}. '
            "Be concise, factual, and avoid inventing unseen details."
        )
    return (
        "You are PolyMorph Perceptor, a visual inspection specialist. "
        "Analyze the provided image carefully and answer concisely with factual observations only."
    )


def _parse_structured_response(text: str) -> dict[str, Any]:
    cleaned = _strip_fences(text)
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return {
                "summary": str(parsed.get("summary") or ""),
                "visible_text": [str(item) for item in (parsed.get("visible_text") or []) if str(item or "").strip()],
                "ui_state": parsed.get("ui_state") if isinstance(parsed.get("ui_state"), dict) else {},
                "uncertainties": [str(item) for item in (parsed.get("uncertainties") or []) if str(item or "").strip()],
            }
    except Exception:
        pass

    return {
        "summary": cleaned,
        "visible_text": [],
        "ui_state": {},
        "uncertainties": ["Model returned non-JSON structured output; summary preserved as raw text."],
    }


def _extract_response_text(response: Any) -> dict[str, Any]:
    text_parts: list[str] = []
    fallback_parts: list[str] = []
    block_types: list[str] = []

    for block in getattr(response, "content", []) or []:
        block_type = str(getattr(block, "type", "") or "").strip() or "unknown"
        block_types.append(block_type)

        text_value = str(getattr(block, "text", "") or "").strip()
        thinking_value = str(getattr(block, "thinking", "") or "").strip()

        if text_value:
            text_parts.append(text_value)
        elif block_type == "thinking" and thinking_value:
            fallback_parts.append(thinking_value)
        elif thinking_value:
            fallback_parts.append(thinking_value)

    primary_text = "\n".join(part for part in text_parts if part).strip()
    fallback_text = "\n".join(part for part in fallback_parts if part).strip()
    effective_text = primary_text or fallback_text

    return {
        "text": effective_text,
        "used_fallback": not bool(primary_text) and bool(fallback_text),
        "block_types": block_types,
    }


def local_ocr_metadata() -> dict[str, Any]:
    enabled = str(os.getenv("VISION_LOCAL_OCR_ENABLED", "true")).strip().lower() in {"1", "true", "yes", "on"}
    engine = str(os.getenv("VISION_LOCAL_OCR_ENGINE", "paddleocr")).strip().lower() or "paddleocr"
    paddle_det_dir = str(os.getenv("VISION_PADDLE_DET_DIR", DEFAULT_PADDLE_DET_DIR)).strip()
    paddle_rec_dir = str(os.getenv("VISION_PADDLE_REC_DIR", DEFAULT_PADDLE_REC_DIR)).strip()
    doc_ori_dir = str(os.getenv("VISION_PADDLE_DOC_ORI_DIR", DEFAULT_PADDLE_DOC_ORI_DIR)).strip()
    textline_dir = str(os.getenv("VISION_PADDLE_TEXTLINE_ORI_DIR", DEFAULT_PADDLE_TEXTLINE_ORI_DIR)).strip()
    uvdoc_dir = str(os.getenv("VISION_PADDLE_UVDOC_DIR", DEFAULT_PADDLE_UVDOC_DIR)).strip()
    glm_dir = str(os.getenv("VISION_GLM_OCR_DIR", DEFAULT_GLM_OCR_DIR)).strip()

    paths = {
        "paddle_det_dir": paddle_det_dir,
        "paddle_rec_dir": paddle_rec_dir,
        "paddle_doc_ori_dir": doc_ori_dir,
        "paddle_textline_ori_dir": textline_dir,
        "paddle_uvdoc_dir": uvdoc_dir,
        "glm_ocr_dir": glm_dir,
    }
    path_exists = {key: Path(value).exists() for key, value in paths.items() if value}
    configured = enabled and path_exists.get("paddle_det_dir", False) and path_exists.get("paddle_rec_dir", False)
    return {
        "enabled": enabled,
        "configured": configured,
        "engine": engine,
        "paths": paths,
        "path_exists": path_exists,
        "timeout_seconds": max(1, int(os.getenv("VISION_LOCAL_OCR_TIMEOUT_SECONDS", "20"))),
    }


def _question_prefers_vlm(question: str | None) -> bool:
    prompt = str(question or "").lower()
    vlm_keywords = (
        "chart",
        "diagram",
        "graph",
        "photo",
        "scene",
        "layout",
        "spatial",
        "icon",
        "color",
        "what is happening",
        "what does this show",
        "ui state",
    )
    return any(keyword in prompt for keyword in vlm_keywords)


def _should_use_local_ocr_auto(question: str | None) -> bool:
    return not _question_prefers_vlm(question)


def _summarize_ocr_text(lines: list[str]) -> str:
    if not lines:
        return "Local OCR did not confidently extract visible text."
    sample = " | ".join(lines[:3])
    return f"Local OCR extracted {len(lines)} text lines. Sample: {sample}"


def _run_local_ocr_subprocess(image_path: Path) -> dict[str, Any]:
    meta = local_ocr_metadata()
    if not meta["configured"]:
        return {
            "ok": False,
            "engine": meta["engine"],
            "error": "Local OCR is not fully configured on this machine.",
        }

    script = f"""
import json
import os
from pathlib import Path

import paddle
cfg = paddle.base.libpaddle.AnalysisConfig
if not hasattr(cfg, "set_optimization_level"):
    def _noop(self, level):
        return None
    cfg.set_optimization_level = _noop

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    text_detection_model_dir={meta["paths"]["paddle_det_dir"]!r},
    text_recognition_model_dir={meta["paths"]["paddle_rec_dir"]!r},
    doc_orientation_classify_model_dir={meta["paths"]["paddle_doc_ori_dir"]!r},
    doc_unwarping_model_dir={meta["paths"]["paddle_uvdoc_dir"]!r},
    textline_orientation_model_dir={meta["paths"]["paddle_textline_ori_dir"]!r},
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)
results = ocr.predict({str(image_path)!r})
normalized = []
for item in results:
    payload = item if isinstance(item, dict) else getattr(item, "json", None)
    if callable(payload):
        payload = item.json
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {{"raw": payload}}
    elif hasattr(item, "json"):
        payload = item.json
    else:
        try:
            payload = item.to_json()
            payload = json.loads(payload)
        except Exception:
            payload = {{"raw": str(item)}}
    normalized.append(payload)
print(json.dumps({{"status": "ok", "results": normalized}}, indent=2))
"""
    env = {
        **os.environ,
        "DISABLE_MODEL_SOURCE_CHECK": "True",
        "PYTHONUNBUFFERED": "1",
    }
    try:
        completed = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=meta["timeout_seconds"],
            env=env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "engine": meta["engine"], "error": f"Local OCR timed out after {meta['timeout_seconds']}s."}

    if completed.returncode != 0:
        stderr = (completed.stderr or completed.stdout or "").strip()
        return {
            "ok": False,
            "engine": meta["engine"],
            "error": f"Local OCR subprocess failed with code {completed.returncode}. {stderr[:1200]}",
        }

    try:
        parsed = json.loads(completed.stdout.strip())
        return {"ok": True, "engine": meta["engine"], "payload": parsed}
    except Exception:
        return {
            "ok": False,
            "engine": meta["engine"],
            "error": f"Local OCR returned non-JSON output: {(completed.stdout or '')[:1200]}",
        }


def _normalize_local_ocr_payload(raw_payload: dict[str, Any], *, file_id: str, filename: str) -> dict[str, Any]:
    results = raw_payload.get("results") if isinstance(raw_payload, dict) else []
    visible_text: list[str] = []
    regions: list[dict[str, Any]] = []
    confidences: list[float] = []
    uncertainties: list[str] = []

    if not isinstance(results, list):
        results = []

    for item in results:
        rec_texts = item.get("rec_texts") if isinstance(item, dict) else None
        rec_scores = item.get("rec_scores") if isinstance(item, dict) else None
        rec_boxes = item.get("rec_boxes") if isinstance(item, dict) else None
        if isinstance(rec_texts, list):
            for idx, text in enumerate(rec_texts):
                if not str(text or "").strip():
                    continue
                visible_text.append(str(text))
                score = None
                if isinstance(rec_scores, list) and idx < len(rec_scores):
                    try:
                        score = float(rec_scores[idx])
                        confidences.append(score)
                    except Exception:
                        score = None
                box = rec_boxes[idx] if isinstance(rec_boxes, list) and idx < len(rec_boxes) else None
                regions.append(
                    {
                        "text": str(text),
                        "confidence": score,
                        "box": box,
                    }
                )
        elif isinstance(item, dict) and item.get("raw"):
            uncertainties.append("OCR result included raw/unparsed items.")

    confidence = round(sum(confidences) / len(confidences), 4) if confidences else None
    return {
        "status": "ok",
        "inspection_mode": "local_ocr",
        "engine": local_ocr_metadata()["engine"],
        "artifact_ref": f"attachment://{file_id}",
        "file_id": file_id,
        "filename": filename,
        "summary": _summarize_ocr_text(visible_text),
        "visible_text": visible_text,
        "regions": regions,
        "confidence": confidence,
        "ui_state": {},
        "uncertainties": uncertainties,
    }


async def _inspect_with_vlm(
    *,
    resolved_file_id: str,
    file_path: Path,
    question: str | None,
    output_format: str,
    verify_with_fusion: bool,
) -> dict[str, Any]:
    blocks = await file_ops.get_file_prompt_blocks(resolved_file_id, include_images=True)
    if not any(block.get("type") == "image_url" for block in blocks):
        return {
            "status": "error",
            "message": f"Unable to load image prompt blocks for '{_file_label(file_path)}'.",
        }

    provider = get_vision_provider()
    if provider is None:
        return {
            "status": "error",
            "message": "No delegated vision provider is configured. Set VISION_* env vars.",
        }

    original_name = _file_label(file_path)
    prompt_blocks: list[dict[str, Any]] = [{"type": "text", "text": _base_question(question, original_name)}]
    prompt_blocks.extend(blocks)

    max_tokens = int(os.getenv("VISION_MAX_TOKENS", "1200"))
    response = await provider.generate(
        system=_system_prompt(output_format),
        tools=[],
        messages=[{"role": "user", "content": prompt_blocks}],
        max_tokens=max_tokens,
        temperature=0.1,
        enable_thinking=False,
    )
    extracted = _extract_response_text(response)
    response_text = str(extracted.get("text") or "").strip()

    payload: dict[str, Any] = {
        "status": "ok",
        "inspection_mode": "vlm",
        "engine": response.model_name or provider.model_name,
        "artifact_ref": f"attachment://{resolved_file_id}",
        "file_id": resolved_file_id,
        "filename": original_name,
        "provider": response.provider_name or provider.provider_name,
        "model": response.model_name or provider.model_name,
        "route": "delegated_vision",
        "response_block_types": extracted.get("block_types") or [],
    }
    empty_response_meta = response.metadata.get("empty_response_diagnostics") if isinstance(response.metadata, dict) else None
    if not response.content and isinstance(empty_response_meta, dict):
        return {
            "status": "error",
            "error_kind": "empty_provider_response",
            "message": "Delegated vision provider returned no usable normalized content.",
            "inspection_mode": "vlm",
            "engine": response.model_name or provider.model_name,
            "artifact_ref": f"attachment://{resolved_file_id}",
            "file_id": resolved_file_id,
            "filename": original_name,
            "provider": response.provider_name or provider.provider_name,
            "model": response.model_name or provider.model_name,
            "route": "delegated_vision",
            "diagnostics": empty_response_meta,
            "response_block_types": extracted.get("block_types") or [],
        }
    if output_format == "structured":
        payload.update(_parse_structured_response(response_text))
    else:
        payload["summary"] = response_text

    if extracted.get("used_fallback"):
        payload.setdefault("uncertainties", [])
        if isinstance(payload["uncertainties"], list):
            payload["uncertainties"].append(
                "Delegated vision returned no text blocks; summary was recovered from non-text response blocks."
            )

    if verify_with_fusion:
        verifier = get_vision_verifier_provider()
        if verifier is not None:
            verify_response = await verifier.generate(
                system=_system_prompt("structured"),
                tools=[],
                messages=[{"role": "user", "content": prompt_blocks}],
                max_tokens=max_tokens,
                temperature=0.1,
                enable_thinking=False,
            )
            verify_extracted = _extract_response_text(verify_response)
            verify_text = str(verify_extracted.get("text") or "").strip()
            payload["verification"] = {
                "provider": verify_response.provider_name or verifier.provider_name,
                "model": verify_response.model_name or verifier.model_name,
                "response_block_types": verify_extracted.get("block_types") or [],
                "observation": _parse_structured_response(verify_text),
            }
            if verify_extracted.get("used_fallback"):
                observation = payload["verification"].get("observation")
                if isinstance(observation, dict):
                    uncertainties = observation.setdefault("uncertainties", [])
                    if isinstance(uncertainties, list):
                        uncertainties.append(
                            "Verification model returned no text blocks; observation was recovered from non-text response blocks."
                        )

    return payload


async def inspect_visual(
    *,
    artifact_ref: str | None = None,
    file_id: str | None = None,
    question: str | None = None,
    mode: str = "auto",
    output_format: str = "structured",
    verify_with_fusion: bool = False,
) -> str:
    resolved_file_id = _extract_file_id(artifact_ref or file_id or "")
    if not resolved_file_id:
        return json.dumps({"status": "error", "message": "inspect_visual requires artifact_ref or file_id."}, indent=2)

    file_path = file_ops._find_file_path(resolved_file_id)  # noqa: SLF001
    if not file_path:
        return json.dumps({"status": "error", "message": f"Image file '{resolved_file_id}' was not found."}, indent=2)

    if file_path.suffix.lower() not in file_ops.IMAGE_EXTENSIONS:
        return json.dumps({"status": "error", "message": f"File '{_file_label(file_path)}' is not a supported image."}, indent=2)

    normalized_mode = str(mode or "auto").strip().lower() or "auto"
    if normalized_mode not in {"auto", "local_ocr", "vlm"}:
        return json.dumps({"status": "error", "message": "inspect_visual mode must be one of: auto, local_ocr, vlm."}, indent=2)

    ocr_meta = local_ocr_metadata()
    vision_meta = vision_routing_metadata()
    selected_mode = normalized_mode
    if normalized_mode == "auto":
        selected_mode = "local_ocr" if _should_use_local_ocr_auto(question) else "vlm"

    if selected_mode == "local_ocr":
        local_result = _run_local_ocr_subprocess(file_path)
        if local_result.get("ok"):
            normalized = _normalize_local_ocr_payload(local_result["payload"], file_id=resolved_file_id, filename=_file_label(file_path))
            normalized["routing"] = {
                "requested_mode": normalized_mode,
                "selected_mode": "local_ocr",
                "local_ocr_configured": ocr_meta["configured"],
                "delegated_vision_route": vision_meta.get("route"),
            }
            return json.dumps(normalized, indent=2)

        if normalized_mode == "local_ocr":
            failed = {
                "status": "error",
                "inspection_mode": "local_ocr",
                "engine": ocr_meta["engine"],
                "artifact_ref": f"attachment://{resolved_file_id}",
                "file_id": resolved_file_id,
                "filename": _file_label(file_path),
                "message": local_result.get("error") or "Local OCR failed.",
            }
            return json.dumps(failed, indent=2)

        vlm_payload = await _inspect_with_vlm(
            resolved_file_id=resolved_file_id,
            file_path=file_path,
            question=question,
            output_format=output_format,
            verify_with_fusion=verify_with_fusion,
        )
        vlm_payload["routing"] = {
            "requested_mode": normalized_mode,
            "selected_mode": "vlm",
            "local_ocr_attempted": True,
            "local_ocr_error": local_result.get("error"),
            "delegated_vision_route": vision_meta.get("route"),
        }
        return json.dumps(vlm_payload, indent=2)

    vlm_payload = await _inspect_with_vlm(
        resolved_file_id=resolved_file_id,
        file_path=file_path,
        question=question,
        output_format=output_format,
        verify_with_fusion=verify_with_fusion,
    )
    vlm_payload["routing"] = {
        "requested_mode": normalized_mode,
        "selected_mode": "vlm",
        "local_ocr_configured": ocr_meta["configured"],
        "delegated_vision_route": vision_meta.get("route"),
    }
    return json.dumps(vlm_payload, indent=2)


async def inspect_image(
    *,
    artifact_ref: str | None = None,
    file_id: str | None = None,
    question: str | None = None,
    output_format: str = "structured",
    verify_with_fusion: bool = False,
) -> str:
    return await inspect_visual(
        artifact_ref=artifact_ref,
        file_id=file_id,
        question=question,
        mode="vlm",
        output_format=output_format,
        verify_with_fusion=verify_with_fusion,
    )
