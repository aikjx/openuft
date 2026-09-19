import os

base = r"D:\a10\aikjx\code\my_lib\uft"
files = sorted([f for f in os.listdir(base) if f.startswith('__') and f.endswith('.md')])
total = 0
out = []
for f in files:
    sz = os.path.getsize(os.path.join(base, f))
    total += sz
    out.append("%-52s %8d B" % (f, sz))
out.append("---")
out.append("Total: %d files, %d bytes (%.1f KB)" % (len(files), total, total/1024))

# Also list arxiv package
arxiv_dir = os.path.join(base, "arxiv")
out.append("\n=== arxiv package ===")
for root, dirs, fs in os.walk(arxiv_dir):
    for fn in sorted(fs):
        full = os.path.join(root, fn)
        rel = os.path.relpath(full, base)
        out.append("%-52s %8d B" % (rel, os.path.getsize(full)))

# Also list 03-物理统一场 scripts
out.append("\n=== 03-物理统一场 scripts ===")
phys = os.path.join(base, "03-物理统一场")
for fn in sorted(os.listdir(phys)):
    if fn.endswith('.py'):
        full = os.path.join(phys, fn)
        out.append("%-52s %8d B" % (fn, os.path.getsize(full)))

print("\n".join(out))
