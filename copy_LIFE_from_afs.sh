#!/bin/bash

#usage: ./x0_preprocess [subListFile]
#create folder structure and copy the data from the LIFE-folder to the subject's folders

orig_dir="/afs/cbs.mpg.de/projects/life/patients"
results_dir="/nobackup/clustercache/liem/LIFE/raw_data"

subj_file="/scr/adenauer2/Franz/LIFE16/LIFE16_subjects_list_n2557.txt"


read_files()
{
while read DEM
do 

subject="${DEM}"

echo "-----------------------------------"
echo "processing $subject"
echo "-----------------------------------"

#create folders for checking and data
mkdir -p $results_dir/$subject/check
mkdir -p $results_dir/$subject/func
mkdir -p $results_dir/$subject/anat
mkdir -p $results_dir/$subject/unwarp
mkdir -p $results_dir/$subject/dMRI

#copy the first in the list of MPRAGE-images found.. (supposingly they are all the same)
first_dir=$(find $orig_dir/$subject -d -name "${subject}"*)
echo $first_dir
set -- $first_dir
echo "$1" >> $results_dir/$subject/check/images_used.txt

#copy the first in the list of anatomical images
anat_name=$(find $1 -name *_MPRAGE_ADNI_*_2.98* | sort) #only use PAT2
echo $anat_name
anat_arr=($anat_name)
nifti_tool -copy_im -prefix $results_dir/$subject/anat/MPRAGE_t1.nii -infiles ${anat_arr[0]}
echo "anatomical image: ${anat_arr[0]}" >> $results_dir/$subject/check/images_used.txt


#copy the first in the list of EPI-images found
func_name=$(find $1 -name *_t2star_epi_2D_standard_30*)
echo $func_name
func_arr=($func_name)
nifti_tool -copy_im -prefix $results_dir/$subject/func/EPI_t2.nii -infiles ${func_arr[0]}
echo "functional image: ${func_arr[0]}" >> $results_dir/$subject/check/images_used.txt

#copy the first in the list of mag-images found
mag_name=$(find $1 -name *_gre_field_mapping_5.19*)
echo $mag_name
mag_arr=($mag_name)
nifti_tool -copy_im -prefix $results_dir/$subject/unwarp/B0_mag.nii -infiles ${mag_arr[0]}
echo "magnitude image: ${mag_arr[0]}" >> $results_dir/$subject/check/images_used.txt

#copy the second in the list of ph-images found (because the first one is the other magnitude image)
ph_name=$(find $1 -name *_gre_field_mapping_7.65* | sort)
echo $ph_name
ph_arr=($ph_name)
nifti_tool -copy_im -prefix $results_dir/$subject/unwarp/B0_ph.nii -infiles ${ph_arr[1]}
echo "phase image: ${ph_arr[1]}" >> $results_dir/$subject/check/images_used.txt


#copy the first in the list of dMRI-images found
dMRI_name=$(find $1 -name *_DTI_100.nii*)
echo $dMRI_name
dMRI_arr=($dMRI_name)
nifti_tool -copy_im -prefix $results_dir/$subject/dMRI/dMRI.nii.gz -infiles ${dMRI_arr[0]}
echo "dMRI image: ${dMRI_arr[0]}" >> $results_dir/$subject/check/images_used.txt

#copy the first in the list of bvec found
dMRI_bvec_name=$(find $1 -name *_DTI_100.bvec*)
echo $dMRI_bvec_name
dMRI_bvec_arr=($dMRI_bvec_name)
cp ${dMRI_bvec_arr[0]} $results_dir/$subject/dMRI/bvecs.gz
echo "bvec image: ${dMRI_bvec_arr[0]}" >> $results_dir/$subject/check/images_used.txt

#copy the first in the list of bval found
dMRI_bval_name=$(find $1 -name *_DTI_100.bval*)
echo $dMRI_bval_name
dMRI_bval_arr=($dMRI_bval_name)
cp ${dMRI_bval_arr[0]} $results_dir/$subject/dMRI/bvals.gz
echo "bval image: ${dMRI_bval_arr[0]}" >> $results_dir/$subject/check/images_used.txt

gzip -d $results_dir/$subject/dMRI/bvecs.gz
gzip -d $results_dir/$subject/dMRI/bvals.gz

#/afs/cbs.mpg.de/projects/life/patients/LI00055374/LI00055374_20110317.VER1/NIFTI/S10_MPIL_DTI_100.bvec.gz /afs/cbs.mpg.de/projects/life/patients/LI00055374/LI00055374_20110317.VER1/NIFTI/S10_MPIL_DTI_100.bval.gz /afs/cbs.mpg.de/projects/life/patients/LI00055374/LI00055374_20110317.VER1/NIFTI/S10_MPIL_DTI_100.nii.gz


done < ${1}
}
#
read_files ${subj_file}
