"""
Calculates how many different districts letters are there
"""

import config as cfg

lines = open('district.txt').read().split("\n")

letter = dict()

for line in lines:
    for ch in line:
        if ch in letter:
            letter[ch] += 1
        else:
            letter[ch] = 1
        # end if
    # end for
# end for

for ch in cfg.LETTER_LABELS.keys():
    if ch in letter:
        del letter[ch]
# end for

for k, v in letter.items():
    print(k)
# end for
