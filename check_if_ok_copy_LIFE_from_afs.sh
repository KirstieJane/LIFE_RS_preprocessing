#!/bin/bash

#usage: ./x0_preprocess [subListFile]
#create folder structure and copy the data from the LIFE-folder to the subject's folders
orig_dir="/afs/cbs.mpg.de/projects/life/patients"
results_dir="/nobackup/clustercache/liem/LIFE/raw_data"

subj_file="/scr/adenauer2/Franz/LIFE16/LIFE16_subjects_list_n2557.txt"
missing_file="/scr/adenauer2/Franz/LIFE16/LIFE16_subjects_list_n2557_missing.txt"

if [ -e $missing_file ]
then
    rm $missing_file
fi

read_files()
{
echo CHECKING MISSING FILES:
echo

while read DEM
do 

subject="${DEM}"

check_files=(${results_dir}/${subject}/func/EPI_t2.nii
${results_dir}/${subject}/anat/MPRAGE_t1.nii
${results_dir}/${subject}/unwarp/B0_mag.nii
${results_dir}/${subject}/unwarp/B0_ph.nii)

missing=0
for file in ${check_files[*]}
do
    if [ ! -e $file ]
    then
        missing=1
    fi
done

if [ $missing == 1 ]
then
    echo $subject >> $missing_file
    echo remove $subject
    cmd="rm -rf $results_dir/$subject"
    echo $cmd
    #$cmd
fi

done < ${1}
}
#
read_files ${subj_file}
