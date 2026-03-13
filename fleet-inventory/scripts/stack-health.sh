#!/usr/bin/env bash
set -euo pipefail

COMPOSE_ROOT="${1:-$HOME/aether-model-node/control}"

if [[ ! -d "$COMPOSE_ROOT" ]]; then
  echo "Compose root not found: $COMPOSE_ROOT"
  exit 1
fi

cd "$COMPOSE_ROOT"

echo "== COMPOSE PS =="
docker compose ps
echo

echo "== CONTAINER HEALTH =="
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
