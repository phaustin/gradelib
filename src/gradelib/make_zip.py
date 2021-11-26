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


def list_files(zip_path, json_path):
    zip_path = Path(zip_path)
    json_path = Path(json_path)
    with ZipFile(zip_path, "r") as myzip:
        with open(json_path, "w") as json_out:
            out = myzip.infolist()
            out_list = []
            for item in out:
                out_list.append(item.filename)
            json.dump(out_list, json_out, indent=4)


def move_files(file_list, new_zip, orig_zip=None):
    """
    turn a list of files into a zip file
    """
    curr_dir = Path()
    new_zip = Path(new_zip)
    with tempfile.TemporaryDirectory(dir=curr_dir) as tmpdirname:
        temp_dir = Path(tmpdirname)
        with working_directory(temp_dir):
            if orig_zip is not None:
                with ZipFile(orig_zip, "r") as in_zip:
                    in_zip.extractall()
            with open(file_list, "r") as f:
                file_list = json.load(f)
            with ZipFile(new_zip, "w") as out_zip:
                for the_file in file_list:
                    out_zip.write(the_file)
            shutil.copy(new_zip, new_zip.parent)
            print(f"copied to {new_zip} to {new_zip.parent}")


def write_collect(oldname, new_zip, assign_name, notebook_name):
    oldname = Path(oldname)
    new_zip = Path(new_zip)
    namelist = []
    curr_dir = Path()
    with ZipFile(oldname, "r") as myzip:
        out = myzip.infolist()
        for item in out:
            if item.filename.find("assign") > -1:
                print(item.filename)
    # pdb.set_trace()
    with tempfile.TemporaryDirectory(dir=curr_dir) as tmpdirname:
        temp_dir = Path(tmpdirname)
        with ZipFile(oldname, "r") as myzip:
            out = myzip.infolist()
            print(out)
            print("created temporary directory", temp_dir)
            for i, the_zip in enumerate(out):
                print("zip filename: ", the_zip.filename)
                elements = the_zip.filename.split("_")
                #
                # mercerkendra_27495_4022961_Finite_Volume_Assignment.ipynb
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
                the_zip.filename = new_name
                print("new name for file: ", new_name)
                new_path = temp_dir / Path(the_zip.filename)
                namelist.append(new_path.name)
                myzip.extract(the_zip, path=temp_dir)

        with working_directory(temp_dir):
            print(f"in {Path().resolve()} {temp_dir}")
            temp_zip = new_zip.name
            print(f"writing zipfile {temp_zip}")
            with ZipFile(temp_zip, "w") as myzip:
                for the_name in namelist:
                    print("filename: ", the_name)
                    myzip.write(the_name)
            shutil.copy(temp_zip, new_zip)
            print(f"copied to {new_zip}")
    return new_zip
