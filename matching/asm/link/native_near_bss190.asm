; Reconstructed uninitialized native RAM machine views; not historical C objects.
; Extent from CRTclear52CC..CBE0 and originalDOS minimum allocation, not address-gap C capacities.
; Existing C private BSS4 remains outside this module; no initialized bytes or byte credit.
bits 16
cpu 8086
segment _BSS public align=2 class=BSS use16
segment XOB public align=2 class=BSS use16
segment XO public align=2 class=BSS use16
segment XOE public align=2 class=BSS use16
segment BC_NATIVE_LATE public align=16 class=BSS use16
group DGROUP _BSS XOB XO XOE BC_NATIVE_LATE
global _active_8e22
global _active_95fe
global _active_964e
global _active_a834
global _active_actor
global _active_arena_9344
global _active_data_b0ca
global _active_lists_b080
global _actor_flag_9374
global _actor_map
global _animation_busy
global _animation_counter
global _animation_tasks
global _arena_capacity
global _arena_cursor
global _asset_drive_count
global _asset_drive_fallback
global _asset_lengths
global _asset_offsets
global _asset_table_53f8
global _asset_table_8ae4
global _background
global _best
global _board
global _book_choice_offset
global _book_matches
global _book_saved_index
global _book_state_index
global _border
global _buttons_8d04
global _byte_read_cursor
global _byte_ring_buffer
global _byte_write_cursor
global _cached_frames
global _castle_owner
global _check_8f44
global _check_state
global _checkpoint_8180
global _checkpoint_8186
global _checkpoint_936e
global _checkpoint_987e
global _checkpoint_arena_9368
global _checkpoint_data_933e
global _checkpoint_lists_a84e
global _clock_epoch
global _clock_sample
global _clock_value
global _command_root
global _command_words_8d2c
global _commands
global _current
global _current_controls
global _current_event
global _current_side
global _current_ticks_9884
global _cursor_actor_57d0
global _cursor_colour_9850
global _cursor_frames_820e
global _dialog_event
global _dialog_selected
global _directory_lists
global _dirty_bottom
global _dirty_left
global _dirty_right
global _dirty_top
global _endgame
global _event_context
global _finished
global _first_score
global _flash_rank_b0a3
global _foreground
global _frame_data_cursor
global _frame_descriptors
global _frame_directory
global _frame_index
global _frame_indices
global _frame_list_cursor
global _frame_lists
global _frame_metadata
global _frame_resources
global _frame_words
global _frames
global _height
global _hint_line
global _hint_score_964c
global _history
global _history_index
global _history_move_counter
global _history_storage
global _history_tail
global _home_pawn
global _input_flag_8fe0
global _input_mode_984e
global _input_state
global _interrupted
global _iteration
global _last_event_ticks_b07a
global _last_key_8dcc
global _left_controls
global _left_lists
global _limit
global _marked_square_8dd6
global _material_balance
global _menu_blink
global _menu_columns
global _menu_last
global _menu_positions
global _menu_state
global _menu_x
global _menu_y
global _menus
global _metadata_records
global _mode_8176
global _mode_8188
global _motion_x
global _motion_y
global _move_count
global _move_list
global _opponent
global _packed_pen
global _pair_directory_lengths
global _pair_offsets
global _paused
global _pawn_bonus_side
global _pawn_mask
global _pawn_material
global _pawn_state
global _pen_x
global _pen_y
global _phase
global _piece_controls
global _piece_counts
global _piece_square
global _pieces
global _pointer_x
global _pointer_y
global _position_score
global _previous_buttons_9888
global _rays
global _ready_9856
global _region_left
global _region_right
global _region_width
global _remote_board_b082
global _remote_move_817a
global _requested_limit
global _right_controls
global _right_lists
global _row_mask_9230
global _saved
global _saved_cursor_8d0a
global _saved_history_index
global _saved_name_count_52d4
global _saved_state
global _screen_x
global _screen_y
global _search_active
global _search_frames
global _search_level
global _search_options
global _search_pair_moves
global _search_side
global _selected_move
global _serial_irq_flags_b0d4
global _setup_lengths
global _setup_offsets
global _setup_word_934a
global _setup_word_9646
global _setup_word_9844
global _side_info_9604
global _side_piece_counts
global _square_x
global _square_y
global _startup_lengths_a8b6
global _startup_offsets_9648
global _state_57cc
global _state_8d12
global _state_8fde
global _state_934c
global _state_cbd2
global _state_index
global _stride
global _task_pool
global _temporary
global _timer_b
global _total_material
global _values
global _window_limit
global _working_follow_8bb6
global _working_move
segment _BSS
_castle_owner: ; native DS 52D0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dialog_selected: ; native DS 52D2 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_saved_name_count_52d4: ; native DS 52D4 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dialog_event: ; native DS 52D6 machine address
    resb 20 ; complete aggregate CRT-cleared RAM span
