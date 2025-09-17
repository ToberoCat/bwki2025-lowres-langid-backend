#!/usr/bin/env bash

URL="https://bwki2025-lowres-langid-backend.fly.dev/health"

while true; do
  echo "$(date): $(curl -s -o /dev/null -w "%{http_code}" "$URL")"
  sleep 30
done
