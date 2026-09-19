#!/usr/bin/env python3
"""Build complete arXiv submission package."""
import os, tarfile

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "submission_package")

os.makedirs(OUT, exist_ok=True)

# Files to include in tar.gz
tex_files = ["main.tex", "references.bib"]
fig_dir = "figures"
code_dir = "code"

print("Building submission package...")

# Copy files
for f in tex_files:
    src = os.path.join(BASE, f)
    if os.path.exists(src):
        import shutil
        shutil.copy(src, OUT)
        print(f"  + {f}")
    else:
        print(f"  MISSING: {f}")

if os.path.exists(os.path.join(BASE, fig_dir)):
    fig_out = os.path.join(OUT, fig_dir)
    os.makedirs(fig_out, exist_ok=True)
    import shutil
    shutil.copytree(os.path.join(BASE, fig_dir), fig_out, dirs_exist_ok=True)
    print(f"  + {fig_dir}/")

if os.path.exists(os.path.join(BASE, code_dir)):
    code_out = os.path.join(OUT, code_dir)
    os.makedirs(code_out, exist_ok=True)
    import shutil
    shutil.copytree(os.path.join(BASE, code_dir), code_out, dirs_exist_ok=True)
    print(f"  + {code_dir}/")

# Create tar.gz
tar_name = os.path.join(BASE, "perpendicular_mode_geometry.tar.gz")
with tarfile.open(tar_name, "w:gz") as tar:
    tar.add(OUT, arcname="perpendicular_mode_geometry")

print(f"\nPackage created: {tar_name}")
print(f"Size: {os.path.getsize(tar_name)/1024:.1f} KB")
print()
print("Next steps:")
print("1. Install LaTeX or use Overleaf to compile main.tex")
print("2. Register at https://arxiv.org")
print("3. Submit perpendicular_mode_geometry.tar.gz")
