import re
with open('scripts/configure.py', 'r') as f:
    text = f.read()

# I want to put FileAbstraction back into pbg3_sources
text = text.replace('            "FileAbstraction",\n            "TextHelper",\n            "AsciiManager",\n', '            "AsciiManager",\n')
text = text.replace('            "Pbg3Archive",\n', '            "Pbg3Archive",\n            "FileAbstraction",\n')

# And I want to put TextHelper BEFORE AsciiManager
text = text.replace('            "AsciiManager",\n', '            "TextHelper",\n            "AsciiManager",\n')

with open('scripts/configure.py', 'w') as f:
    f.write(text)
