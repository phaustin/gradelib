"""
build web pages from ipynb files

build_html notebook_dir file_re

e.g.:
build_html autograded "lab_wk9*ipynb"
"""

from pathlib import Path
import click
import shutil
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

def make_page(notebook_file,html_file):
    with open(notebook_file,'r') as in_file:
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'classic'
        (body, resources) = html_exporter.from_file(in_file)
    with open(html_file,'w') as out_file:
        out_file.write(body)


@click.command()
@click.argument('notebook_dir',type=str)
@click.argument('file_re',type=str)
def main(notebook_dir,file_re):
    notebook_dir=Path(notebook_dir)
    print(f"starting conversion of {notebook_dir} to html")
    full_re = f"**/{file_re}"
    print(f"searcing for {full_re}")
    notebook_files = list(notebook_dir.glob(full_re))
    print(f"found {len(notebook_files)} files")
    for the_notebook in notebook_files:
        out_file = f"{the_notebook.stem}.html"
        out_file = the_notebook.parent / out_file
        make_page(the_notebook,out_file)
        print(f"through with {out_file}")
        if out_file.is_file():
            print(f"wrote {out_file=}")
        else:
            print(f"can't find {out_file}")


