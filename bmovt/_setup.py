import os
import sys
from pathlib import Path
parent_dir = str(Path().resolve())
sys.path.append(parent_dir)
os.chdir(parent_dir)

from setuptools import setup, find_packages

nuitka_file = "setup.py"

setup(
    name="bmovt",    #パッケージ名
    version="0.0.1",
    description="bmovt: Boot Movie Maker",
    long_description="",
    author="DriCro6663",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 1 - Planning"
    ], 
    packages=["libs", ".libs"],   #パッケージのサブフォルダー
    command_options={
        "nuitka": {
            "--mingw64": (nuitka_file, True), 
            "--onefile": (nuitka_file, True),
            "--follow-imports": (nuitka_file, True),
            "--enable-plugin": (nuitka_file, ["numpy", "pyqt5"]), 
            "--include-package": (nuitka_file, "bmovt"), 
            "--windows-icon-from-ico": (nuitka_file, "../res/bmovt.ico"), 
        }
    }
)