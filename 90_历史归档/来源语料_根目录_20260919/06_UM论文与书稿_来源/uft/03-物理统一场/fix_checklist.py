# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\SUBMISSION_CHECKLIST.md"
with open(path, 'r', encoding='utf-8') as f:
    md = f.read()

repls = [
    ("alpha_S/alpha_W = 3.75 as a falsifiable prediction testable at",
     "alpha_S/alpha_W = 3.75 as a weak falsifiable prediction (7.4% deviation from independent experiment; best match alpha_S/alpha_EM = 15 at 0.6%) testable at"),

    ("The framework is 85% complete as a geometric\ninterpretation.",
     "The framework is 60-63% complete as a weak geometric\ninterpretation (3.75 prediction has 7.4% deviation, not 1.2% as earlier claimed)."),
]

count = 0
for old, new in repls:
    if old in md:
        md = md.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % repr(old[:50]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(md)

print("Replaced %d/%d" % (count, len(repls)))
