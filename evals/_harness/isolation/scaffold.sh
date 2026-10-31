#!/bin/bash
set -eu
exec bash "$(dirname "${BASH_SOURCE[0]}")/../../xSubsystemSweep/c7-mixer/scaffold.sh"
