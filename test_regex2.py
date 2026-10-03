import re
lines = open('src/AnmManager.cpp').readlines()
print("line 946:", repr(lines[945]))
m1 = re.match(r'^[a-zA-Z_0-9]+.* AnmManager::([a-zA-Z_0-9]+)\(', lines[945])
print("m1:", m1)
