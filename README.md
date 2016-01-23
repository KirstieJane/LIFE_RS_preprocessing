# LIFE_Lemon_mod_mod



# Results

├── resting_state
│   ├── ants
│   │   ├── rest_mni_unsmoothed_fullspectrum.nii.gz
│   │   └── rest_mni_unsmoothed.nii.gz
│   ├── coregister
│   │   ├── rest2anat.dat.mincost
│   │   ├── rest_coregistered_nativespace.nii.gz
│   │   ├── rest_mean2anat_highres.nii.gz
│   │   ├── rest_mean2anat_lowres.nii.gz
│   │   ├── rest_mean2fmap.nii.gz
│   │   ├── rest_mean2fmap_unwarped.nii.gz
│   │   ├── T1_resampled.nii.gz
│   │   └── transforms2anat                             
│   │       ├── B0_ph_fslprepared.nii.gz            
│   │       ├── fullwarpfield.nii.gz
│   │       ├── rest2anat.dat
│   │       └── rest2anat.mat
│   ├── denoise
│   │   ├── artefact
│   │   │   ├── art.rest2anat_masked_outliers.txt
│   │   │   ├── global_intensity.rest2anat_masked.txt
│   │   │   ├── norm.rest2anat_masked.txt
│   │   │   ├── plot.rest2anat_masked.png
│   │   │   └── stats.rest2anat_masked.txt
│   │   ├── mask
│   │   │   ├── T1_brain_mask2epi.nii.gz
│   │   │   ├── T1_brain_mask_lowres.nii.gz
│   │   │   └── wmcsf_mask_lowres.nii.gz
│   │   ├── regress
│   │   │   ├── F_mcart.nii.gz
│   │   │   ├── F_noise.nii.gz
│   │   │   ├── mcart_regressor.txt
│   │   │   ├── noise_regressor.txt
│   │   │   ├── pF_mcart.nii.gz
│   │   │   └── pF_noise.nii.gz
│   │   ├── rest_preprocessed_nativespace_fullspectrum.nii.gz
│   │   └── rest_preprocessed_nativespace.nii.gz
│   ├── FWHM6
│   │   └── rest_mni_smoothed.nii
│   └── realign
│       ├── MAT                             realignment matrices for all volumes
│       │   ├── MAT_0000
│       │   ....
│       │   └── MAT_0294
│       ├── plots                           plots of estimated motion
│       │   ├── abs_displacement_plot.png
│       │   ├── rel_displacment_plot.png
│       │   ├── rotation_plot.png
│       │   └── translation_plot.png
│       ├── rest_realigned_abs.rms          absolute and relative rms displacement (similar to mean frame displacement)
│       ├── rest_realigned_mean.nii.gz      temporal mean after realignment
│       ├── rest_realigned.par              realignment parameters
│       ├── rest_realigned_rel.rms          absolute and relative rms displacement (similar to mean frame displacement)
│       └── rest_realigned_tsnr.nii.gz      temporal snr after realignment
└── structural
    ├── brain.nii.gz                        skull stripped
    ├── T1_brain2mni.nii.gz                 brain in MNI152 1mm space
    ├── T1_brain_mask.nii.gz                brain mask
    ├── T1.nii.gz                           whole head after background masking in freesurfer space
    └── transforms2mni                      transforms anatomy to MNI space (use antsApplyTransfom)
        ├── transform0GenericAffine.mat
        ├── transform1InverseWarp.nii.gz    inverse of nonlinear transformation
        └── transform1Warp.nii.gz

