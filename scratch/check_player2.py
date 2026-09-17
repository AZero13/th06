with open('src/Player.hpp', 'r') as f:
    text = f.read()

import re
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'ZunTimer' in line or 'ZunTimer' in line:
        print(f"{i}: {line}")
