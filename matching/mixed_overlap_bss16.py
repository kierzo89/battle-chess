"""Twenty exact new mixed-group BSS F2 clients; no frame normalization."""
import hashlib
CONTRACTS={'04fc9a5d5ed9624011c21ca811bb0fe7f4c29fb69061ad6606fe7018f51942e1': {'source': 'src/input_mixed_context_match.c',
                                                                      'source_sha256': '9cfe972686121e02c8fce86ab10054c5cd45073e2cae4cef7b85974a5fa94d94',
                                                                      'owners': ['fill_region_1780',
                                                                                 'select_mode_code84',
                                                                                 'next_event_184d',
                                                                                 'handle_input_1917',
                                                                                 'input_control_1c77'],
                                                                      'allowed': {266: ('_current_ticks_9884', 7, None, 'c50a260707'),
                                                                                  270: ('_current_ticks_9884', 7, 2, 'c50e2207070200'),
                                                                                  347: ('_current_ticks_9884', 7, None, 'c55b260707'),
                                                                                  351: ('_current_ticks_9884', 7, 2, 'c55f2207070200'),
                                                                                  355: ('_last_event_ticks_b07a', 30, None, 'c563261e1e'),
                                                                                  359: ('_last_event_ticks_b07a', 30, 2, 'c567221e1e0200'),
                                                                                  376: ('_current_ticks_9884', 7, None, 'c578260707'),
                                                                                  380: ('_current_ticks_9884', 7, 2, 'c57c2207070200'),
                                                                                  383: ('_last_event_ticks_b07a', 30, None, 'c57f261e1e'),
                                                                                  387: ('_last_event_ticks_b07a', 30, 2, 'c583221e1e0200'),
                                                                                  434: ('_paused', 8, None, 'c5b2260808'),
                                                                                  744: ('_pointer_x', 32, None, 'c6e8262020'),
                                                                                  754: ('_pointer_y', 33, None, 'c6f2262121'),
                                                                                  931: ('_menus', 4, None, 'c7a3260404')}},
 '909220367ff0a3197db9192a40e5ce78933cb0d95ec2843f5c9bd0dce9854ecc': {'source': 'src/motion_mixed_context_match.c',
                                                                      'source_sha256': 'a85d408380757b940d0fd2b2f7d5c6fba1b69ffea867b3f349b91b9fe9d70ed9',
                                                                      'owners': ['init_animation_code1083',
                                                                                 'offset_task_70ef',
                                                                                 'face_task_724d',
                                                                                 'turn_task_code640'],
                                                                      'allowed': {1231: ('_frames', 6, None, 'c4d3260606'),
                                                                                  1279: ('_motion_y', 23, None, 'c503261717'),
                                                                                  1283: ('_motion_x', 22, None, 'c507261616'),
                                                                                  1376: ('_motion_y', 23, None, 'c564261717'),
                                                                                  1380: ('_motion_x', 22, None, 'c568261616'),
                                                                                  1502: ('_frames', 6, None, 'c5e2260606')}}}
def validate_client_frame(row,raw,f,symbol):
 h=hashlib.sha256(raw).hexdigest();assert h in CONTRACTS,'exact reviewed whole mixed object';c=CONTRACTS[h]
 assert row['kind']=='mixed-c-fa-authored-asm-whole-omf' and row['source']==c['source'] and row['source_sha256']==c['source_sha256'] and row['selected_owners']==c['owners'],'exact source/owner context'
 assert f.offset in c['allowed'] and (symbol,f.target[1],f.displacement,f.raw.hex())==c['allowed'][f.offset],'exact native BSS raw field'
 assert f.frame==(2,f.target[1]) and f.target[0]==2 and f.segment==1 and f.width==2 and f.location_type==1 and f.segment_relative is True,'actual raw external frame required'
 return 'proven_MIXED_OVERLAP_external_PUBLIC_group1'
