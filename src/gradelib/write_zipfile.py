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
    canvas_zip = Path(canvas_zip).resolve()
    write_collect(canvas_zip, extracted_zip, assign_name, notebook_name)

