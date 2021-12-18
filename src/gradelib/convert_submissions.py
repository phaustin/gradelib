"""
convert a canvas sumissions zip into a folder of web pages

export canvas_file=/home/phil/Nextcloud/eosc211_2021/tests/e211_2021_grading/2021-12-16T1827_Grades-EOSC_211_101_2021W1.csv

export zipfile=/home/jupyter/repos/nbgrader_dir/datadir/e211_files/canvas/week2_extracted.zip

convert_submissions $canvas_file $zipfile .

e.g.:
build_html autograded "lab_wk9*ipynb"
"""

from pathlib import Path
import click
import shutil
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
from zipfile import ZipFile
import pandas as pd
from .grade_lib import make_canvas_index
from .utils import working_directory

def make_page(notebook_file,html_file):
    with open(notebook_file,'r') as in_file:
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'classic'
        (body, resources) = html_exporter.from_file(in_file)
    with open(html_file,'w') as out_file:
        out_file.write(body)

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

def unzip(zipfile, the_dir):
    """
    unzip zipfile into the_dir
    """
    with working_directory(the_dir):
        with ZipFile(zipfile, "r") as in_zip:
            in_zip.extractall()
    return None

def make_namedict(canvas_file):
    """
    turn a canvas file into dictionary with canvas id as key
    """
    the_list = pd.read_csv(canvas_file)
    the_df,possible = make_canvas_index(the_list)
    track_bads = [-999]
    name_df = the_df.apply(get_canvas_id,args = (track_bads,),axis=1)
    #
    # make a dictionary id_dict of names and ids
    #
    name_df.set_index('canvas_id',inplace=True)
    print(name_df.head())
    id_dict = name_df.to_dict(orient='index')
    return id_dict

@click.command()
@click.argument('canvas_file',type=str)
@click.argument('zip_file',type=str)
@click.argument('build_dir',type=str)
def main(canvas_file,zip_file,build_dir):
    build_dir = Path(build_dir)
    notebooks = build_dir.glob("*ipynb")
    html_dir = build_dir / 'html'
    unzip(zip_file,build_dir)
    id_dict = make_namedict(canvas_file)
    for the_file in notebooks:
        print(the_file)
        
#         html_file = build_dir
        
#     notebook_dir=Path(notebook_dir)
#     print(f"starting conversion of {notebook_dir} to html")
#     full_re = f"**/{file_re}"
#     print(f"searcing for {full_re}")
#     notebook_files = list(notebook_dir.glob(full_re))
#     print(f"found {len(notebook_files)} files")
#     for the_notebook in notebook_files:
#         out_file = f"{the_notebook.stem}.html"
#         out_file = the_notebook.parent / out_file
#         make_page(the_notebook,out_file)
#         print(f"through with {out_file}")
#         if out_file.is_file():
#             print(f"wrote {out_file=}")
#         else:
#             print(f"can't find {out_file}")
# ;

