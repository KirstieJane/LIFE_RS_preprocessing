# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 11:10:25 2015

@author: fbeyer
run:

"""

from structural import create_structural
import sys, os



subjects = ['LI00156432', 'LI01171116', 'LI01287335']


for subject in subjects:
    print 'Running subject ' + subject
    root_dir = '/data/liem-1/LIFE_redo'
    working_dir = os.path.join('/data/liem-3/LIFE_redo/struct', 'wd', subject)
    data_dir = os.path.join(root_dir, subject)
    out_dir = os.path.join(root_dir, 'preprocessed', subject, 'structural')

    freesurfer_dir = '/scr/kennedy2/LIFE/freesurfer_all/'

    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz'
    create_structural(subject=subject, working_dir=working_dir, data_dir=data_dir,
                      freesurfer_dir=freesurfer_dir, out_dir=out_dir,
                      standard_brain=standard_brain)
