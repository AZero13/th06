with open('src/EclManager.cpp', 'r') as f:
    content = f.read()

# Remove added methods
import re
content = re.sub(r'\n\ni32 EclManager::GetTimelineCount\(\).*?EclTimelineInstr \*EclManager::GetTimeline.*?\}\n\}\; // namespace th06',
    '\n}; // namespace th06', content, flags=re.DOTALL)

# Restore the timeline = line
content = content.replace(
    '    for (int idx = 0; idx < this->eclFile->mainCount; idx++)',
    '    this->timeline = this->eclFile->timelineOffsets[0];\n    for (int idx = 0; idx < this->eclFile->mainCount; idx++)'
)

with open('src/EclManager.cpp', 'w') as f:
    f.write(content)

print("Done")
