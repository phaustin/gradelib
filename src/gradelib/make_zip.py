"""
read a canvas notebook submission zip file and rename to
standard pattern
"""
import json
import shutil
import tempfile
from pathlib import Path
from zipfile import ZipFile

from .utils import working_directory

def rename_file(zip_filename,assign_name, notebook_name):
    """
    given a zip_filename like:
      mercerkendra_27495_4022961_Finite_Volume_Assignment.ipynb
      or mercerkendra_LATE_27495_4022961_Finite_Volume_Assignment.ipynb
    and assign_name: "week2_lab"
        notebook_name: "Finite_Volume_Assignment.ipynb"
    split on underscore and capture the canvas id and name
    rewrite the name to the new format:
      week2_lab-mercerkendra_27495_attempt_Finite_Volume_Assignment.ipynb

    zip_filename: original filename from canvas archive
    assign_name:  nbgrader assignment
    notebook_name: nbgrader notebook
    """
    print(f"{zip_filename=}")
    elements = zip_filename.split("_")
    if elements[1]=='LATE':
        late = elements.pop(1)
        print('found late')
    if (elements[-1].find('ipynb') == -1 or elements[-1].find('func') > -1):
        raise ValueError("not an ipynb or func.py file")
    #
    # student name is elements[0]
    #
    # canvasid is elements[1]
    #
    the_id = elements[1]
    if the_id == "late":
        the_id = elements[2]
    new_name = (
        f"{assign_name}-{elements[0]}_{the_id}_attempt_{notebook_name}"
    )
    return new_name

def write_collect(canvas_zip, grader_zip, assign_name, notebook_name):
    """
    create a temporary directory and extract each file from the canvas_zip archive
    renaming it to an nbgrader-compatible filename and writing it to
    the new archive grader_zip which will be in the same directory as canvas_zip

    canvas_zip: full Path to canvas zipfile
    grader_zip: filename of new zipfile
    assign_name: nbgrader assignment
    notebook_name: notebook to run
    """
    canvas_zip = Path(canvas_zip).resolve()
    canvas_dir = canvas_zip.parent
    grader_zip = canvas_dir / grader_zip
    namelist=[]
    with tempfile.TemporaryDirectory(dir=canvas_dir) as tmpdirname:
        temp_path = Path(tmpdirname)
        with working_directory(temp_path):
            with ZipFile(canvas_zip, "r") as can_archive:
                out = can_archive.infolist()
                for item in out:
                    old_name=item.filename
                    new_name = rename_file(item.filename,assign_name,notebook_name)
                    can_archive.extract(old_name, path=temp_path)
                    namelist.append((old_name,new_name))
            with ZipFile(grader_zip, "w") as grader_archive:
                for oldname,newname in namelist:
                    print(f"{(oldname,newname)=}")
                    grader_archive.write(filename=oldname,arcname=newname)
