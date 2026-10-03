with open('src/ResultScreen.hpp', 'r') as f:
    lines = f.readlines()

start = -1
for i, l in enumerate(lines):
    if l.startswith('struct ResultScreen'):
        start = i
        break

end = start
for i in range(start, len(lines)):
    if lines[i].startswith('};'):
        end = i
        break

lines = lines[:start] + lines[end+1:]

with open('src/ResultScreen.hpp', 'w') as f:
    f.writelines(lines)
