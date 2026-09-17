import os
import re

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.cpp'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            # Simple single line pattern (no inner parenthesis)
            new_content = re.sub(r'\(ZunBool\)\(([^()]*?)\.current\s*([<>=!]+)\s*([^()]*?)\)', r'(\1 \2 \3)', content)
            
            # Specific multiline replacements for BulletManager
            new_content = new_content.replace(
                '(ZunBool)(curBullet->timer.current >=\n                                  curBullet->dirChangeInterval * (curBullet->dirChangeNumTimes + 1))',
                '(curBullet->timer >=\n                                  curBullet->dirChangeInterval * (curBullet->dirChangeNumTimes + 1))'
            )
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
