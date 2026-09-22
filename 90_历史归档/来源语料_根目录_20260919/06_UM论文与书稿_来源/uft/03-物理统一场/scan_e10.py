import os, re

base = r"D:\a10\aikjx\code\my_lib\uft"

patterns = [
    r'3\.7959',
    r'偏差\s*1\.2',
    r'偏差\s*1\.21',
    r'1\.2%',
    r'alpha_S/alpha_W\s*=\s*3\.75',
    r'3\.75\s*预测',
    r'3\.75\s*现象',
    r'唯一.*预测',
    r'only.*predict',
]

results = []
for root, dirs, files in os.walk(base):
    if 'figures' in root:
        continue
    for fn in files:
        if not (fn.endswith('.md') or fn.endswith('.txt') or fn.endswith('.tex')):
            continue
        full = os.path.join(root, fn)
        try:
            with open(full, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except:
            continue
        for i, line in enumerate(lines, 1):
            for pat in patterns:
                if re.search(pat, line, re.IGNORECASE):
                    rel = os.path.relpath(full, base)
                    results.append((rel, i, line.strip()[:90]))
                    break

with open('scan_result.txt', 'w', encoding='utf-8') as f:
    f.write("=== FILES WITH 3.75 / FALSE CLAIM REFERENCES ===\n")
    f.write("Total matches: %d\n\n" % len(results))
    for rel, ln, text in results:
        f.write("(%s:%d) %s\n" % (rel, ln, text))
