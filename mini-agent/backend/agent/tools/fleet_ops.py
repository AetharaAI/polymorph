from __future__ import annotations

import json
from typing import Any

from backend.fleet.manager import FleetManager


_MANAGER = FleetManager()


def _json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


async def show_fleet_status() -> str:
    return _json(_MANAGER.show_fleet_status())


async def show_node_inventory(node: str) -> str:
    return _json(_MANAGER.show_node_inventory(node))


async def locate_model(model_name_or_tag: str, node: str | None = None) -> str:
    return _json(
        {
            "query": model_name_or_tag,
            "node": node,
            "matches": _MANAGER.locate_model(model_name_or_tag, node_name=node),
        }
    )


async def find_candidate_nodes(requested_capability: str) -> str:
    return _json(
        {
            "requested_capability": requested_capability,
            "candidates": _MANAGER.find_candidate_nodes(requested_capability),
        }
    )


async def get_gpu_status(node: str, dry_run: bool = False) -> str:
    return _json(await _MANAGER.get_gpu_status(node, dry_run=dry_run))


async def get_disk_status(node: str, dry_run: bool = False) -> str:
    return _json(await _MANAGER.get_disk_status(node, dry_run=dry_run))


async def get_docker_status(node: str, dry_run: bool = False) -> str:
    return _json(await _MANAGER.get_docker_status(node, dry_run=dry_run))


async def validate_compose(node: str, compose_path: str | None = None, dry_run: bool = False) -> str:
    return _json(await _MANAGER.validate_compose(node, compose_path, dry_run=dry_run))


async def stop_stack(node: str, stack_name_or_path: str | None = None, dry_run: bool = True, confirm: bool = False) -> str:
    return _json(await _MANAGER.stop_stack(node, stack_name_or_path, dry_run=dry_run, confirm=confirm))


async def start_stack(node: str, stack_name_or_path: str | None = None, dry_run: bool = True, confirm: bool = False) -> str:
    return _json(await _MANAGER.start_stack(node, stack_name_or_path, dry_run=dry_run, confirm=confirm))


async def check_stack_health(node: str, stack_name_or_path: str | None = None, dry_run: bool = False) -> str:
    return _json(await _MANAGER.check_stack_health(node, stack_name_or_path, dry_run=dry_run))


async def audit_fleet_scripts() -> str:
    return _json({"scripts": _MANAGER.audit_scripts()})


async def plan_model_deployment(
    model_name_or_tag: str,
    node: str | None = None,
    repo_id: str | None = None,
    semantic_tags: list[str] | None = None,
    compose_path: str | None = None,
    execute: bool = False,
    dry_run: bool = True,
    confirm: bool = False,
) -> str:
    return _json(
        await _MANAGER.plan_model_deployment(
            model_name_or_tag=model_name_or_tag,
            node_name=node,
            repo_id=repo_id,
            semantic_tags=semantic_tags,
            compose_path=compose_path,
            execute=execute,
            dry_run=dry_run,
            confirm=confirm,
        )
    )
