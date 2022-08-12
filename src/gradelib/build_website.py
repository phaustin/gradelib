import click
from gradelib.make_short_ids import create_keydict, make_short_ids
from gradelib.grade_lib import make_id
import gradelib
import pandas as pd
from pathlib import Path
import json

version = gradelib.__version__

def add_col(row,shortid_dict):
    row['short_id']=shortid_dict[row.name]
    return row

@click.command()
@click.version_option(version)
@click.argument('classlist_csv',type=str)
@click.argument('id_col',type=str)
@click.argument('web_folder',type=str)
def main(classlist_csv: str, id_col: str, web_folder: str):
    """
    \b
    build_website classlist.csv id e211_nbgrader_2022/website_e211/e211_marked_labs
    """
    gradebook_file = Path(classlist_csv).resolve()
    df_gradebook = pd.read_csv(gradebook_file)
    df_gradebook = make_id(df_gradebook, id_col)
    df_gradebook = df_gradebook.set_index('the_ids',drop=False)
    id_list = list(df_gradebook['the_ids'])
    keylen=3
    shortid_dict, multiid_dict = create_keydict(id_list,keylen=keylen)
    new_dict, new_key_dict =make_short_ids(shortid_dict,multiid_dict,keylen=keylen)
    print(new_dict)
    df_gradebook = df_gradebook.apply(add_col,args=(new_dict,),axis=1)
    web_folder = Path(web_folder).resolve()
    for sid in df_gradebook['short_id']:
        new_dir= web_folder / sid
        new_dir.mkdir(exist_ok=True,parents=True)
    json_name = f"{gradebook_file.stem}_with_shortids.json"
    full_path = gradebook_file.parent / json_name
    output_list = df_gradebook.to_dict(orient="records")
    with open(full_path,'w') as outfile:
        json.dump(output_list,outfile,indent=4)
    
if __name__ == "__main__":
    main()
    
