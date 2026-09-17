import re

with open('src/AnmVm.hpp', 'r') as f:
    hpp = f.read()

# I want to split AnmVm at pos.
# Currently AnmVmBase contains everything.
# Let's read the file and manually split it using a script.
