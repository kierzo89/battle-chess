#!/bin/sh
set -eu
native_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cmake -S "$native_dir" -B "$native_dir/build" -DCMAKE_BUILD_TYPE=Debug
if [ "${1:-}" = "--viewer" ]; then
    shift
    cmake --build "$native_dir/build" --target battle-chess-linux -j 4
    exec "$native_dir/build/battle-chess-linux" "$native_dir/build/assets.bcframes" "$@"
fi
cmake --build "$native_dir/build" --target battle-chess-game -j 4
exec "$native_dir/build/battle-chess-game" "$native_dir/build/pieces.bcp" "$@"
