"""
execute a notebook file hierarchy

run_notebooks orig_notebook_dir file_re

run_notebooks autograded "lab_wk9*ipynb"
"""

from pathlib import Path
import click
from .utils import working_directory
import shutil
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_file(notebook_file, result_file):
    print(f"running {notebook_file}")
    exec_dir = str(notebook_file.parent)
    with open(notebook_file) as f:
        nb = nbformat.read(f, as_version=4)
        ep = ExecutePreprocessor(timeout=600,allow_errors=True, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': exec_dir}})
        with open(result_file, 'wt') as f:
            nbformat.write(nb, f)


@click.command()
@click.argument('notebook_folder',type=str)
@click.argument('file_re',type=str)
def main(notebook_folder, file_re):
    notebook_folder=Path(notebook_folder).resolve()
    file_re = f"**/{file_re}"
    print(f"starting conversion in {notebook_folder} with {file_re=}")
    file_dict = {}
    notebook_files = list(notebook_folder.glob(file_re))
    print(f"found {len(notebook_files)} files")
    for the_notebook in notebook_files:
        if str(the_notebook).find("exec") > -1:
            print(f"deleting {the_notebook}")
            the_notebook.unlink()
            continue
        print(f"attempting {the_notebook}")
        out_file = f"{the_notebook.stem}_exec.ipynb"
        out_file = the_notebook.parent / out_file
        run_file(the_notebook,out_file)
        print(f"through with {out_file}")
        if  out_file.is_file():
            print(f"wrote {out_file=}")
        else:
            print(f"can't find {out_file}")


