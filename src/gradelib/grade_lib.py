import pandas as pd
import click
import json
import pathlib
from pathlib import Path
import numpy as np
from fuzzywuzzy import fuzz
import pdb
import pandas as pd


def make_upload(df_canvas):
    """
    make a upload frame with a sort_order column
    """
    can_grade_cols = list(df_canvas.columns.to_list())
    can_mandatory_columns = list(can_grade_cols[:5])
    df_upload = pd.DataFrame(df_canvas[can_mandatory_columns], copy=True)
    #
    # preserve sort order with this column
    #
    can_col = np.linspace(
          -1, len(df_upload), num=len(df_upload), dtype=np.int, endpoint=False
    ).astype(np.int)
    df_upload["sort_order"] = can_col
    return df_upload


def add_possible(df_upload,possible_row,col_name,possible_points):
    possible_row[1:5] = " "
    colnames = list(df_upload.columns[:5])
    colnames.append(col_name)
    possible_row = possible_row[:5].append(pd.Series([possible_points]))
    the_rows = [dict(zip(colnames,possible_row.values))]
    points_possible=pd.DataFrame.from_records(the_rows)
    points_possible.index = ['-1']
    df3=pd.concat([points_possible,df_upload])
    return df3

def find_student(name_string,grade_df,name_col='Student'):
    """
    find the student id for a name guess

    Parameters
    ----------

    name_string: str -- "lastname, firstname"
    grade_df: DataFrame -- gradebook dataframe indexed by student number
    name_col: str -- name of column to use for first,last

    Returns
    -------

    prints name and id
    """
    good_names = grade_df[name_col]
    the_name, score = find_closest(name_string,good_names)
    print(f"found {the_name}")
    hit = good_names == the_name
    result = grade_df.loc[hit]
    print(result)
    if isinstance(result,pd.Series):
        the_id = result.name
    else:
        the_id = result.index[0]
    return the_id

def make_id(df,idcol):
    """
    Parameters
    ----------
    df: either string filename of csv file or pandas dataframe
    idcol: str 
       name of column to make id
    usage: the_df = make_id(the_df,'SIS User ID')
    """
    if isinstance(df,str):
        with open(df,'r') as infile:
            df = pd.read_csv(df)
    else:
        df = pd.DataFrame(df,copy=True)
    keep_bad = [-999]
    def convert_col(row,keep_bad):
        the_id = row[idcol]
        try:
            #
            # '63514095.0'
            #
            the_int = int(float(the_id))
            str_id = f"{int(the_int):d}"
        except Exception as e:
            print(f"id conversion problem in make_id: {e}")
            print(f"{the_id=}")
            bad_val = keep_bad[-1]
            str_id = f"{int(bad_val):d}"
            bad_val+= -1
            keep_bad.append(bad_val)
        row["the_ids"] = str_id
        return row
    
    df = df.apply(convert_col,args=(keep_bad,),axis=1)
    bad_num = len(keep_bad) - 1
    if bad_num > 0:
        print(f"found {bad_num} bad ids: replaced with {keep_bad[:-1]}")
    df.set_index("the_ids", inplace=True, drop=False)
    return df

def find_possible(df_canvas):
    possible_row = df_canvas.loc[
        df_canvas["Student"].str.find("Points Possible") > -1]
    possible_row = possible_row.iloc[0,:]
    return possible_row

def make_canvas_index(df_canvas,idcol='SIS User ID'):
    """
    produce a datafame with nans set to 0 for all columns
    bigger than start_col -- i.e. convert scores but not ids
    """
    df_canvas = pd.DataFrame(make_id(df_canvas,idcol),copy=True)
    possible_row = find_possible(df_canvas)
    #print(f"\nfound points possible row:\n {possible_row}\n\n")
    #
    # drop negative integer non-id rows and cast all
    # columns to the right of Lab or column 7 to float
    #
    hit = [item[0] == '-' for item in df_canvas.index]
    df_canvas.drop(df_canvas.index[hit], inplace=True)
    has_lab=False
    for col_num, col_name in enumerate(df_canvas.columns):
        if col_name == 'Lab':
            has_lab=True
            break
    if has_lab:
        start_col = col_num +1
    else:
        start_col = 7
    type_dict = {key: np.float for key in df_canvas.columns.values[start_col:]}
    new_canvas_df = df_canvas.astype(dtype=type_dict)
    new_canvas_df.fillna(0., inplace=True)
    return new_canvas_df, possible_row

