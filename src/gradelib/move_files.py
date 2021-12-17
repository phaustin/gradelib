"""
move all files containing a string with a new filename

move_files orig_file_dir file_regex new_file_dir new_filename

e.g.

move_files autograded "*lab_wk9*exec*ipynb" lab_wk9.ipynb

"""
from pathlib import Path
import click
from .utils import working_directory
import shutil


@click.command()
@click.argument('orig_file_dir',type=str)
@click.argument('file_regex',type=str)
@click.argument('new_filename',type=str)
def main(orig_file_dir,file_regex,new_filename):
    file_list = []
    new_regex = f"**/{file_regex}"
    orig_files = list(Path(orig_file_dir).glob(new_regex))
    print(f"found {len(orig_files)} files")
    file_list=[]
    for the_file in orig_files:
        new_file = the_file.parent / new_filename
        if new_file.is_file():
            new_file.unlink()
        shutil.copy(the_file, new_file)

