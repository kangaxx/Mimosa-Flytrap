#!/usr/bin/env bash
set -euo pipefail

EXAMPLE=.env.example
TARGET=.env

if [ ! -f "$EXAMPLE" ]; then
  echo "No $EXAMPLE found in $(pwd). Nothing to sync." >&2
  exit 1
fi

if [ ! -f "$TARGET" ]; then
  cp "$EXAMPLE" "$TARGET"
  echo "No $TARGET found — copied $EXAMPLE -> $TARGET"
  exit 0
fi

BACKUP="${TARGET}.bak.$(date +%s)"
cp "$TARGET" "$BACKUP"
echo "Backed up existing $TARGET -> $BACKUP"

# Append missing keys from example; keep existing values in .env
while IFS= read -r line || [ -n "$line" ]; do
  case "$line" in
    ''|\#*) continue ;;
  esac

  key=${line%%=*}
  if [ -z "$key" ]; then
    continue
  fi

  if grep -qE "^${key}=" "$TARGET"; then
    :
  else
    echo "$line" >> "$TARGET"
    echo "Appended missing key $key to $TARGET"
  fi
done < "$EXAMPLE"

echo "Sync complete. Backup at $BACKUP"
