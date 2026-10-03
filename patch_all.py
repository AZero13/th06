import json
import csv

with open('objdiff.json', 'r') as f:
    objdiff = json.load(f)

new_objects = [
    {"name": "File", "target_path": "build/objdiff/orig/File.obj", "base_path": "build/objdiff/reimpl/File.obj", "reverse_fn_order": False},
    {"name": "grpfont", "target_path": "build/objdiff/orig/grpfont.obj", "base_path": "build/objdiff/reimpl/grpfont.obj", "reverse_fn_order": False},
    {"name": "score", "target_path": "build/objdiff/orig/score.obj", "base_path": "build/objdiff/reimpl/score.obj", "reverse_fn_order": False},
    {"name": "sprtanim", "target_path": "build/objdiff/orig/sprtanim.obj", "base_path": "build/objdiff/reimpl/sprtanim.obj", "reverse_fn_order": False},
    {"name": "sprtdisp", "target_path": "build/objdiff/orig/sprtdisp.obj", "base_path": "build/objdiff/reimpl/sprtdisp.obj", "reverse_fn_order": False},
]

# We don't remove Global, ResultScreen, AnmManager.
objects = objdiff['objects']
objdiff['objects'] = objects + new_objects

with open('objdiff.json', 'w') as f:
    json.dump(objdiff, f, indent=4)

with open('config/ghidra_ns_to_obj.csv', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('Global,'):
        new_lines.append('Global,th06::Chain,th06::ChainElem,th06::Controller,th06::GameErrorContext,th06::Rng,th06::utils\n')
        new_lines.append('grpfont,th06::CMyFont\n')
        new_lines.append('File,th06::FileSystem\n')
    elif line.startswith('ResultScreen,'):
        new_lines.append('ResultScreen,th06::ResultScreen\n')
        new_lines.append('score,th06::OpenScore,th06::ParseCatk\n') # Just dummy namespaces to let ghidra script pass
    elif line.startswith('AnmManager,'):
        new_lines.append('AnmManager,th06::AnmManager\n')
        new_lines.append('sprtanim,th06::AnmVm\n')
        new_lines.append('sprtdisp,th06::sprtdisp\n') # dummy
    else:
        new_lines.append(line)

new_lines.sort()

with open('config/ghidra_ns_to_obj.csv', 'w') as f:
    f.writelines(new_lines)

with open('scripts/configure.py', 'r') as f:
    content = f.read()

new_sources = '"File",\n            "grpfont",\n            "score",\n            "sprtanim",\n            "sprtdisp",'
content = content.replace('"Global",', '"Global",\n            ' + new_sources)

with open('scripts/configure.py', 'w') as f:
    f.write(content)
print("Config patched.")
