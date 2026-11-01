; Real initialized hardware state, each label has independent native consumers.
_DATA SEGMENT WORD PUBLIC 'DATA'
_DATA ENDS
DGROUP GROUP _DATA
ASSUME DS:DGROUP
_DATA SEGMENT WORD PUBLIC 'DATA'
PUBLIC _audio_calibration_ticks_2eae, _saved_timer_vector_2eaf, _speed_2eb3
PUBLIC _saved_critical_vector_2eb5, _saved_pic_mask_2eb9
_audio_calibration_ticks_2eae DB 0
_saved_timer_vector_2eaf DD 0
_speed_2eb3 DW 0
_saved_critical_vector_2eb5 DD 0
_saved_pic_mask_2eb9 DB 0
_DATA ENDS
END
