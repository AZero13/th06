import os
import re

for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.cpp') or file.endswith('.hpp'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            new_content = re.sub(r'([a-zA-Z0-9_\->.]+)\.InitializeForPopup\(\)', r'\1 = 0', content)
            new_content = re.sub(r'([a-zA-Z0-9_\->.]+)\.SetCurrent\(([^)]+)\)', r'\1 = \2', new_content)
            
            if new_content != content:
                with open(path, 'w') as f:
                    f.write(new_content)
