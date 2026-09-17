import subprocess
import os
import sys

scripts_dir = os.path.abspath("scripts")
sys.path.append(scripts_dir)
from winhelpers import run_windows_program

cl_args = ["/nologo", "/c", "/Od", "/Os", "/Gy", "/GF", "/Op", "scratch/dummy2.cpp", "/Foscratch/dummy2.obj"]
cl = os.path.join(scripts_dir, "prefix", "bin", "cl.exe")
run_windows_program([str(os.path.join(scripts_dir, "th06run.bat")), cl] + cl_args, cwd=os.getcwd())

dumpbin_args = ["/DISASM", "scratch/dummy2.obj"]
dumpbin = os.path.join(scripts_dir, "prefix", "bin", "dumpbin.exe")
with open("scratch/dummy2.asm", "w") as f:
    subprocess.check_call(["wine", dumpbin] + dumpbin_args, stdout=f)
