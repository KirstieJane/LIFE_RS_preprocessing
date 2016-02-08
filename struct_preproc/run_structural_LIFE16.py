# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:10:25 2015

@author: fbeyer
run:
python struct_preproc/run_structural_LIFE16.py f /scr/adenauer2/Franz/LIFE16/LIFE16_subjects_list_n2557.txt

"""

from structural import create_structural
import sys, os

'''
Meta script to run structural preprocessing
------------------------------------------
Can run in two modes:
python run_structural.py s {subject_id}
python run_structural.py f {text file containing list of subjects}
'''
mode = sys.argv[1]

if mode == 's':
    subjects = [sys.argv[2]]
    print subjects
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

# select fold
# subjects = subjects[:1300]
#subjects = subjects[1300:]


for subject in subjects:
    print 'Running subject ' + subject
    root_dir = '/data/liem-1/LIFE'
    #root_dir_2 = '/data/liem-2/LIFE'
    root_dir_2 = '/scr/adenauer2/Franz/LIFE_WD'
    working_dir = os.path.join(root_dir_2, 'wd', subject)
    data_dir = os.path.join(root_dir, subject)
    out_dir = os.path.join(root_dir, 'preprocessed', subject, 'structural')

    freesurfer_dir = '/scr/kennedy2/LIFE/freesurfer_all/'

    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    create_structural(subject=subject, working_dir=working_dir, data_dir=data_dir,
                      freesurfer_dir=freesurfer_dir, out_dir=out_dir,
                      standard_brain=standard_brain)
