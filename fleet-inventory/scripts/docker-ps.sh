#!/usr/bin/env bash
set -euo pipefail

echo "== HOST =="
hostname
echo

echo "== DOCKER PS =="
docker ps -a
echo

echo "== DOCKER COMPOSE LS =="
docker compose ls || true
