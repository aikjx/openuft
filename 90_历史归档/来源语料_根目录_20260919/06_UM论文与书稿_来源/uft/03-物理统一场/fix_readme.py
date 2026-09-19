# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\README.md"
with open(path, 'r', encoding='utf-8') as f:
    md = f.read()

repls = [
    # A. Key Prediction block (use actual +/- char)
    ("- **Experiment** (PDG 2024): 3.7959 \u00b1 0.0031\n"
     "- **Deviation**: 1.2% (within experimental error)",
     "- **Independent Experiment** (PDG 2024): 3.49 (using $\\alpha_2 = g_2^2/4\\pi = 0.0338$)\n"
     "- **Deviation**: 7.4% (NOTE: 3.7959 was circular via $\\alpha_W = 4\\alpha_{\\rm EM}$)"),

    # D_title
    ("## IMPORTANT CORRECTION",
     "## IMPORTANT CORRECTIONS"),

    # D2. Append E10 after retraction
    ("This claim is hereby\nexplicitly retracted.",
     "This claim is hereby explicitly retracted.\n\n"
     "### Correction 2: 3.75 prediction circular dependency\n\n"
     "Previous versions claimed $\\alpha_S/\\alpha_W = 3.75$ agrees with experiment\n"
     "$3.7959$ at 1.2% deviation. This is **ERRONEOUS**: the value $3.7959$ was computed\n"
     "circularly as $\\alpha_S/(4\\alpha_{\\rm EM})$, using the framework's own assumption\n"
     "$\\alpha_W = 4\\alpha_{\\rm EM}$. With independent $\\alpha_2(M_Z) = g_2^2/(4\\pi) = 0.0338$,\n"
     "the ratio is $3.49$ (7.4% deviation). The best-matching ratio is\n"
     "$\\alpha_S/\\alpha_{\\rm EM} = 15$ (0.6% deviation, trivial from assigned integer 15).\n"
     "This claim is hereby explicitly corrected."),
]

count = 0
for old, new in repls:
    if old in md:
        md = md.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % repr(old[:40]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(md)

print("Replaced %d/%d" % (count, len(repls)))
