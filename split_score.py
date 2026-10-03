import re

with open('src/ResultScreen.cpp', 'r') as f:
    lines = f.readlines()

def find_lines(pattern):
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            return i
    return -1

score_start = find_lines(r'ScoreDat \*OpenScore')
# Find the end of score functions: it's right before ResultScreen_RegisterChain
score_end = find_lines(r'ZunResult ResultScreen_RegisterChain')

if score_start != -1 and score_end != -1:
    score_code = lines[score_start:score_end]
    
    # Also extract the g_AlphabetList, g_CharacterList, g_SpellcardsWeightsList?
    # Wait, these are used by ResultScreen. We should leave them in ResultScreen!
    # Does score.cpp use them? ParseCatk uses g_AlphabetList? No.
    
    content = '#include "th06.hpp"\n#include "ResultScreen.hpp"\n\nnamespace th06\n{\n'
    content += "".join(score_code)
    content += '}\n'
    
    with open('src/score.cpp', 'w') as f:
        f.write(content)
        
    new_result = lines[:score_start] + lines[score_end:]
    with open('src/ResultScreen.cpp', 'w') as f:
        f.writelines(new_result)
    print("Score split done.")
else:
    print("Could not find score functions.")
