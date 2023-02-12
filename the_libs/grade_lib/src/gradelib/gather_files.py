"""
collect files from an autograded hierarchy into a single folder

e.g.

gather_files autograded "*exec*html" html_dir 

"""
from pathlib import Path
import click
from .utils import working_directory
import shutil


@click.command()
@click.argument('orig_file_dir',type=str)
@click.argument('file_regex',type=str)
@click.argument('new_file_dir',type=str)
def main(orig_file_dir,file_regex,new_file_dir):
    file_list = []
    all_files = list(Path(orig_func_dir).glob(file_regex))
    for a_file in all_files:
        elements = str(a_file).split('_')
        if elements[1]=='LATE':
            late = elements.pop(1)
            print('found late')
        new_file = f"{elements[0]}-{elements[1]}-lab9_funcs.py"
        file_list.append({'old':str(a_file),'new':new_file})
    new_dir = Path(new_func_dir)
    new_dir.mkdir(parents=True,exist_ok = True)
    for file_pair in file_list:
        print(file_pair)
        old_file = file_pair['old']
        new_file = new_dir / file_pair['new']
        print(old_file, new_file)
        out=shutil.copy(old_file, new_file)
        print(out)

