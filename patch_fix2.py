with open('src/EclManager.cpp', 'r') as f:
    content = f.read()

# Remove the bad stub Load and leave only GetTimelineCount and GetTimeline in namespace
bad_load = """
ZunResult EclManager::Load(char *ecl)
{
    // stub - actual implementation already exists above
    return ZUN_SUCCESS;
}

"""
content = content.replace(bad_load, "\n")

with open('src/EclManager.cpp', 'w') as f:
    f.write(content)

print("Done")
