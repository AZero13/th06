with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
last_pragma = -1
for i, line in enumerate(lines):
    if '#pragma var_order(i, vm)' in line:
        if last_pragma != -1 and i - last_pragma < 5:
            last_pragma = i
            continue # Skip duplicate
        last_pragma = i
    new_lines.append(line)

final_lines = []
namespace_count = 0
for line in reversed(new_lines):
    if line.startswith('} // namespace th06'):
        namespace_count += 1
        if namespace_count > 1:
            continue
    final_lines.append(line)

final_lines.reverse()

with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(final_lines)
