#!/bin/sh
set -eu
native_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cmake -S "$native_dir" -B "$native_dir/build" -DCMAKE_BUILD_TYPE=Debug
cmake --build "$native_dir/build" -j 4
exec "$native_dir/build/battle-chess-linux" "$native_dir/build/assets.bcframes" "$@"
