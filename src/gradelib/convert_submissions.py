"""
convert a canvas sumissions zip into a folder of web pages

convert_submissions canvas_file zip_file build_dir

export canvas_file=/home/phil/Nextcloud/eosc211_2021/tests/e211_2021_grading/2021-12-16T1827_Grades-EOSC_211_101_2021W1.csv

export zipfile=/home/jupyter/repos/nbgrader_dir/datadir/e211_files/canvas/week2_extracted.zip

convert_submissions $canvas_file $zipfile .


"""

from pathlib import Path
import click
import shutil
from zipfile import ZipFile
import pandas as pd
from .grade_lib import make_canvas_index, get_canvas_id, make_namedict
from .utils import working_directory, unzip,  make_page


@click.command()
@click.argument('canvas_file',type=str)
@click.argument('zip_file',type=str)
@click.argument('build_dir',type=str)
def main(canvas_file,zip_file,build_dir):
    """
    convert a canvas sumissions zip into a folder of web pages

    convert_submissions canvas_file zip_file build_dir

    example usage:

    export canvas_file=/home/phil/Nextcloud/eosc211_2021/tests/e211_2021_grading/2021-12-16T1827_Grades-EOSC_211_101_2021W1.csv

    export zipfile=/home/jupyter/repos/nbgrader_dir/datadir/e211_files/canvas/week2_extracted.zip

    convert_submissions $canvas_file $zipfile .
    """
    build_dir = Path(build_dir)
    html_dir = build_dir / 'html'
    html_dir.mkdir(exist_ok=True,parents=True)
    unzip(zip_file,html_dir)
    id_dict = make_namedict(canvas_file)
    notebooks = html_dir.glob("*ipynb")
    for the_file in notebooks:
        html_file = the_file.with_suffix('.html')
        make_page(the_file,html_file)
        if html_file.is_file():
            print(f"constructed {html_file}")
        else:
            print(f"don't see {html_file}")
