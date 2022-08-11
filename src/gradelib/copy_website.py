import click
import gradelib
import pandas as pd
from pathlib import Path
import sysrsync
import json

version = gradelib.__version__

@click.command()
@click.version_option(version)
@click.argument('classlist_json',type=str)
@click.argument('feedback_folder',type=str)
@click.argument('web_folder',type=str)
def main(classlist_json: str, feedback_folder: str, web_folder: str):
    gradebook_file = Path(classlist_json).resolve()
    with open(gradebook_file,'r') as input:
        class_list = json.load(input)
    for row in class_list:
        short_id = row['short_id']
        full_id = row['the_ids']
        source_path = Path(feedback_folder).resolve() / full_id
        dest_path = Path(web_folder).resolve() / short_id
        
if __name__ == "__main__":
    main()
    
