import json

with open('objdiff.json', 'r') as f:
    objdiff = json.load(f)

new_objects = [
    {"name": "File", "target_path": "build/objdiff/orig/File.obj", "base_path": "build/objdiff/reimpl/File.obj", "reverse_fn_order": False},
    {"name": "grpfont", "target_path": "build/objdiff/orig/grpfont.obj", "base_path": "build/objdiff/reimpl/grpfont.obj", "reverse_fn_order": False},
]

objects = objdiff['objects']
global_idx = next(i for i, obj in enumerate(objects) if obj['name'] == 'Global')
objects[global_idx+1:global_idx+1] = new_objects
objdiff['objects'] = objects

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
    else:
        new_lines.append(line)

new_lines.sort()

with open('config/ghidra_ns_to_obj.csv', 'w') as f:
    f.writelines(new_lines)

with open('scripts/configure.py', 'r') as f:
    content = f.read()

content = content.replace('"Global",', '"Global",\n            "File",\n            "grpfont",')
with open('scripts/configure.py', 'w') as f:
    f.write(content)
