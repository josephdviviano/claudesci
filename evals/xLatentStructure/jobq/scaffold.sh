#!/bin/bash
set -eu
cp -R "$(dirname "${BASH_SOURCE[0]}")"/fixture/. .
git init -q
git add -A
git -c user.name=eval -c user.email=eval@example.invalid commit -qm fixture
