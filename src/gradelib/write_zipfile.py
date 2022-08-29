import click
from pathlib import Path
from .make_zip import write_collect
import gradelib

version = gradelib.__version__

@click.command()
@click.argument('canvas_zip',type=str)
@click.argument('extracted_zip',type=str)
@click.argument('assign_name',type=str)
@click.argument('notebook_name',type=str)
@click.version_option(version)
def main(canvas_zip,extracted_zip,assign_name,notebook_name):
    """
    convert a canvas zipfile, with notebooks named like:

      mercerkendra_27495_4022961_Finite_Volume_Assignment.ipynb

    into a nbgrader compatibile zipfile with notebook names like:

      week2_lab-mercerkendra_27495_attempt_Finite_Volume_Assignment.ipynb

    Parameters
    ----------

    canvas_zip: path to zipfile downloaded from canvas

    extracted_zip: path to output zipfile to be written

    assign_name: name of the nbgrader assignment

    notebook_name: name of the distributed nbgrader notebook Finite_Volume_Assignment.ipynb

    Usage
    ------

    wrie_zipfile canvas_lab2.zip  week2_labs.zip week2_lab 
    """
    canvas_zip = Path(canvas_zip).resolve()
    write_collect(canvas_zip, extracted_zip, assign_name, notebook_name)

