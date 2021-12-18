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
from .grade_lib import make_canvas_index, get_canvas_id, make_namedict
from .utils import working_directory, unzip,  make_page


@click.command()
@click.argument('canvas_file',type=str)
@click.argument('zip_file',type=str)
@click.argument('build_dir',type=str)
def main(canvas_file,zip_file,build_dir):
    build_dir = Path(build_dir)
    notebooks = build_dir.glob("*ipynb")
    html_dir = build_dir / 'html'
    html_dir.mkdir(exist_ok=True,parents=True)
    unzip(zip_file,html_dir)
    id_dict = make_namedict(canvas_file)
    print(id_dict)
        
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