segment BC_NATIVE_LATE
_commands: ; native DS 52F0 machine address
    resb 256 ; opaque RAM reserve; no per-object capacity claim
_event_context: ; native DS 53F0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_requested_limit: ; native DS 53F2 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_first_score: ; native DS 53F6 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_asset_table_53f8: ; native DS 53F8 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_positions: ; native DS 53FA machine address
    resb 10 ; opaque RAM reserve; no per-object capacity claim
_rays: ; native DS 5404 machine address
    resb 956 ; opaque RAM reserve; no per-object capacity claim
_pawn_material: ; native DS 57C0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_search_options: ; native DS 57C2 machine address
    resb 6 ; opaque RAM reserve; no per-object capacity claim
_temporary: ; native DS 57C8 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_state_57cc: ; native DS 57CC machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_asset_drive_fallback: ; native DS 57CE machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_cursor_actor_57d0: ; native DS 57D0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_search_frames: ; native DS 57D2 machine address
    resb 10656 ; opaque RAM reserve; no per-object capacity claim
_packed_pen: ; native DS 8172 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_mode_8176: ; native DS 8176 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_remote_move_817a: ; native DS 817A machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pair_offsets: ; native DS 817C machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_8180: ; native DS 8180 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_phase: ; native DS 8182 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_saved_history_index: ; native DS 8184 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_8186: ; native DS 8186 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_mode_8188: ; native DS 8188 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_limit: ; native DS 818A machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_frames: ; native DS 818E machine address
    resb 128 ; opaque RAM reserve; no per-object capacity claim
_cursor_frames_820e: ; native DS 820E machine address
    resb 592 ; opaque RAM reserve; no per-object capacity claim
_move_count: ; native DS 845E machine address
    resb 26 ; opaque RAM reserve; no per-object capacity claim
_frame_lists: ; native DS 8478 machine address
    resb 300 ; opaque RAM reserve; no per-object capacity claim
_history_storage: ; native DS 85A4 machine address
_saved: ; native DS 85A4 machine address
_saved_state: ; native DS 85A4 machine address
    resb 824 ; opaque RAM reserve; no per-object capacity claim
_history: ; native DS 88DC machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_history_tail: ; native DS 88E4 machine address
    resb 192 ; opaque RAM reserve; no per-object capacity claim
_frame_indices: ; native DS 89A4 machine address
    resb 256 ; opaque RAM reserve; no per-object capacity claim
_actor_map: ; native DS 8AA4 machine address
    resb 64 ; opaque RAM reserve; no per-object capacity claim
_asset_table_8ae4: ; native DS 8AE4 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_byte_read_cursor: ; native DS 8AE6 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_frame_resources: ; native DS 8AE8 machine address
    resb 68 ; opaque RAM reserve; no per-object capacity claim
_window_limit: ; native DS 8B2C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_byte_ring_buffer: ; native DS 8B2E machine address
    resb 128 ; opaque RAM reserve; no per-object capacity claim
_working_move: ; native DS 8BAE machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_working_follow_8bb6: ; native DS 8BB6 machine address
    resb 184 ; opaque RAM reserve; no per-object capacity claim
_left_controls: ; native DS 8C6E machine address
    resb 72 ; opaque RAM reserve; no per-object capacity claim
_right_controls: ; native DS 8CB6 machine address
    resb 72 ; opaque RAM reserve; no per-object capacity claim
_book_state_index: ; native DS 8CFE machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pair_directory_lengths: ; native DS 8D00 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_buttons_8d04: ; native DS 8D04 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_square_x: ; native DS 8D06 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dirty_bottom: ; native DS 8D08 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_saved_cursor_8d0a: ; native DS 8D0A machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_square_y: ; native DS 8D0C machine address
    resb 6 ; opaque RAM reserve; no per-object capacity claim
