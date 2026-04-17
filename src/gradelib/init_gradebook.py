"""
read a csv file with student ids and create the gradebook.db

python init_gradebook.py gradebook.db id lastname_col firstname_col classlist.csv
"""
from nbgrader.api import Gradebook
import sqlalchemy as dbsql
import pandas as pd
from pathlib import Path
import click
import gradelib

version = gradelib.__version__

@click.command()
@click.version_option(version)
@click.argument('classlist_csv',type=str)
@click.argument('gradebook_file',type=str)
@click.argument('id_col',type=str)
@click.argument('lastname_col',type=str)
@click.argument('firstname_col',type=str)
def main(classlist_csv: str, gradebook_file: str,id_col: str, lastname_col: str,  firstname_col: str):
    """
    read a csv file with student ids and create the gradebook.db

    \b
    example:
    init_gradebook nbgrader_demo/classlist.csv gradebook.db id last_name first_name

    \b
    which will create gradebook.db in the current directory


    where:

    \b
    classlist_csv: path to classlist csv file with columns for id number, lastname and firstname
    gradebook_file:  path to gradebook database to be created
    id_col: name of the id column in the csv file
    lastname_col: name of the lastname column in the csv file
    firstname_col: name of the firstname column in the csv file
    """
    gradebook_file = Path(gradebook_file)
    classlist_csv = Path(classlist_csv)
    db_name=f'sqlite:///{str(gradebook_file)}'
    print(f'data base is {db_name}')

    if gradebook_file.is_file():
        gradebook_file.unlink()
    
    gb = Gradebook(db_name)
    df_gradebook = pd.read_csv(classlist_csv)
    df_gradebook = df_gradebook.set_index(id_col, drop=False)
    print(f"\ndata frame crated from {classlist_csv}\n{df_gradebook.head()}\n")
    for the_id,row  in df_gradebook.iterrows():
        first_name, last_name = row['first_name'], row['last_name']
        student_dict={'first_name':first_name,'last_name':last_name}
        gb.add_student(the_id,**student_dict)

    #check the result by reading db
    print(f"\nwrite out {db_name}\n")
    engine_in = dbsql.create_engine(db_name)
    with engine_in.begin() as connection:
        df = pd.read_sql_table('student',connection)
    print(df)
    
if __name__== "__main__":
    main()


