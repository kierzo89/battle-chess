"""Twenty exact new mixed-group BSS F2 clients; no frame normalization."""
import hashlib
CONTRACTS={'db232231fe3e9ba1ce80e672cc19b4841d0f0818f49fab820aaf5013559c2648': {'source': 'src/attacks_neighbors_match.c',
                                                                      'source_sha256': 'c8904a4b293bcd91e322cb5c23946f2e8fdb172fb66cfa606b9d7fb96a1c11dd',
                                                                      'owners': ['init_rays_code185',
                                                                                 'piece_attacks_98f9',
                                                                                 'pawn_attacks_99be'],
                                                                      'allowed': {258: ('_rays', 7, None, 'c502260707'),
                                                                                  417: ('_board', 1, None, 'c5a1260101')}},
 'f7ac7b7bd97f4aa326cf13053ad06339176b04761ff6a1d40ef583b9279deb29': {'source': 'src/display_queue_neighbors_match.c',
                                                                      'source_sha256': 'e1d6a7e8c1d4e19dfb68c966f1094547c26e065261c491157c8571fc5fceae37',
                                                                      'owners': ['animate_move_code363',
                                                                                 'redraw_piece_7a61',
                                                                                 'queue_piece_7aa7',
                                                                                 'reset_display_7b86',
                                                                                 'select_display_7ba4',
                                                                                 'init_display_7bc2',
                                                                                 'trim_history_7bf9'],
                                                                      'allowed': {607: ('_frame_index', 5, None, 'c65f260505'),
                                                                                  616: ('_frames', 8, None, 'c668260808'),
                                                                                  629: ('_screen_y', 28, None, 'c675261c1c'),
                                                                                  640: ('_screen_x', 26, None, 'c680261a1a'),
                                                                                  664: ('_saved_state', 6, None, 'c698260606'),
                                                                                  681: ('_ready_9856', 30, None, 'c6a9261e1e'),
                                                                                  687: ('_state_57cc', 33, None, 'c6af262121'),
                                                                                  727: ('_mode_8176', 21, None, 'c6d7261515'),
                                                                                  780: ('_history_index', 19, None, 'c70c261313'),
                                                                                  792: ('_history_index', 19, None, 'c718261313'),
                                                                                  828: ('_history_index', 19, None, 'c73c261313'),
                                                                                  833: ('_saved', 3, None, 'c741260303'),
                                                                                  845: ('_history_tail', 15, None, 'c74d260f0f')}}}
def validate_client_frame(row,raw,f,symbol):
 h=hashlib.sha256(raw).hexdigest();assert h in CONTRACTS,'exact reviewed whole mixed object';c=CONTRACTS[h]
 assert row['kind']=='mixed-c-fa-authored-asm-whole-omf' and row['source']==c['source'] and row['source_sha256']==c['source_sha256'] and row['selected_owners']==c['owners'],'exact source/owner context'
 assert f.offset in c['allowed'] and (symbol,f.target[1],f.displacement,f.raw.hex())==c['allowed'][f.offset],'exact native BSS raw field'
 assert f.frame==(2,f.target[1]) and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative is True,'actual raw external frame required'
 return 'proven_MIXED_VISUAL_external_PUBLIC_group1'
