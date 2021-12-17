import click
from setuptools_scm import get_version
from .make_zip import write_collect

version = get_version()

@click.command()
@click.argument('canvas_zip',type=str)
@click.argument('extracted_zip',type=str)
@click.argument('assign_name',type=str)
@click.argument('notebook_name',type=str)
@click.version_option(version)
def main(canvas_zip,extracted_zip,assign_name,notebook_name):
    write_collect(zipfile, new_zip, assign_name, notebook_name)