_state_8d12: ; native DS 8D12 machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_values: ; native DS 8D1A machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_foreground: ; native DS 8D22 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pawn_mask: ; native DS 8D24 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pen_x: ; native DS 8D26 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_material_balance: ; native DS 8D28 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pen_y: ; native DS 8D2A machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_command_words_8d2c: ; native DS 8D2C machine address
    resb 160 ; opaque RAM reserve; no per-object capacity claim
_last_key_8dcc: ; native DS 8DCC machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_side_piece_counts: ; native DS 8DCE machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_menu_columns: ; native DS 8DD2 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_height: ; native DS 8DD4 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_marked_square_8dd6: ; native DS 8DD6 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_x: ; native DS 8DD8 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menus: ; native DS 8DDA machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_y: ; native DS 8DDC machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_state: ; native DS 8DDE machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_best: ; native DS 8DE0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_search_side: ; native DS 8DE2 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_asset_offsets: ; native DS 8DE4 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_iteration: ; native DS 8DE8 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_home_pawn: ; native DS 8DEA machine address
    resb 10 ; opaque RAM reserve; no per-object capacity claim
_piece_controls: ; native DS 8DF4 machine address
    resb 46 ; opaque RAM reserve; no per-object capacity claim
_active_8e22: ; native DS 8E22 machine address
    resb 290 ; opaque RAM reserve; no per-object capacity claim
_check_8f44: ; native DS 8F44 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_left_lists: ; native DS 8F46 machine address
    resb 72 ; opaque RAM reserve; no per-object capacity claim
_right_lists: ; native DS 8F8E machine address
    resb 72 ; opaque RAM reserve; no per-object capacity claim
_timer_b: ; native DS 8FD6 machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_state_8fde: ; native DS 8FDE machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_input_flag_8fe0: ; native DS 8FE0 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pawn_bonus_side: ; native DS 8FE2 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pawn_state: ; native DS 8FE4 machine address
    resb 200 ; opaque RAM reserve; no per-object capacity claim
_search_pair_moves: ; native DS 90AC machine address
    resb 384 ; opaque RAM reserve; no per-object capacity claim
_position_score: ; native DS 922C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dirty_left: ; native DS 922E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_row_mask_9230: ; native DS 9230 machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_arena_cursor: ; native DS 9238 machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_setup_offsets: ; native DS 9240 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_check_state: ; native DS 9244 machine address
    resb 54 ; opaque RAM reserve; no per-object capacity claim
_hint_line: ; native DS 927A machine address
    resb 192 ; opaque RAM reserve; no per-object capacity claim
_pointer_x: ; native DS 933A machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_blink: ; native DS 933C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_data_933e: ; native DS 933E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_interrupted: ; native DS 9340 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_byte_write_cursor: ; native DS 9342 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_active_arena_9344: ; native DS 9344 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_border: ; native DS 9348 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_setup_word_934a: ; native DS 934A machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_state_934c: ; native DS 934C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_metadata_records: ; native DS 934E machine address
    resb 16 ; opaque RAM reserve; no per-object capacity claim
_pointer_y: ; native DS 935E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_background: ; native DS 9360 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_motion_x: ; native DS 9362 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dirty_right: ; native DS 9364 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_book_saved_index: ; native DS 9366 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_arena_9368: ; native DS 9368 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_frame_data_cursor: ; native DS 936C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_936e: ; native DS 936E machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_stride: ; native DS 9372 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_actor_flag_9374: ; native DS 9374 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_motion_y: ; native DS 9376 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_dirty_top: ; native DS 9378 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_move_list: ; native DS 937A machine address
    resb 640 ; opaque RAM reserve; no per-object capacity claim
_search_active: ; native DS 95FA machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_active_95fe: ; native DS 95FE machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_animation_counter: ; native DS 9602 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_pieces: ; native DS 9604 machine address
_side_info_9604: ; native DS 9604 machine address
    resb 64 ; opaque RAM reserve; no per-object capacity claim
_region_right: ; native DS 9644 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_setup_word_9646: ; native DS 9646 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_startup_offsets_9648: ; native DS 9648 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_hint_score_964c: ; native DS 964C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_active_964e: ; native DS 964E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_frame_directory: ; native DS 9650 machine address
    resb 500 ; opaque RAM reserve; no per-object capacity claim
