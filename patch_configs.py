import json
import csv

with open('objdiff.json', 'r') as f:
    objdiff = json.load(f)

new_objects = [
    {"name": "Controller", "target_path": "build/objdiff/orig/Controller.obj", "base_path": "build/objdiff/reimpl/Controller.obj", "reverse_fn_order": False},
    {"name": "font", "target_path": "build/objdiff/orig/font.obj", "base_path": "build/objdiff/reimpl/font.obj", "reverse_fn_order": False},
    {"name": "FileSystem", "target_path": "build/objdiff/orig/FileSystem.obj", "base_path": "build/objdiff/reimpl/FileSystem.obj", "reverse_fn_order": False},
    {"name": "GameErrorContext", "target_path": "build/objdiff/orig/GameErrorContext.obj", "base_path": "build/objdiff/reimpl/GameErrorContext.obj", "reverse_fn_order": False},
    {"name": "ZunMath", "target_path": "build/objdiff/orig/ZunMath.obj", "base_path": "build/objdiff/reimpl/ZunMath.obj", "reverse_fn_order": False},
]

objects = objdiff['objects']
global_idx = next(i for i, obj in enumerate(objects) if obj['name'] == 'Global')
objects[global_idx+1:global_idx+1] = new_objects

with open('objdiff.json', 'w') as f:
    json.dump(objdiff, f, indent=4)

with open('config/ghidra_ns_to_obj.csv', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('Global,'):
        new_lines.append('Global,th06::Chain,th06::ChainElem\n')
        new_lines.append('Controller,th06::Controller\n')
        new_lines.append('font,th06::CMyFont\n')
        new_lines.append('FileSystem,th06::FileSystem\n')
        new_lines.append('GameErrorContext,th06::GameErrorContext\n')
        new_lines.append('ZunMath,th06::Rng,th06::utils\n')
    else:
        new_lines.append(line)

new_lines.sort()

with open('config/ghidra_ns_to_obj.csv', 'w') as f:
    f.writelines(new_lines)

with open('scripts/configure.py', 'r') as f:
    content = f.read()

new_sources = '"Controller",\n            "font",\n            "FileSystem",\n            "GameErrorContext",\n            "ZunMath",'
content = content.replace('"Global",', '"Global",\n            ' + new_sources)

with open('scripts/configure.py', 'w') as f:
    f.write(content)
