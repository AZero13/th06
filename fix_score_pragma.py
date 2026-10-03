with open('src/score.cpp', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith('#pragma var_order(difficulty'):
        continue
    if 'shotType, originalByte' in line:
        continue
    new_lines.append(line)

with open('src/score.cpp', 'w') as f:
    f.writelines(new_lines)

with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('void ResultScreen::WriteScore'):
        lines.insert(i, '#pragma var_order(difficulty, highScoreSlot, fileBuffer, sizeOfFile, scoreNode, shottype, clrd, catk, pscr, stage,     \\\n                  shotType, originalByte, remainingSize, xorValue, bytes, sd)\n')
        break

final_lines = []
namespace_count = 0
for line in reversed(lines):
    if line.startswith('} // namespace th06'):
        namespace_count += 1
        if namespace_count > 1:
            continue
    final_lines.append(line)
final_lines.reverse()

with open('src/ResultScreen.cpp', 'w') as f:
    f.writelines(final_lines)

with open('src/AnmManager.cpp', 'r') as f:
    lines = f.readlines()

final_lines = []
namespace_count = 0
for line in reversed(lines):
    if line.startswith('} // namespace th06'):
        namespace_count += 1
        if namespace_count > 1:
            continue
    final_lines.append(line)
final_lines.reverse()

with open('src/AnmManager.cpp', 'w') as f:
    f.writelines(final_lines)

