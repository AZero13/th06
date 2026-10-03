import json

with open('objdiff.json', 'r') as f:
    objdiff = json.load(f)

objects = [obj for obj in objdiff['objects'] if obj['name'] not in ('score', 'sprtanim', 'sprtdisp')]
objdiff['objects'] = objects

with open('objdiff.json', 'w') as f:
    json.dump(objdiff, f, indent=4)

with open('config/ghidra_ns_to_obj.csv', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('score,') or line.startswith('sprtanim,') or line.startswith('sprtdisp,'):
        continue
    # Revert ResultScreen and AnmManager namespaces
    if line.startswith('ResultScreen,th06::ResultScreen'):
        new_lines.append('ResultScreen,th06::ResultScreen,th06::OpenScore,th06::ParseCatk\n') # Add dummy back? Wait, originally it was ResultScreen,th06::ResultScreen
        continue
    if line.startswith('AnmManager,th06::AnmManager'):
        new_lines.append('AnmManager,th06::AnmVm,th06::AnmManager\n')
        continue
    new_lines.append(line)

new_lines.sort()

with open('config/ghidra_ns_to_obj.csv', 'w') as f:
    f.writelines(new_lines)

with open('scripts/configure.py', 'r') as f:
    content = f.read()

content = content.replace('\n            "score",\n            "sprtanim",\n            "sprtdisp",', '')
with open('scripts/configure.py', 'w') as f:
    f.write(content)
