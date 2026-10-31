#!/bin/bash
# Usage: check.sh [source dir]. Builds the mixer and diffs its output against golden.txt.
set -eu
here="$(cd "$(dirname "$0")" && pwd)"
src="${1:-$here}"
out="$src/.build"
mkdir -p "$out"
c++ -std=c++20 -O2 -o "$out/mixer" "$src/main.cpp" "$src/mixer.cpp"
"$out/mixer" > "$out/actual.txt"
diff "$here/golden.txt" "$out/actual.txt"
echo "PASS"
