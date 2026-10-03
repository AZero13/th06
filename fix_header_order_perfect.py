with open('src/ResultScreen.hpp', 'r') as f:
    lines = f.readlines()

# We want to extract ALL structs and put them in a clean order.
# The order should be:
# 1. Th6k
# 2. Catk, Clrd, Pscr, Hscr
# 3. ScoreListNode
# 4. ScoreDat
# 5. ResultScreen
# 6. Global functions (OpenScore, ParseCatk, etc.)

def extract_struct(name, lines):
    start = -1
    for i, line in enumerate(lines):
        if line.startswith(f'struct {name}'):
            start = i
            break
    if start == -1:
        return []
    end = start
    for i in range(start, len(lines)):
        if lines[i].startswith('ZUN_ASSERT_TYPE(' + name) or lines[i].startswith('};'):
            if lines[i].startswith('};'):
                # check if next line is assert
                if i+1 < len(lines) and lines[i+1].startswith('ZUN_ASSERT_TYPE(' + name):
                    end = i+1
                else:
                    end = i
            else:
                end = i
            break
    
    code = lines[start:end+1]
    # blank line
    code.append('\n')
    # blank out from original
    for i in range(start, end+1):
        lines[i] = ''
    return code

structs = []
for name in ['Th6k', 'Catk', 'Clrd', 'Pscr', 'Hscr', 'ScoreListNode', 'ScoreDat', 'ResultScreen']:
    structs.extend(extract_struct(name, lines))

# Now remove the forward declaration if it exists
for i, line in enumerate(lines):
    if line.strip() == 'struct ResultScreen;':
        lines[i] = ''

# Find where to insert
insert_idx = -1
for i, line in enumerate(lines):
    if line.startswith('enum ResultScreenState'):
        insert_idx = i
        break

if insert_idx != -1:
    # Insert after the two enums
    # Let's just find the end of ResultScreenMainMenuCursor
    for i in range(insert_idx, len(lines)):
        if lines[i].startswith('enum ResultScreenMainMenuCursor'):
            for j in range(i, len(lines)):
                if lines[j].startswith('};'):
                    insert_idx = j + 2
                    break
            break

if insert_idx != -1:
    lines = lines[:insert_idx] + structs + lines[insert_idx:]

# filter out empty lines that we blanked out
final_lines = []
for line in lines:
    if line != '':
        final_lines.append(line)

with open('src/ResultScreen.hpp', 'w') as f:
    f.writelines(final_lines)
