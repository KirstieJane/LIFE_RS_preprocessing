from utils import check_if_wf_is_ok
import os, glob





# wd_path = '/scr/kansas1/liem/sample_5/wd'
# wd_path = '/nobackup/clustercache/liem/sample_5/wd'
# wf = 'lemon_resting'

root_dir = '/scr/kennedy2/liem/sample_5/subjects/'

check_file_list = ['{subject_id}/preprocessed/mod/resting/ants/rest_mni_unsmoothed_fullspectrum.nii.gz',
                   '{subject_id}/preprocessed/mod/resting/ants/rest_mni_unsmoothed.nii.gz',
                   '{subject_id}/preprocessed/mod/resting/denoise/rest_preprocessed_nativespace_fullspectrum.nii.gz',
                   '{subject_id}/preprocessed/mod/resting/denoise/rest_preprocessed_nativespace.nii.gz',
                   '{subject_id}/preprocessed/mod/resting/FWHM6/rest_mni_smoothed.nii',
                   '{subject_id}/preprocessed/mod/resting/realign/rest_realigned.par',
                   '{subject_id}/preprocessed/mod/anat/transforms2mni/transform0GenericAffine.mat',
                   '{subject_id}/preprocessed/mod/anat/transforms2mni/transform1InverseWarp.nii.gz',
                   '{subject_id}/preprocessed/mod/anat/transforms2mni/transform1Warp.nii.gz',
                   ]

with open('/home/raid2/liem/Dropbox/LeiCa/LIFE/subjects_lists/subjects_big_sample5_2_preprocessing_ok_n1181.txt', 'r') as f:
    subjects_list = [line.strip() for line in f]

print('\n\n CHECKING FOR MISSING FILES...')
missing_files = False
for subject_id in subjects_list:
    for file_template in check_file_list:
        subject_file = os.path.join(root_dir, file_template.format(subject_id=subject_id))

        if not os.path.exists(subject_file):
            print('MISSING FILE %s: %s' % (subject_id, subject_file))
            missing_files = True

if missing_files:
    print('\n SOME FILES MISSING')
else:
    print('\n ALL OK: files are there (%s subjects)'%len(subjects_list))
