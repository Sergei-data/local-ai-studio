#!/usr/bin/env bash
set -euo pipefail

echo "=== Ollama service ==="
systemctl status ollama --no-pager || true

echo
echo "=== Effective environment ==="
systemctl show ollama -p Environment --value | tr ' ' '\n'

echo
echo "=== Listening sockets ==="
ss -tuln | grep 11434 || true

echo
echo "=== API tags ==="
curl -s http://127.0.0.1:11434/api/tags || true
echo
