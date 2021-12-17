"""
copy lab9_funcs.py into the autograded folder

interleaves a folder of files produced by 

"""
from pathlib import Path
import click
from .utils import working_directory
import shutil
import pandas as pd
from gradelib.grade_lib import (floatvec_to_string,
                                make_canvas_index, make_id, 
                                find_possible,calc_grades, merge_two, 
                                make_upload, find_closest)

#
# apply this function to gradebook dataframe
# produce a new dataframe indexed by canvasids
#
def get_canvas_id(row,track_bads):
    try:
        the_id = f"{int(row['ID']):d}"
    except ValueError:
        the_id = track_bads[-1]
        new_id = the_id - 1
        track_bads.append(new_id)
    new_row = pd.Series(row[['Student']])
    new_row['canvas_id'] = the_id
    new_row['student_num'] = int(row['SIS User ID'])
    return new_row

# export autograded=/home/jupyter/repos/nbgrader_dir/datadir/e211_files/autograded
# export funcdir=/home/jupyter/repos/nbgrader_dir/datadir/e211_files/canvas/week9_fix/funcdir
# copy_files $autograded $funcdir

@click.command()
@click.argument('autograde_folder',type=str)
@click.argument('lab9_funcs_dir',type=str)
def main(autograde_folder, lab9_funcs_dir):
    #
    # find all id folders for the autograded lab9s
    #
    class_list = Path('/home/phil/Nextcloud/eosc211_2021/tests/e211_2021_grading').glob('*2021-12-16T1827*csv')
    class_list = list(class_list)[0]
    the_list = pd.read_csv(class_list)
    the_df,possible = make_canvas_index(the_list)
    track_bads = [-999]
    name_df = the_df.apply(get_canvas_id,args = (track_bads,),axis=1)
    #
    # make a dictionary id_dict of names and ids
    #
    name_df.set_index('canvas_id',inplace=True)
    print(name_df.head())
    id_dict = name_df.to_dict(orient='index')
    #
    # make a dictionary week9_dict of autograder dirs
    #
    autograde_files = list(Path(autograde_folder).glob('**/*'))
    week9_dict = {}
    for target in autograde_files:
        if target.is_dir():
            if target.parts[-1] == 'week9_lab':
                the_id = target.parts[-2]
                if the_id not in week9_dict:
                    week9_dict[the_id] = target
    #
    # make a dicitonary file_dict of func files
    #
    func_files = list(Path(lab9_funcs_dir).glob('*'))
    file_dict={}
    for a_file in func_files:
        filename = a_file.parts[-1]
        name,the_id,filename = filename.split('-')
        file_dict[the_id] = a_file
    #
    # distribute the files into the folders
    #
    for the_id,orig_file in file_dict.items():
        dest_dir = week9_dict[the_id]
        new_file = dest_dir / 'lab9_funcs.py'
        out=shutil.copyfile(orig_file,new_file)
        print(f"{new_file=}, {out=}")
    #
    # file_list = []
    # all_files = list(Path(orig_func_dir).glob(file_regex))
    # for a_file in all_files:
    #     elements = str(a_file).split('_')
    #     if elements[1]=='LATE':
    #         late = elements.pop(1)
    #         print('found late')
    #     new_file = f"{elements[0]}-{elements[1]}-lab9_funcs.py"
    #     file_list.append({'old':str(a_file),'new':new_file})
    # new_dir = Path(new_func_dir)
    # new_dir.mkdir(parents=True,exist_ok = True)
    # for file_pair in file_list:
    #     print(file_pair)
    #     old_file = file_pair['old']
    #     new_file = new_dir / file_pair['new']
    #     print(old_file, new_file)
    #     out=shutil.copy(old_file, new_file)
    #     print(out)

