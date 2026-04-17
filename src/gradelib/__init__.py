from os import path

from pathlib import Path
root_dir = Path(__file__).resolve().parent
# print(f"{root_dir=}")

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("gradelib")
except PackageNotFoundError:
    __version__ = "unknown version"

try:
    from ._version import version_tuple
except ImportError:
    version_tuple = (0, 0, "unknown version")

print("in sat_lib init")
