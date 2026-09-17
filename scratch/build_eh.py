import subprocess
import os
import sys

scripts_dir = os.path.abspath("scripts")
sys.path.append(scripts_dir)
from winhelpers import run_windows_program

cl_args = ["/nologo", "/c", "/Od", "/Os", "/Gy", "/GF", "/Op", "/GX", "src/Gui.cpp", "/Fobuild/Gui.obj"]
cl = os.path.join(scripts_dir, "prefix", "bin", "cl.exe")
# We must use run_windows_program properly.
run_windows_program([str(os.path.join(scripts_dir, "th06run.bat")), cl] + cl_args, cwd=os.getcwd())
