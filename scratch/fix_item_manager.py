import re

with open('src/ItemManager.hpp', 'r') as f:
    hpp = f.read()

# Remove the empty braces
hpp = re.sub(r'\{\s*\}', '', hpp)
# Put back the struct Item {
hpp = hpp.replace('struct Item', 'struct Item\n{')
with open('src/ItemManager.hpp', 'w') as f:
    f.write(hpp)
