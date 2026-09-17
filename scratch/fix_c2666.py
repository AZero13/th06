import re
with open('src/AnmManager.cpp', 'r') as f:
    content = f.read()

content = content.replace('vm->scaleInterpTime >= vm->scaleInterpEndTime', 'vm->scaleInterpTime >= (i32)vm->scaleInterpEndTime')
content = content.replace('vm->alphaInterpTime >= vm->alphaInterpEndTime', 'vm->alphaInterpTime >= (i32)vm->alphaInterpEndTime')
content = content.replace('vm->posInterpTime >= vm->posInterpEndTime', 'vm->posInterpTime >= (i32)vm->posInterpEndTime')

with open('src/AnmManager.cpp', 'w') as f:
    f.write(content)
