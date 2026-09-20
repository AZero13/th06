with open('src/EclManager.cpp', 'r') as f:
    content = f.read()

content = content.replace("this->timeline = this->eclFile->timelineOffsets[0];", "")

new_methods = """
i32 EclManager::GetTimelineCount()
{
    return 1; // Or whatever is appropriate
}

EclTimelineInstr* EclManager::GetTimeline(i32 timelineIdx)
{
    return this->eclFile->timelineOffsets[timelineIdx];
}
"""

content = content + "\n" + new_methods

with open('src/EclManager.cpp', 'w') as f:
    f.write(content)
