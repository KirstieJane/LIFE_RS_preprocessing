
def get_condor_exit_status(batch_dir):
    import yaml
    import glob
    import os

    log_file = glob.glob(os.path.join(batch_dir, 'workflow*.dag.metrics'))[-1]
    f = open(log_file)
    d = yaml.load(f)
    f.close()

    return(d['exitcode'], d['jobs_failed']) # int 0:ok; >0:not ok

def check_if_wf_crashed(crash_dir):
    import os
    wf_crashed = False
    if os.path.exists(crash_dir):
        if os.listdir(crash_dir):
            wf_crashed = True
    return wf_crashed


def check_if_wf_is_ok(batch_path_template, crash_path_template, subjects_list):
    import pandas as pd

    df = pd.DataFrame(columns=['exitcode', 'jobs_failed', 'crashed'])

    for subject_id in subjects_list:
        print(subject_id)
        batch_path = batch_path_template.format(subject_id=subject_id)
        crash_path = crash_path_template.format(subject_id=subject_id)

        exit_status = get_condor_exit_status(batch_path)
        crash_status = check_if_wf_crashed(crash_path)
        df.loc[subject_id] = [exit_status[0], exit_status[1], crash_status]

    df_crashed = df[(df['exitcode'] > 0) | (df['crashed'] == True)]
    if len(df_crashed) > 0:
        print df_crashed
        everything_ok = False
    else:
        print('nothing crashed. %s subjects ok'%len(df))
        everything_ok = True
    return everything_ok

