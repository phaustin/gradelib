from setuptools_scm import get_version
from pathlib import Path
root_dir = Path().resolve()
print(f"{root_dir=}")
git_version = get_version(root=str(root_dir))
print(f"{git_version=}")
import paged_html_theme
print(f"{paged_html_theme.__version__}")



