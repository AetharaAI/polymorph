#!/usr/bin/env bash
set -euo pipefail

echo "== HOST =="
hostname
echo

echo "== FILESYSTEM USAGE =="
df -h
echo

echo "== INODE USAGE =="
df -i
echo

echo "== BLOCK DEVICES =="
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,TYPE
echo

echo "== MOUNTS =="
mount | sort
