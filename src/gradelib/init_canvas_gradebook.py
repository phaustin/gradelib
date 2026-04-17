"""
read a csv file with student ids and create the gradebook.db

python init_gradebook.py gradebook.db id_col last_first_col classlist.csv
"""
from nbgrader.api import Gradebook
import sqlalchemy as dbsql
import pandas as pd
from pathlib import Path
import click
import gradelib
from gradelib.grade_lib import make_id

version = gradelib.__version__

@click.command()
@click.version_option(version)
@click.argument('gradebook_file',type=str)
@click.argument('id_col',type=str)
@click.argument('last_first_col',type=str)
@click.argument('classlist_csv',type=str)
def main(classlist_csv: str, gradebook_file: str,id_col: str, last_first_col: str):
    """
    read a csv file with student ids and create the gradebook.db

    \b
    example:
    init_gradebook nbgrader_demo/classlist.csv gradebook.db id_col last_first_col

    \b
    which will create  or modifiy gradebook.db in the current directory


    where:

    \b
    classlist_csv: path to classlist csv file with columns for id number, lastname and firstname
    gradebook_file:  path to gradebook database to be created
    id_col: name of the id column in the csv file
    last_first_col: name of the column with student name in the csv file
    """
    gradebook_file = Path(gradebook_file)
    classlist_csv = Path(classlist_csv)
    db_name=f'sqlite:///{str(gradebook_file)}'
    print(f'data base is {db_name}')

    if gradebook_file.is_file():
        gradebook_file.unlink()
    
    gb = Gradebook(db_name)
    # df_gradebook = pd.read_csv(classlist_csv)
    # df_gradebook = df_gradebook.set_index(id_col, drop=False)
    df_gradebook = pd.read_csv(classlist_csv)
    df_gradebook = make_id(df_gradebook,id_col)
    print(df_gradebook.head())
    print(f"\ndata frame crated from {classlist_csv}\n{df_gradebook.head()}\n")
    for the_id,row  in df_gradebook.iterrows():
        if the_id[0] == '-':
            continue
        lastname,firstname = row['Student'].split(',')
        print(lastname,firstname,the_id)
        student_dict={'first_name':firstname,'last_name':lastname}
        gb.add_student(the_id,**student_dict)

    #check the result by reading db
    print(f"\nwrite out {db_name}\n")
    engine_in = dbsql.create_engine(db_name)
    with engine_in.begin() as connection:
        df = pd.read_sql_table('student',connection)
    print(df)
    
if __name__== "__main__":
    main()