def record_from_name(the_name,the_df,name_col='Student'):
    record_name, record_num =find_closest(the_name,the_df[name_col])
    return the_df.iloc[record_num]
    
    


def find_closest(the_string, good_strings,threshold=None):
    """
    search through a list of strings and return the
    members of good_strings that are closest to the_string

    Parameters
    ----------

    the_string: string
      stirng to test

    good_strings: list of strings
      the gradebook strings to test against

    threshold: float
      if None, then return best match, otherwise
      return all matchews that score higher than a threshold

    Returns
    -------

    good_choice,max_index: string, int
       best fit string
    """
    score_list = []
    for choice in good_strings:
        score_list.append(fuzz.ratio(the_string, choice))
    score_array = np.array(score_list)
    max_index = np.argmax(score_array)
    good_choice = good_strings[max_index]
    return good_choice, max_index

def make_group_index(df_group):
    group_ids = [
        "STUDENT ID #1",
        "STUDENT ID #2",
        "STUDENT ID #3",
        "STUDENT ID #4",
        "Percent Score",
    ]
    group_scores = df_group[group_ids].to_numpy()
    nrows, ncols = group_scores.shape
    group_id_list = []
    group_list = []
    for i in range(nrows):
        row_ids = group_scores[i, :4]
        the_score = group_scores[i, 4]
        row_list = []
        for item in row_ids:
            try:
                the_id = str(int(item))
            except:
                print((f"trouble reading df_group\n"
                       f"sudent number {item} set to '-999'"))
                the_id = str(-999)
            group_id_list.append(the_id)
            row_list.append({"id": the_id, "Percent Score": the_score})
        group_list.append(row_list)
    group_scores = []
    for a_row in group_list:
        group_scores.extend(a_row)
    df_group = pd.DataFrame.from_records(group_scores)
    df_group.set_index("id", inplace=True, drop=True)
    return df_group

def calc_grades(ax,scores,nbins=10):
    """
    returns ax, the_median,the_mean
    """
    the_median=np.nanmedian(scores)
    the_mean=np.nanmean(scores)
    ax.hist(scores,nbins)
    return ax,the_median, the_mean

def make_ind_index(df_ind):
    ind_id_list = []
    ind_list = []
    ind_scores = df_ind[["STUDENT ID", "Percent Score"]].to_numpy()
    nrows, ncols = ind_scores.shape
    for i in range(nrows):
        the_id = str(int(ind_scores[i, 0]))
        the_score = ind_scores[i, 1]
        ind_id_list.append(the_id)
        ind_list.append({"id": the_id, "ind_score": the_score})
    df_ind = pd.DataFrame.from_records(ind_list)
    df_ind.set_index("id", inplace=True, drop=True)
    return df_ind


def merge_two(df_left, df_right,suffixes=('_x', '_y')):
    df_return = pd.merge(df_left,
                         df_right,
                         how="left",
                         left_index=True,
                         right_index=True,
                         sort=False,
                         suffixes=suffixes)
    return pd.DataFrame(df_return, copy=True)


def mark_combined(row):
    try:
        group = row["group_score"]
        if group < row["ind_score"]:
            group = row["ind_score"]
        mark = 0.85 * row["ind_score"] + 0.15 * group
    except NameError:
        print(f"trouble: {row}")
    return mark


def check_ids(df, good_ids):
    print(f"checking ids")
    for the_id in df.index.to_numpy():
        nearest_id = find_closest(the_id, good_ids)
        if nearest_id != the_id:
            print(f"miss bad id -- {the_id},closest id -- {nearest_id}")


@click.group()
def main():
    """
    set of tools for figure resizing
    """
    pass


