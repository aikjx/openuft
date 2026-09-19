# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\code\verify_core.py"
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

repls = [
    ('print("  PREDICTIONS (testable):")',
     'print("  MATCHES (weak, E10 corrected):")'),
    ('print("    [E] alpha_S/alpha_W = 3.75 -- OK (1.2% from exp)")',
     'print("    [E] alpha_S/alpha_W = 3.75 -- WEAK (7.4% dev, 1.2% circular retracted)")'),
]

count = 0
for old, new in repls:
    if old in code:
        code = code.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % repr(old[:50]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Replaced %d/%d" % (count, len(repls)))

import subprocess
r = subprocess.run(["python", path], capture_output=True, text=True, encoding='utf-8',
                   cwd=r"D:\a10\aikjx\code\my_lib\uft\arxiv\code")
print("=== SUMMARY SECTION ===")
# Extract summary
out = r.stdout
idx = out.find("SUMMARY")
print(out[idx:idx+800])
