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

while IFS= read -r line || [ -n "$line" ]; do
  # skip comments and empty lines
  case "$line" in
    ''|\#*) continue ;;
  esac
  key=${line%%=*}
  val=${line#*=}

  if grep -qE "^${key}=" "$TARGET"; then
    if [ "$key" = "DEEPSEEK_MODEL" ]; then
      # replace the line for this key using awk to be portable
      tmp=$(mktemp)
      awk -v k="$key" -v v="$val" 'BEGIN{FS=OFS="="} $1==k{$0=k"="v; print}' "$TARGET" > "$tmp" && mv "$tmp" "$TARGET"
      echo "Updated $key in $TARGET to example value"
    else
      # leave existing value as-is
      :
    fi
  else
    echo "$line" >> "$TARGET"
    echo "Appended missing key $key to $TARGET"
  fi
done < "$EXAMPLE"

echo "Sync complete. Backup at $BACKUP"
