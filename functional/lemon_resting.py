# -*- coding: utf-8 -*-
"""
Created on Mon Feb  9 12:26:20 2015

@author: fbeyer
"""

from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util
import nipype.interfaces.io as nio
import nipype.interfaces.fsl as fsl
from strip_rois import strip_rois_func
from moco import create_moco_pipeline
from fieldmap_coreg import create_fmap_coreg_pipeline
from transform_timeseries import create_transform_pipeline
from ants_registration import create_ants_registration_pipeline
from denoise import create_denoise_pipeline
from smoothing import create_smoothing_pipeline
from visualize import create_visualize_pipeline
from slicetiming_correction import create_slice_timing_pipeline

'''
Main workflow for lemon resting state preprocessing.
====================================================
Uses file structure set up by conversion script.
'''
def create_lemon_resting(subject, working_dir, data_dir, freesurfer_dir, out_dir,
    vol_to_remove, TR, epi_resolution, highpass, lowpass,
    echo_space, te_diff, pe_dir, standard_brain, standard_brain_resampled, standard_brain_mask, 
    standard_brain_mask_resampled, fwhm_smoothing):
    # set fsl output type to nii.gz
    fsl.FSLCommand.set_default_output_type('NIFTI_GZ')
    # main workflow
    func_preproc = Workflow(name='lemon_resting')
    func_preproc.base_dir = working_dir
    func_preproc.config['execution']['crashdump_dir'] = func_preproc.base_dir + "/crash_files"
    # select files
    templates={'func': 'func/EPI_t2.nii',
    'fmap_phase' : 'unwarp/B0_ph.nii',
    'fmap_mag' : 'unwarp/B0_mag.nii',
    'anat_head' : 'preprocessed/mod/anat/T1.nii.gz', #either with mod or without
    'anat_brain' : 'preprocessed/mod/anat/brain.nii.gz', #new version with brain_extraction from freesurfer  #T1_brain_brain.nii.gz',
    'brain_mask' : 'preprocessed/mod/anat/T1_brain_mask.nii.gz', #T1_brain_brain_mask.nii.gz',
    'ants_affine': 'preprocessed/mod/anat/transforms2mni/transform0GenericAffine.mat',
    'ants_warp':   'preprocessed/mod/anat/transforms2mni/transform1Warp.nii.gz'
    }
    
    
    selectfiles = Node(nio.SelectFiles(templates,
    base_directory=data_dir),
    name="selectfiles")
    
    
    # node to remove first volumes
    remove_vol = Node(util.Function(input_names=['in_file','t_min'],
    output_names=["out_file"],
    function=strip_rois_func),
    name='remove_vol')
    remove_vol.inputs.t_min = vol_to_remove
    # workflow for motion correction
    moco=create_moco_pipeline()
    
    # workflow for fieldmap correction and coregistration
    fmap_coreg=create_fmap_coreg_pipeline()
    fmap_coreg.inputs.inputnode.fs_subjects_dir=freesurfer_dir
    fmap_coreg.inputs.inputnode.fs_subject_id=subject
    fmap_coreg.inputs.inputnode.echo_space=echo_space
    fmap_coreg.inputs.inputnode.te_diff=te_diff
    fmap_coreg.inputs.inputnode.pe_dir=pe_dir
    
    # workflow for applying transformations to timeseries
    transform_ts = create_transform_pipeline()
    transform_ts.inputs.inputnode.resolution=epi_resolution
   
          
    # workflow to denoise timeseries
    denoise = create_denoise_pipeline()
    denoise.inputs.inputnode.highpass_sigma= 1./(2*TR*highpass)
    denoise.inputs.inputnode.lowpass_sigma= 1./(2*TR*lowpass)
    #https://www.jiscmail.ac.uk/cgi-bin/webadmin?A2=ind1205&L=FSL&P=R57592&1=FSL&9=A&I=-3&J=on&d=No+Match%3BMatch%3BMatches&z=4
    denoise.inputs.inputnode.tr = TR
    
    #workflow to transform timeseries to MNI
    ants_registration=create_ants_registration_pipeline()
    ants_registration.inputs.inputnode.ref=standard_brain_resampled    
    
    #workflow to smooth
    smoothing = create_smoothing_pipeline() 
    smoothing.inputs.inputnode.fwhm=fwhm_smoothing
   
    #workflow to slice time in the end as a try
    slicetiming = create_slice_timing_pipeline() 
    
    #visualize registration results
    visualize = create_visualize_pipeline()
    visualize.inputs.inputnode.mni_template=standard_brain_resampled 
    

    
    #sink to store files
    sink = Node(nio.DataSink(parameterization=False,
    base_directory=out_dir,
    substitutions=[('fmap_phase_fslprepared', 'fieldmap'),
    ('fieldmap_fslprepared_fieldmap_unmasked_vsm', 'shiftmap'),
    ('plot.rest_coregistered', 'outlier_plot'),
    ('filter_motion_comp_norm_compcor_art_dmotion', 'nuissance_matrix'),
    ('rest_realigned.nii.gz_abs.rms', 'rest_realigned_abs.rms'),
    ('rest_realigned.nii.gz.par','rest_realigned.par'),
    ('rest_realigned.nii.gz_rel.rms', 'rest_realigned_rel.rms'),
    ('rest_realigned.nii.gz_abs_disp', 'abs_displacement_plot'),
    ('rest_realigned.nii.gz_rel_disp', 'rel_displacment_plot'),
    ('art.rest_coregistered_outliers', 'outliers'),
    ('global_intensity.rest_coregistered', 'global_intensity'),
    ('norm.rest_coregistered', 'composite_norm'),
    ('stats.rest_coregistered', 'stats'),
    ('rest_denoised_bandpassed_norm.nii.gz', 'rest_preprocessed_nativespace.nii.gz'),
    ('rest_denoised_bandpassed_norm_trans.nii.gz', 'rest_mni_unsmoothed.nii.gz'),
    ('rest_denoised_bandpassed_norm_trans_smooth.nii', 'rest_mni_smoothed.nii')]),
    name='sink')
    
    
    # connections
    func_preproc.connect([
    #remove the first volumes    
    (selectfiles, remove_vol, [('func', 'in_file')]),

    #align volumes and motion correction
    (remove_vol, moco, [('out_file', 'inputnode.epi')]),

    #prepare field map 
    (selectfiles, fmap_coreg, [('fmap_phase', 'inputnode.phase'),
    ('fmap_mag', 'inputnode.mag'),
    ('anat_head', 'inputnode.anat_head'),
    ('anat_brain', 'inputnode.anat_brain')
    ]),
    (moco, fmap_coreg, [('outputnode.epi_mean', 'inputnode.epi_mean')]),

    #transform timeseries
    (remove_vol, transform_ts, [('out_file', 'inputnode.orig_ts')]),
    (selectfiles, transform_ts, [('anat_head', 'inputnode.anat_head')]),
    (selectfiles, transform_ts, [('brain_mask', 'inputnode.brain_mask')]),
    (moco, transform_ts, [('outputnode.mat_moco', 'inputnode.mat_moco')]),
    (fmap_coreg, transform_ts, [('outputnode.fmap_fullwarp', 'inputnode.fullwarp')]),
  
    #correct slicetiming
    (transform_ts, slicetiming, [('outputnode.trans_ts_masked', 'inputnode.ts')]),
    (slicetiming, denoise, [('outputnode.ts_slicetcorrected','inputnode.epi_coreg')]),
    
    #denoise data
    (selectfiles, denoise, [('brain_mask', 'inputnode.brain_mask'),
    ('anat_brain', 'inputnode.anat_brain')]),
    (moco, denoise, [('outputnode.par_moco', 'inputnode.moco_par')]),
    (fmap_coreg, denoise, [('outputnode.epi2anat_dat', 'inputnode.epi2anat_dat'),
    ('outputnode.unwarped_mean_epi2fmap', 'inputnode.unwarped_mean')]),
    (denoise, ants_registration, [('outputnode.normalized_file', 'inputnode.denoised_ts')]),
        
   
    #registration to MNI space
    (selectfiles, ants_registration, [('ants_affine', 'inputnode.ants_affine')] ),
    (selectfiles, ants_registration, [('ants_warp', 'inputnode.ants_warp')] ),

    (ants_registration, smoothing, [('outputnode.ants_reg_ts', 'inputnode.ts_transformed')]),

    (smoothing, visualize,  [('outputnode.ts_smoothed', 'inputnode.ts_transformed')]),


    ##all the output
    (moco, sink, [#('outputnode.epi_moco', 'realign.@realigned_ts'),
    ('outputnode.par_moco', 'realign.@par'),
    ('outputnode.rms_moco', 'realign.@rms'),
    ('outputnode.mat_moco', 'realign.MAT.@mat'),
    ('outputnode.epi_mean', 'realign.@mean'),
    ('outputnode.rotplot', 'realign.plots.@rotplot'),
    ('outputnode.transplot', 'realign.plots.@transplot'),
    ('outputnode.dispplots', 'realign.plots.@dispplots'),
    ('outputnode.tsnr_file', 'realign.@tsnr')]),
    (fmap_coreg, sink, [('outputnode.fmap','coregister.transforms2anat.@fmap'),
    #('outputnode.unwarpfield_epi2fmap', 'coregister.@unwarpfield_epi2fmap'),
    ('outputnode.unwarped_mean_epi2fmap', 'coregister.@unwarped_mean_epi2fmap'),
    ('outputnode.epi2fmap', 'coregister.@epi2fmap'),
    #('outputnode.shiftmap', 'coregister.@shiftmap'),
    ('outputnode.fmap_fullwarp', 'coregister.transforms2anat.@fmap_fullwarp'),
    ('outputnode.epi2anat', 'coregister.@epi2anat'),
    ('outputnode.epi2anat_mat', 'coregister.transforms2anat.@epi2anat_mat'),
    ('outputnode.epi2anat_dat', 'coregister.transforms2anat.@epi2anat_dat'),
    ('outputnode.epi2anat_mincost', 'coregister.@epi2anat_mincost')
    ]),
    (transform_ts, sink, [#('outputnode.trans_ts', 'coregister.@full_transform_ts'),
    ('outputnode.trans_ts_mean', 'coregister.@full_transform_mean'),
    ('outputnode.resamp_brain', 'coregister.@resamp_brain')]),
    (denoise, sink, [
    ('outputnode.wmcsf_mask', 'denoise.mask.@wmcsf_masks'),
    ('outputnode.combined_motion','denoise.artefact.@combined_motion'),
    ('outputnode.outlier_files','denoise.artefact.@outlier'),
    ('outputnode.intensity_files','denoise.artefact.@intensity'),
    ('outputnode.outlier_stats','denoise.artefact.@outlierstats'),
    ('outputnode.outlier_plots','denoise.artefact.@outlierplots'),
    ('outputnode.mc_regressor', 'denoise.regress.@mc_regressor'),
    ('outputnode.comp_regressor', 'denoise.regress.@comp_regressor'),
    ('outputnode.mc_F', 'denoise.regress.@mc_F'),
    ('outputnode.mc_pF', 'denoise.regress.@mc_pF'),
    ('outputnode.comp_F', 'denoise.regress.@comp_F'),
    ('outputnode.comp_pF', 'denoise.regress.@comp_pF'),
    ('outputnode.brain_mask_resamp', 'denoise.mask.@brain_resamp'),
    ('outputnode.brain_mask2epi', 'denoise.mask.@brain_mask2epi'),
    ('outputnode.normalized_file', 'denoise.@normalized')
    ]),
    (ants_registration, sink, [('outputnode.ants_reg_ts', 'ants.@antsnormalized')
    ]),
    (smoothing, sink, [('outputnode.ts_smoothed', '@smoothed.FWHM6')]),
    ])

    #func_preproc.write_graph(dotfilename='func_preproc.dot', graph2use='colored', format='pdf', simple_form=True)
    func_preproc.run(plugin='CondorDAGMan')
    # plugin='MultiProc'plugin='MultiProc'plugin='CondorDAGMan')plugin='CondorDAGMan'
    #func_preproc.run()plugin='CondorDAGMan'plugin='CondorDAGMan'plugin='CondorDAGMan'
#plugin='CondorDAGMan'