with open('src/font.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('class CMyFont'):
        skip = True
        continue
    if skip and line.startswith('};'):
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

with open('src/font.cpp', 'w') as f:
    f.writelines(new_lines)
