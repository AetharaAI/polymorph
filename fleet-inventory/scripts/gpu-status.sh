#!/usr/bin/env bash
set -euo pipefail

echo "== HOST =="
hostname
echo

echo "== NVIDIA-SMI =="
nvidia-smi || true
echo

echo "== GPU TOPOLOGY =="
nvidia-smi topo -m || true
echo

echo "== GPU PROCESSES =="
nvidia-smi pmon -c 1 || true
