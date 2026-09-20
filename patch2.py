with open('src/EnemyManager.cpp', 'r') as f:
    content = f.read()

content = content.replace("this->timelineInstr = g_EclManager.timeline;", "this->timelineInstr = g_EclManager.GetTimeline(0);")

with open('src/EnemyManager.cpp', 'w') as f:
    f.write(content)

