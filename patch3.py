with open('src/EclManager.hpp', 'r') as f:
    content = f.read()

import re

# We can just look for typedef char* EclFileName; and replace everything down to struct EclManager
start = content.find("typedef char* EclFileName;")
end = content.find("struct EclManager", start)

if start != -1 and end != -1:
    content = content[:start] + content[end:]

with open('src/EclManager.hpp', 'w') as f:
    f.write(content)