_setup_word_9844: ; native DS 9844 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_current_side: ; native DS 9846 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_asset_lengths: ; native DS 9848 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_history_move_counter: ; native DS 984C machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_input_mode_984e: ; native DS 984E machine address
    resb 1 ; opaque RAM reserve; no per-object capacity claim
_command_root: ; native DS 984F machine address
    resb 1 ; opaque RAM reserve; no per-object capacity claim
_cursor_colour_9850: ; native DS 9850 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_animation_busy: ; native DS 9852 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_input_state: ; native DS 9854 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_ready_9856: ; native DS 9856 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_frame_descriptors: ; native DS 985A machine address
    resb 32 ; opaque RAM reserve; no per-object capacity claim
_setup_lengths: ; native DS 987A machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_987e: ; native DS 987E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_history_index: ; native DS 9880 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_current_event: ; native DS 9882 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_current_ticks_9884: ; native DS 9884 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_previous_buttons_9888: ; native DS 9888 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_asset_drive_count: ; native DS 988A machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_paused: ; native DS 988E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_frame_index: ; native DS 9890 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_frame_words: ; native DS 9892 machine address
    resb 4002 ; opaque RAM reserve; no per-object capacity claim
_active_a834: ; native DS A834 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_opponent: ; native DS A836 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_search_level: ; native DS A838 machine address
    resb 22 ; opaque RAM reserve; no per-object capacity claim
_checkpoint_lists_a84e: ; native DS A84E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_active_actor: ; native DS A850 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_state_index: ; native DS A852 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_animation_tasks: ; native DS A854 machine address
    resb 98 ; opaque RAM reserve; no per-object capacity claim
_startup_lengths_a8b6: ; native DS A8B6 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_board: ; native DS A8BA machine address
    resb 482 ; opaque RAM reserve; no per-object capacity claim
_frame_metadata: ; native DS AA9C machine address
    resb 1500 ; opaque RAM reserve; no per-object capacity claim
_directory_lists: ; native DS B078 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_last_event_ticks_b07a: ; native DS B07A machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_frame_list_cursor: ; native DS B07E machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_active_lists_b080: ; native DS B080 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_remote_board_b082: ; native DS B082 machine address
    resb 33 ; opaque RAM reserve; no per-object capacity claim
_flash_rank_b0a3: ; native DS B0A3 machine address
    resb 1 ; opaque RAM reserve; no per-object capacity claim
_total_material: ; native DS B0A4 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_piece_counts: ; native DS B0A6 machine address
    resb 6 ; opaque RAM reserve; no per-object capacity claim
_selected_move: ; native DS B0AC machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_arena_capacity: ; native DS B0B4 machine address
    resb 6 ; opaque RAM reserve; no per-object capacity claim
_region_left: ; native DS B0BA machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_task_pool: ; native DS B0BE machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_screen_x: ; native DS B0C6 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_screen_y: ; native DS B0C8 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_active_data_b0ca: ; native DS B0CA machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_book_matches: ; native DS B0CC machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_current_controls: ; native DS B0CE machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_book_choice_offset: ; native DS B0D2 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_serial_irq_flags_b0d4: ; native DS B0D4 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_endgame: ; native DS B0D6 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_region_width: ; native DS B0D8 machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_menu_last: ; native DS B0DA machine address
    resb 2 ; opaque RAM reserve; no per-object capacity claim
_piece_square: ; native DS B0DC machine address
    resb 2882 ; opaque RAM reserve; no per-object capacity claim
_cached_frames: ; native DS BC1E machine address
    resb 4000 ; opaque RAM reserve; no per-object capacity claim
_clock_epoch: ; native DS CBBE machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_clock_sample: ; native DS CBC2 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_clock_value: ; native DS CBC6 machine address
    resb 4 ; opaque RAM reserve; no per-object capacity claim
_current: ; native DS CBCA machine address
    resb 8 ; opaque RAM reserve; no per-object capacity claim
_finished: ; native DS CBD2 machine address
_state_cbd2: ; native DS CBD2 machine address
    resb 14 ; complete aggregate CRT-cleared RAM span
