#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE_FILE="$PROJECT_ROOT/ops/ollama/ollama.service.override.conf"
TARGET_DIR="/etc/systemd/system/ollama.service.d"
TARGET_FILE="$TARGET_DIR/override.conf"

echo "Project root: $PROJECT_ROOT"
echo "Source: $SOURCE_FILE"
echo "Target: $TARGET_FILE"

if [[ ! -f "$SOURCE_FILE" ]]; then
  echo "Source file not found: $SOURCE_FILE" >&2
  exit 1
fi

sudo mkdir -p "$TARGET_DIR"
sudo cp "$SOURCE_FILE" "$TARGET_FILE"

sudo mkdir -p /srv/ollama-models
sudo chown -R ollama:ollama /srv/ollama-models
sudo chmod 755 /srv/ollama-models

sudo systemctl daemon-reload
sudo systemctl restart ollama

echo
echo "Installed override:"
sudo systemctl cat ollama.service

echo
echo "Effective environment:"
systemctl show ollama -p Environment --value | tr ' ' '\n'
