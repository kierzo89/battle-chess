"""Finite mixed policy dispatcher: only two separately closed source profiles.

No profile/native/output file reads in generator callbacks; imported closed
modules are selected by exact row profile or exact sealed transform identity.
"""
import mixed_refresh_chat_pipeline16 as old
import mixed_restore_decoder_pipeline16 as new
KIND=old.KIND
PROFILES={'refresh_chat284_v1':old,'restore_decoder340_v1':new}
TRANSFORMS={old.TRANSFORM:old,new.TRANSFORM:new}
def need(v,m):
 if not v:raise ValueError('Finite mixed dispatcher: '+m)
def module_for_row(r):
 need(r.get('kind')==KIND and r.get('object_profile')in PROFILES,'one exact closed mixed profile');return PROFILES[r['object_profile']]
def module_for_seal(r):
 need(r.get('kind')==KIND and r.get('mixed_transform')in TRANSFORMS,'one exact closed mixed sealed transform');return TRANSFORMS[r['mixed_transform']]
def validate_row(r):return module_for_row(r).validate_row(r)
def validate_sources(r,project):return module_for_row(r).validate_sources(r,project)
def record_read(observer,p,raw):return module_for_row(observer.current[0]).record_read(observer,p,raw)
def before_process(observer,row,event,root,argv,kw):return module_for_row(row).before_process(observer,row,event,root,argv,kw)
def finish_event(observer,row,event,result):return module_for_row(row).finish_event(observer,row,event,result)
def validate_selected(spec,selected,components,project):return module_for_row(spec).validate_selected(spec,selected,components,project)
def seal_extra(spec,selected):
 if spec['kind']!=KIND:return{}
 return module_for_row(spec).seal_extra(spec,selected)
def validate_seal_row(r):
 if r['kind']!=KIND:return True
 return module_for_seal(r).validate_seal_row(r)
