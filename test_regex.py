import re
line = "i32 AnmManager::ExecuteScript(AnmVm *vm)"
m1 = re.match(r'^[a-zA-Z_0-9]+.* AnmManager::([a-zA-Z_0-9]+)\(', line)
m2 = re.match(r'^[a-zA-Z_0-9]+ AnmManager::([a-zA-Z_0-9]+)\(', line)
print("m1:", m1)
print("m2:", m2)
