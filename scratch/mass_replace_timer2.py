import os
import re

for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.cpp') or file.endswith('.hpp'):
            path = os.path.join(root, file)
            with open(path, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Replace .InitializeForPopup() with = 0
            content = re.sub(r'([a-zA-Z0-9_\->.]+)\.InitializeForPopup\(\)', r'\1 = 0', content)
            
            # Replace .NextTick() with ++
            content = re.sub(r'([a-zA-Z0-9_\->.]+)\.NextTick\(\)', r'\1++', content)
            
            # Specifically handle the IncrementInline case in EclManager
            if 'IncrementInline' in content:
                content = content.replace('enemy->currentContext.time.IncrementInline(\n                    *EnemyEclInstr::GetVar(enemy, &instruction->args.timeSet.timeToSet, NULL))', 'enemy->currentContext.time += *EnemyEclInstr::GetVar(enemy, &instruction->args.timeSet.timeToSet, NULL)')
                
            if content != original_content:
                with open(path, 'w') as f:
                    f.write(content)
