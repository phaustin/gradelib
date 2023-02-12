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
    """
    \b
    copy_website classlist_with_shortids.json nbgrader/container_home/feedback e211_nbgrader_2022/website_e211/e211_marked_labs    
    """
    gradebook_file = Path(classlist_json).resolve()
    with open(gradebook_file,'r') as input:
        class_list = json.load(input)
    for row in class_list:
        short_id = row['short_id']
        full_id = row['the_ids']
        source_path = Path(feedback_folder).resolve() / full_id
        dest_path = Path(web_folder).resolve() / short_id
        source_path, dest_path = str(source_path),str(dest_path)
        source_path = f"{source_path}/"
        dest_path = f"{dest_path}/"
        print(source_path,dest_path)
        sysrsync.run(source=source_path,destination=dest_path,
                     options=['-r'])
        
if __name__ == "__main__":
    main()
    
