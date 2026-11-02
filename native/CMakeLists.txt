cmake_minimum_required(VERSION 3.20)
project(battle_chess_linux C)
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
find_package(PkgConfig REQUIRED)
pkg_check_modules(SDL3 REQUIRED IMPORTED_TARGET sdl3>=3.2)
find_package(Python3 REQUIRED COMPONENTS Interpreter)
add_library(bc_core src/board.c src/rules.c src/history.c src/savegame.c)
target_include_directories(bc_core PUBLIC src)
target_compile_options(bc_core PRIVATE -Wall -Wextra -Wpedantic -Werror)
add_executable(battle-chess-linux src/main.c)
target_link_libraries(battle-chess-linux PRIVATE bc_core PkgConfig::SDL3)
target_compile_options(battle-chess-linux PRIVATE -Wall -Wextra -Wpedantic -Werror)
set(ASSET_FILE "${CMAKE_CURRENT_BINARY_DIR}/assets.bcframes")
file(GLOB_RECURSE ASSET_INPUTS CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/animations/*" "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/images/palette.json")
add_custom_command(OUTPUT "${ASSET_FILE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_assets.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${ASSET_FILE}"
 DEPENDS tools/prepare_assets.py ../verification/asset-snapshot.json ${ASSET_INPUTS}
 VERBATIM)
add_custom_target(native_assets ALL DEPENDS "${ASSET_FILE}")
add_dependencies(battle-chess-linux native_assets)
enable_testing()
add_executable(test_core tests/test_core.c)
target_link_libraries(test_core PRIVATE bc_core)
target_compile_options(test_core PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME board_state COMMAND test_core)
add_test(NAME asset_render COMMAND battle-chess-linux "${ASSET_FILE}" --smoke)
set_tests_properties(asset_render PROPERTIES ENVIRONMENT "SDL_VIDEODRIVER=dummy;SDL_RENDER_DRIVER=software")
add_executable(test_rules tests/test_rules.c)
target_link_libraries(test_rules PRIVATE bc_core)
target_compile_options(test_rules PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME legal_rules COMMAND test_rules)
# Exact recovered files are compiled read-only; shim adapts DOS memset byte count.
add_executable(test_original_attacks tests/test_original_attacks.c
 ../matching/src/init_rays_tables_match.c ../matching/src/piece_attacks_match.c
 ../matching/src/pawn_attacks_match.c ../matching/src/data/move_lookup_tables.c)
set_target_properties(test_original_attacks PROPERTIES C_STANDARD 99)
target_compile_options(test_original_attacks PRIVATE -UNDEBUG)
target_link_libraries(test_original_attacks PRIVATE bc_core)
add_test(NAME recovered_attack_equivalence COMMAND test_original_attacks)
file(GLOB EVALUATION_DATA CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/../matching/src/data/evaluation_*.c")
set(EVALUATION_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/evaluation.c")
add_custom_command(OUTPUT "${EVALUATION_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/port_evaluation.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${EVALUATION_SOURCE}"
 DEPENDS tools/port_evaluation.py ../matching/src/full_evaluation_match.c
 ../matching/src/data/move_lookup_tables.c ${EVALUATION_DATA} VERBATIM)
add_library(bc_evaluation "${EVALUATION_SOURCE}")
target_include_directories(bc_evaluation PUBLIC src)
# Retain original unused compiler-shaping locals and assignment conditions.
target_compile_options(bc_evaluation PRIVATE -fno-strict-aliasing)
add_executable(test_evaluation tests/test_evaluation.c)
target_link_libraries(test_evaluation PRIVATE bc_evaluation bc_core)
target_compile_options(test_evaluation PRIVATE -UNDEBUG)
add_test(NAME recovered_evaluation COMMAND test_evaluation)
add_test(NAME evaluation_source_gate COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_evaluation_generator.py")
add_executable(test_history tests/test_history.c)
target_link_libraries(test_history PRIVATE bc_core)
target_compile_options(test_history PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME turn_history COMMAND test_history)
add_executable(test_original_history tests/test_original_history.c ../matching/src/repetition_match.c)
target_link_libraries(test_original_history PRIVATE bc_core)
target_compile_options(test_original_history PRIVATE -UNDEBUG)
add_test(NAME recovered_history_equivalence COMMAND test_original_history)
add_executable(test_delta tests/test_delta.c)
target_link_libraries(test_delta PRIVATE bc_evaluation bc_core)
target_compile_options(test_delta PRIVATE -UNDEBUG)
add_test(NAME incremental_evaluation COMMAND test_delta)
set(SEARCH_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/search.c")
add_custom_command(OUTPUT "${SEARCH_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/port_search.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${SEARCH_SOURCE}"
 DEPENDS tools/port_search.py src/search_adapter.inc ../matching/src/search_engine_a4d4_b9ba_match.c VERBATIM)
add_library(bc_search "${SEARCH_SOURCE}" src/difficulty.c)
target_include_directories(bc_search PUBLIC src)
target_link_libraries(bc_search PUBLIC bc_core bc_evaluation)
target_compile_options(bc_search PRIVATE -fno-strict-aliasing)
add_executable(test_search tests/test_search.c)
target_link_libraries(test_search PRIVATE bc_search)
target_compile_options(test_search PRIVATE -UNDEBUG)
add_test(NAME recovered_search_smoke COMMAND test_search)
set_tests_properties(recovered_search_smoke PROPERTIES TIMEOUT 30)
add_executable(test_difficulty tests/test_difficulty.c)
target_link_libraries(test_difficulty PRIVATE bc_search)
target_compile_options(test_difficulty PRIVATE -UNDEBUG)
add_test(NAME difficulty_clock COMMAND test_difficulty)
file(GLOB BOARD_INPUTS CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/setups/*.bin"
 "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/setups/report.json"
 "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/images/palette.json"
 "${CMAKE_CURRENT_SOURCE_DIR}/../assets/recovered/bank1/*.background-packed.bin")
set(BOARD_ASSETS "${CMAKE_CURRENT_BINARY_DIR}/pieces.bcp")
add_custom_command(OUTPUT "${BOARD_ASSETS}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_board_assets.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${BOARD_ASSETS}"
 DEPENDS tools/prepare_board_assets.py ../verification/asset-snapshot.json ${BOARD_INPUTS} ${ASSET_INPUTS} ../assets/recovered/metadata/timing/timelines.json VERBATIM)
add_custom_target(board_assets ALL DEPENDS "${BOARD_ASSETS}")
add_executable(battle-chess-game src/game_ui.c src/board_view.c)
target_link_libraries(battle-chess-game PRIVATE bc_search PkgConfig::SDL3)
add_dependencies(battle-chess-game board_assets)
add_test(NAME native_game_smoke COMMAND battle-chess-game "${BOARD_ASSETS}" --smoke)
set_tests_properties(native_game_smoke PROPERTIES ENVIRONMENT "SDL_VIDEODRIVER=dummy;SDL_RENDER_DRIVER=software" TIMEOUT 15)

add_executable(test_savegame tests/test_savegame.c)
target_link_libraries(test_savegame PRIVATE bc_core)
target_compile_options(test_savegame PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME savegame_roundtrip COMMAND test_savegame)
add_executable(test_fullgame tests/test_fullgame.c)
target_link_libraries(test_fullgame PRIVATE bc_search)
target_compile_options(test_fullgame PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME native_full_games COMMAND test_fullgame)
set_tests_properties(native_full_games PROPERTIES TIMEOUT 60)
add_library(bc_presentation src/presentation.c src/motion.c)
target_link_libraries(bc_presentation PUBLIC bc_core)
target_link_libraries(battle-chess-game PRIVATE bc_presentation)
target_include_directories(bc_presentation PUBLIC src)
target_compile_options(bc_presentation PRIVATE -Wall -Wextra -Wpedantic -Werror)
# Shared copy lets the fixture test call the same C implementation directly.
add_library(presentation_oracle SHARED src/presentation.c)
target_include_directories(presentation_oracle PRIVATE src)
add_test(NAME recovered_presentation_timing COMMAND ${Python3_EXECUTABLE}
 "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_presentation.py" $<TARGET_FILE:presentation_oracle> ${CMAKE_C_COMPILER})
add_executable(test_motion tests/test_motion.c)
target_link_libraries(test_motion PRIVATE bc_presentation)
target_compile_options(test_motion PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME native_piece_motion COMMAND test_motion)

set(STAGE_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/stage.c")
add_custom_command(OUTPUT "${STAGE_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/port_stage.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${STAGE_SOURCE}"
 DEPENDS tools/port_stage.py ../matching/src/animation_stage_match.c
 ../matching/src/data/capture_record_mapping_11ac.c ../matching/src/data/game_kind_map.c VERBATIM)
target_sources(bc_presentation PRIVATE "${STAGE_SOURCE}")
# Keep the recovered queue handle local even though the original never reads it.
set_source_files_properties("${STAGE_SOURCE}" PROPERTIES COMPILE_OPTIONS "-Wno-unused-but-set-variable")
add_executable(test_stage tests/test_stage.c)
target_link_libraries(test_stage PRIVATE bc_presentation)
target_compile_options(test_stage PRIVATE -Wall -Wextra -Wpedantic -Werror -UNDEBUG)
add_test(NAME recovered_move_commands COMMAND test_stage)
set(GEOMETRY_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/geometry.c")
add_custom_command(OUTPUT "${GEOMETRY_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_geometry.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${GEOMETRY_SOURCE}"
 DEPENDS tools/prepare_geometry.py evidence/rea-board-coordinates.json
 ../verification/source-snapshot.json ../matching/src/data/frame_index_flat_0166.c
 ../matching/src/data/game_kind_map.c ../matching/src/queue_piece_match.c VERBATIM)
target_sources(bc_presentation PRIVATE "${GEOMETRY_SOURCE}")
add_library(geometry_oracle SHARED "${GEOMETRY_SOURCE}")
target_include_directories(geometry_oracle PRIVATE src)
add_test(NAME recovered_board_geometry COMMAND ${Python3_EXECUTABLE}
 "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_geometry.py" $<TARGET_FILE:geometry_oracle> ${CMAKE_C_COMPILER})

add_test(NAME native_flat_game_smoke COMMAND battle-chess-game "${BOARD_ASSETS}" --smoke-flat)
set_tests_properties(native_flat_game_smoke PROPERTIES ENVIRONMENT "SDL_VIDEODRIVER=dummy;SDL_RENDER_DRIVER=software" TIMEOUT 15)

set(WALK_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/walk.c")
add_custom_command(OUTPUT "${WALK_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_walk.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${WALK_SOURCE}"
 DEPENDS tools/prepare_walk.py ../verification/asset-snapshot.json
 ../assets/recovered/metadata/timing/report.json ${ASSET_INPUTS} VERBATIM)
target_sources(bc_presentation PRIVATE "${WALK_SOURCE}")
add_library(walk_oracle SHARED "${WALK_SOURCE}" src/presentation.c)
target_include_directories(walk_oracle PRIVATE src)
add_test(NAME recovered_walk_tasks COMMAND ${Python3_EXECUTABLE}
 "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_walk.py" $<TARGET_FILE:walk_oracle>)

set(TURN_SOURCE "${CMAKE_CURRENT_BINARY_DIR}/generated/turn_animation_data.c")
add_custom_command(OUTPUT "${TURN_SOURCE}"
 COMMAND ${Python3_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/tools/prepare_turn.py"
 --root "${CMAKE_CURRENT_SOURCE_DIR}/.." --output "${TURN_SOURCE}"
 DEPENDS tools/prepare_turn.py ../verification/asset-snapshot.json
 ../assets/recovered/metadata/timing/report.json ${ASSET_INPUTS} VERBATIM)
target_sources(bc_presentation PRIVATE "${TURN_SOURCE}" src/turn_animation.c)
add_library(turn_oracle SHARED "${TURN_SOURCE}" src/turn_animation.c src/presentation.c)
target_include_directories(turn_oracle PRIVATE src)
add_test(NAME recovered_turn_tasks COMMAND ${Python3_EXECUTABLE}
 "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_turn_animation.py" $<TARGET_FILE:turn_oracle>)

target_sources(bc_presentation PRIVATE src/compositor.c)
add_library(compositor_oracle SHARED src/compositor.c)
target_include_directories(compositor_oracle PRIVATE src)
add_test(NAME recovered_frame_composition COMMAND ${Python3_EXECUTABLE}
 "${CMAKE_CURRENT_SOURCE_DIR}/tests/test_compositor.py" $<TARGET_FILE:compositor_oracle>)
