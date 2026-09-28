import re
data = open('src/TextHelper.cpp', 'r').read()

# Move <string> outside namespace
data = data.replace('#include <string>', '')
data = data.replace('#include "i18n.hpp"', '#include "i18n.hpp"\n#include <string>')
open('src/TextHelper.cpp', 'w').write(data)