def read_raw_dfs(filenames):
    name_dict = json.load(filenames)
    gradebook_re = name_dict['files']['gradebook']
    gradebook = list(Path().glob(gradebook_re))[0]
    df_canvas = pd.read_csv(gradebook)
    name_dict['files']['gradebook'] = gradebook
    ind_re = name_dict['files']['remark_ind']
    ind_file = list(Path().glob(ind_re))[0]
    name_dict['files']['ind_file'] = ind_file
    df_ind = pd.read_excel(ind_file)
    group_re = name_dict['files']['remark_group']
    group_file = list(Path().glob(group_re))[0]
    df_group = pd.read_excel(group_file)
    name_dict['files']['group_file'] = group_file
    return df_canvas, df_ind, df_group, name_dict

#
# apply this function to gradebook dataframe
# produce a new dataframe indexed by canvasids
#
def get_canvas_id(row,track_bads):
    try:
        the_id = f"{int(row['ID']):d}"
    except ValueError:
        the_id = int(track_bads[-1])
        new_id = the_id - 1
        the_id = f"{int(new_id):d}"
        track_bads.append(new_id)
    new_row = pd.Series(row[['Student']])
    new_row['canvas_id'] = the_id
    new_row['student_num'] = str(int(row['SIS User ID']))
    return new_row


def make_namedict(canvas_file):
    """
    turn a canvas file into dictionary with canvas id as key
    """
    if isinstance(canvas_file,str) or isinstance(canvas_file,pathlib.PurePath):
        the_list = pd.read_csv(canvas_file)
        the_df,possible = make_canvas_index(the_list)
    else:
        the_df = canvas_file
        the_df,possible = make_canvas_index(the_df)
    track_bads = [-999]
    name_df = the_df.apply(get_canvas_id,args = (track_bads,),axis=1)
    #
    # make a dictionary id_dict of names and ids
    #
    name_df.set_index('canvas_id',inplace=True)
    print('debug: ',name_df.head())
    id_dict = name_df.to_dict(orient='index')
    return id_dict



@main.command()
@click.argument("filenames", type=click.File("r"), nargs=1)
def check_columns(filenames):
    df_canvas, df_ind, df_group, name_dict = read_raw_dfs(filenames)
    print(
        f"reading {name_dict['files']['gradebook']} head is:\n{df_canvas.head()}"
    )
    print(f"sample row: {df_canvas.loc[5]}")
    print(f"{df_ind.head()=}")
    print(
        f"reading {name_dict['files']['ind_file']} head is:\n{df_ind.head()}")
    print(f"sample row: {df_ind.loc[5]}")
    print(
        f"reading {name_dict['files']['group_file']} head is: \n{df_group.head()}"
    )
    print(f"sample row: {df_group.loc[5]}")


@main.command()
@click.argument("filenames", type=click.File("r"), nargs=1)
def make_grades(filenames):
    """
    Given the name of a json file with the following format:

    \b
    {
        "history": "2019t1",
        "files": {
            "gradebook": "*EOSC_340_101.csv",
            "remark_ind": "*Q3*Grades.xlsx",
            "remark_group": "*Q3*Group.xlsx"
        }
    }

    calculate the quiz grade

    Example: python grade_quizzes.py filenames.json

    """
    df_canvas, df_ind, df_group, name_dict = read_raw_dfs(filenames)
    new_canvas_df, possible_row = make_canvas_index(df_canvas)
    new_df_group = make_group_index(df_group)
    new_df_ind = make_ind_index(df_ind)
    print(
        f"reading {name_dict['files']['gradebook']} head is:\n{df_canvas.head()}"
    )
    print(f"sample row: {df_canvas.iloc[5]}")
    print(
        f"reading new_df_ind head is:\n{new_df_ind.head()}")
    print(f"sample row: {new_df_ind.iloc[5]}")
    print(
        f"reading new_df_group head is: \n{new_df_group.head()}"
    )
    print(f"sample row: {new_df_group.iloc[5]}")
    student_ids = df_canvas.index.to_list()
    int_ids = [int(item) for item in student_ids]
    df_canvas['int_ids'] = int_ids
    print("checking individual remark")
    check_ids(new_df_ind, student_ids)
    print("checking group remark")
    check_ids(new_df_group, student_ids)

    df_out = merge_two(new_df_ind, new_df_group)

    total_score = df_out.apply(mark_combined, axis=1)
    df_out["total_score"] = total_score

    # #
    # # save points possible then drop it
    # #
    can_grade_cols = list(df_canvas.columns.to_list())
    can_mandatory_columns = list(can_grade_cols[:5])
    df_upload = pd.DataFrame(df_canvas[can_mandatory_columns], copy=True)
    #
    # preserve order with this column
    #
    can_col = np.linspace(
          -1, len(df_upload), num=len(df_upload), dtype=np.int, endpoint=False
    ).astype(np.int)
    df_upload["sort_order"] = can_col
    df_doit = merge_two(df_upload, df_out)
    df_doit.sort_values("sort_order", ascending=True, inplace=True)
    keep_columns = [
        "Student",
        "ID",
        "SIS User ID",
        "SIS Login ID",
        "Section",
        "ind_score",
        "group_score",
        "total_score",
    ]

    df_doit = df_doit[keep_columns]
    points_possible = possible_row.iloc[0, :5]
    points_possible[1:5] = " "
    extent = pd.Series(
        [100, 100, 100], index=["ind_score", "group_score", "total_score"]
    )
    points_possible = points_possible.append(extent)
    the_rows = [dict(zip(points_possible.index,points_possible.values))]
    points_possible=pd.DataFrame.from_records(the_rows)
    points_possible.index = ['-1']
    df2=pd.concat([points_possible,df_doit])
    columns=name_dict['columns']
    outfile = name_dict['outfile']
    df2.rename(
        columns=columns,
        inplace=True,
    )
    df2.to_csv(outfile, index=False)
    with open('dump.json','w') as outfile:
        json.dump(columns, outfile,indent=4)

