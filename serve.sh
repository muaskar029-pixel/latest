#!/bin/sh
# Serve this repo at /latest/, like GitHub Pages does, so the /latest/ paths resolve.
# Usage: ./serve.sh [port]   then open http://localhost:8000/latest/
set -e
repo=$(cd "$(dirname "$0")" && pwd)
root=$(mktemp -d)
trap 'rm -rf "$root"' EXIT INT TERM
ln -s "$repo" "$root/latest"
echo "http://localhost:${1:-8000}/latest/"
cd "$root" && python3 -m http.server "${1:-8000}"
