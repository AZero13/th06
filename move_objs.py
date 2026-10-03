with open('scripts/configure.py', 'r') as f:
    text = f.read()

text = text.replace('            "FileAbstraction",\n', '')
text = text.replace('            "TextHelper",\n', '')

# Insert them before AsciiManager
text = text.replace('            "AsciiManager",\n', '            "FileAbstraction",\n            "TextHelper",\n            "AsciiManager",\n')

with open('scripts/configure.py', 'w') as f:
    f.write(text)
