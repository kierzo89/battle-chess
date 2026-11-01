#!/bin/sh
set -eu
native_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
log_dir="${XDG_STATE_HOME:-$HOME/.local/state}/battle-chess-native"
mkdir -p "$log_dir"
exec "$native_dir/run.sh" >>"$log_dir/launch.log" 2>&1
