#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
  echo "Usage: $0 <node-name> <repo-id> <dest-root> [-- <extra hf args>]"
  echo "Example: $0 l4-360 Qwen/Qwen3-ASR-1.7B /mnt/aetherpro/models/audio/Qwen/Qwen3-ASR-1.7B"
  exit 1
fi

NODE_NAME="$1"
REPO_ID="$2"
DEST_ROOT="$3"
shift 3

is_allowed_dest() {
  local node="$1"
  local dest="$2"

  case "$node" in
    l40s-180)
      [[ "$dest" == /mnt/aetherpro-extra1/models* ]] \
      || [[ "$dest" == /mnt/aetherpro-extra1/llms* ]] \
      || [[ "$dest" == /mnt/aetherpro-extra2/models* ]] \
      || [[ "$dest" == /mnt/aetherpro-extra1/hf-cache* ]] \
      || [[ "$dest" == /mnt/aetherpro-extra2/hf* ]]
      ;;
    l4-360)
      [[ "$dest" == /mnt/aetherpro/models* ]] \
      || [[ "$dest" == /mnt/aetherpro/hf-cache* ]]
      ;;
    l40s-90)
      [[ "$dest" == /mnt/aetherpro/models* ]] \
      || [[ "$dest" == /mnt/aetherpro/llm* ]] \
      || [[ "$dest" == /mnt/aetherpro/hf* ]]
      ;;
    *)
      return 1
      ;;
  esac
}

if ! command -v hf >/dev/null 2>&1; then
  echo "Error: 'hf' CLI not found in PATH"
  exit 2
fi

if ! is_allowed_dest "$NODE_NAME" "$DEST_ROOT"; then
  echo "Refusing download: destination not approved for node '$NODE_NAME'"
  exit 3
fi

mkdir -p "$DEST_ROOT"

echo "Downloading $REPO_ID -> $DEST_ROOT"
hf download "$REPO_ID" --local-dir "$DEST_ROOT" "$@"
