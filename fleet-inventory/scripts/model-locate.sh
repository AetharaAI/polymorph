#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <node-name> <pattern>"
  exit 1
fi

NODE_NAME="$1"
PATTERN="$2"

case "$NODE_NAME" in
  l40s-180)
    ROOTS=(
      /mnt/aetherpro/models
      /mnt/aetherpro-extra1/models
      /mnt/aetherpro-extra1/llms
      /mnt/aetherpro-extra2/models
    )
    ;;
  l4-360)
    ROOTS=(
      /mnt/aetherpro/models
    )
    ;;
  l40s-90)
    ROOTS=(
      /mnt/aetherpro/models
      /mnt/aetherpro/llm
    )
    ;;
  *)
    echo "Unknown node: $NODE_NAME"
    exit 2
    ;;
esac

for root in "${ROOTS[@]}"; do
  [[ -d "$root" ]] || continue
  find "$root" -iname "*${PATTERN}*" 2>/dev/null
done
