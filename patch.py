with open('src/EclManager.hpp', 'r') as f:
    content = f.read()

import re

# Remove DebugEclView
content = re.sub(r'struct DebugEclView.*?;', '', content, flags=re.DOTALL)
content = content.replace("ZUN_ASSERT_SIZE(DebugEclView, 0x688);", "")

with open('src/EclManager.hpp', 'w') as f:
    f.write(content)