def normal(gradevec,the_mean,sigma):
    factor = 1./(sigma*np.sqrt(2*np.pi))
    arg = -0.5*(((gradevec - the_mean)/sigma)**2.)
    the_exp = np.exp(arg)
    return factor*the_exp

def assign_bin(bincounts,bincenters):
    """
    
    """
    totalcounts = np.sum(bincounts)
    print(f"assign_bin: total capacity is {totalcounts}")
    students = np.arange(0,totalcounts,1)
    current_bin = len(bincenters) - 1
    capacity = bincounts[current_bin]
    bincounter= int(0)
    #print(f"starting at bin {current_bin} with capacity {capacity}")
    student_vec = []
    for the_student in students:
        #print(f"working on bin {current_bin} with capacity {capacity}")
        if bincounter < capacity:
            grade = bincenters[current_bin]
            student_vec.append((the_student,grade))
            bincounter+=1
        else:
            current_bin -= 1
            #print(f"dropping down 1 bin to {current_bin}")
            capacity = bincounts[current_bin]
            bincounter=0
            #print(f"new bin {current_bin} capacity is {capacity}")
            grade = bincenters[current_bin]
            student_vec.append((int(the_student),grade))
            bincounter+=1
        #print(f"final assignment: {the_student,current_bin}")
        #print(f"remaining room: {np.sum(bincounts[:current_bin])}")
        #print(f"capacity used: {np.sum(bincounts[current_bin:])}")
        #print(f"students assigned {the_student}")
        bin_dict = {item[0]:item[1] for item in student_vec}
    return bin_dict

def create_dist(amp,clip= -5):
    """
    amp = approx class size
    mean of 70 sd of 10
    """
    zscore = np.linspace(50,100,30)
    sigma = 10
    the_mean = 70
    binwidth = np.diff(zscore)[0]
    bincenters = (zscore[:-1] + zscore[1:])/2.
    binheight = normal(bincenters,the_mean,sigma)
    total_area = np.sum(binwidth*binheight)*amp
    bincounts=np.round(binwidth*binheight*amp).astype(int)
    bincounts = bincounts[:clip]
    print(f"create_dist: total capacity is {np.sum(bincounts)}")
    bincenters = bincenters[:clip]
    bin_dict=assign_bin(bincounts,bincenters)
    return bin_dict

def apply_boost(row, bin_dict,grade_col):
    """
    bin_dict = ideal distribution dictionary from create_dist
    grade_col = 
    """
    boost_grade = bin_dict[int(row['rank'])]
    old_grade = float(row[grade_col])
    new_grade = boost_grade
    if old_grade > boost_grade:
        new_grade=old_grade
    if old_grade < 1:
        new_grade = old_grade
    row['new_grade'] = new_grade
    return row
        
if __name__ == "__main__":
    main()
