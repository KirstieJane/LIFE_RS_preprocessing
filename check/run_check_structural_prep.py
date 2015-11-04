
from utils import check_if_wf_is_ok
import os, glob



wd_path = '/scr/kennedy2/liem/sample_5/wd'
wf = 'anat_preproc'
batch_path_template = os.path.join(wd_path, '{subject_id}', wf, 'batch')
crash_path_template = os.path.join(wd_path, '{subject_id}', wf, 'crash_files')
check_file_list = ['/scr/kennedy2/liem/sample_5/subjects/{subject_id}/preprocessed/mod/anat/transforms2mni/transform1Warp.nii.gz']

os.chdir(wd_path)
subjects_list = glob.glob('LI*')

everything_ok = check_if_wf_is_ok(batch_path_template, crash_path_template, subjects_list)


missing_files = False
for subject_id in subjects_list:
    for file_template in check_file_list:
        subject_file = file_template.format(subject_id)
        if not os.path.exists(subject_file):
            print('%s MISSING FILE'%subject_id)
            missing_files = True

if missing_files:
    print('\n FILES MISSING')
else:
    print('\n ALL OK: files are there')
