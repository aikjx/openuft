import os

path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\main.tex"
with open(path, 'r', encoding='utf-8') as f:
    tex = f.read()

repls = [
    # A. Abstract
    (r"experiment: $3.7959$, deviation 1.2\%",
     r"independent experiment: $3.49$, deviation 7.4\% (circular $3.7959$ retracted)"),

    # B. Introduction - value line
    (r"the experimental value of $3.7959 \pm 0.0031$ (PDG 2024) ---",
     r"independent values $\alpha_S(M_Z)=0.1179$ and $\alpha_2(M_Z)=0.0338$ ---"),

    # B2. Introduction - deviation line
    (r"a deviation of 1.2\%, within experimental error.",
     r"a deviation of 7.4\%. (The quoted $3.7959$ used circular definition $\alpha_W=4\alpha_{\rm EM}$.)"),

    # C. Table row 1
    (r"$\alpha_S/\alpha_W$ & 3.7500 & $3.7959 \pm 0.0031$ & 1.2\% \\",
     r"$\alpha_S/\alpha_W$ & 3.7500 & $3.49$ & 7.4\% \\"),

    # C2. Table row 2
    (r"$\alpha_S/\alpha_{\rm EM}$ & 15.00 & 16.16 & 7.2\% \\",
     r"$\alpha_S/\alpha_{\rm EM}$ & 15.00 & 15.09 & 0.6\% \\"),

    # C3. Table row 3
    (r"$\alpha_W/\alpha_{\rm EM}$ & 4.000 & 4.257 & 6.4\% \\",
     r"$\alpha_W/\alpha_{\rm EM}$ & 4.000 & 4.32 & 8.1\% \\"),

    # D. Table caption text
    (r"differs from experiment\nby 1.2\%, which is within the current experimental uncertainty.",
     r"differs from the independent experiment\nby 7.4\%. The value $3.7959$ used a circular definition $\alpha_W=4\alpha_{\rm EM}$."),

    # D2. "6--7%" -> "6--8%"
    (r"so the other ratios deviate by 6--7\%.",
     r"so $\alpha_S/\alpha_{\rm EM}$ matches (0.6\%) but $\alpha_W/\alpha_{\rm EM}$ deviates by 8.1\%."),

    # E. Testability
    (r"$\alpha_S/\alpha_W = 3.75 \pm 0.004$, the framework is supported.",
     r"$\alpha_S/\alpha_W = 3.75$ constant across scales, the framework is supported."),

    # F. Discussion
    (r"One falsifiable prediction: $\alpha_S/\alpha_W = 3.75$ (from assigned integers).",
     r"A weak falsifiable prediction: $\alpha_S/\alpha_W = 3.75$ (7.4\% deviation from independent experiment; best match is $\alpha_S/\alpha_{\rm EM}=15$ at 0.6\%)."),

    # G. Conclusion
    (r"(current experimental value: $3.7959 \pm 0.0031$).",
     r"(independent experiment: $3.49$, deviation 7.4\%; the value $3.7959$ was circular)."),
]

count = 0
for old, new in repls:
    if old in tex:
        tex = tex.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % old[:60])

with open(path, 'w', encoding='utf-8') as f:
    f.write(tex)

print("Replaced %d/%d patterns" % (count, len(repls)))
print("File: %s" % path)
