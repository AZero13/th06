with open('src/EclManager.cpp', 'r') as f:
    content = f.read()

# Remove the methods appended outside the namespace
content = content.rstrip()
# Remove the trailing GetTimelineCount and GetTimeline methods that are outside namespace
marker = "}; // namespace th06"
idx = content.rfind(marker)
if idx != -1:
    content = content[:idx + len(marker)]

# Now insert the methods INSIDE the namespace, before closing it
insert_point = content.rfind("}; // namespace th06")
new_methods = """
ZunResult EclManager::Load(char *ecl)
{
    // stub - actual implementation already exists above
    return ZUN_SUCCESS;
}

i32 EclManager::GetTimelineCount()
{
    return 1;
}

EclTimelineInstr *EclManager::GetTimeline(i32 timelineIdx)
{
    return this->eclFile->timelineOffsets[timelineIdx];
}
"""

# Actually, just move those two methods before the closing namespace brace
content = content[:insert_point] + new_methods + content[insert_point:]

with open('src/EclManager.cpp', 'w') as f:
    f.write(content)

print("Done")
