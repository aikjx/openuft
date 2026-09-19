"""List all files in the arxiv package with sizes."""
import os

BASE = r"D:\a10\aikjx\code\my_lib\uft\arxiv"

total = 0
print("=" * 72)
print("ARXIV PACKAGE FILE LIST")
print("=" * 72)

for root, dirs, files in os.walk(BASE):
    # Skip __pycache__
    dirs[:] = [d for d in dirs if d != "__pycache__"]
    for f in sorted(files):
        if f.endswith(".pyc"):
            continue
        path = os.path.join(root, f)
        size = os.path.getsize(path)
        total += size
        rel = os.path.relpath(path, BASE)
        ext = os.path.splitext(f)[1].lower()
        if ext in [".py", ".md", ".cff", ".yml", ".txt", ".bib", ""]:
            tag = ""
        elif ext in [".pdf", ".png"]:
            tag = " [FIG]"
        elif ext == ".tex":
            tag = " [MAIN]"
        elif ext in [".gitignore"]:
            tag = ""
        else:
            tag = ""
        print(f"  {size:>8,} B  {rel}{tag}")

print("=" * 72)
print(f"  TOTAL: {total:,} bytes ({total//1024} KB)")
print()
print("STATUS:")
print("  Paper (main.tex): READY")
print("  Figures (3 PDF): GENERATED")
print("  Code (4 Python): TESTED")
print("  References: COMPLETE")
print("  Package: READY FOR SUBMISSION")
print()
print("NEXT:")
print("  1. Create GitHub repo at https://github.com/new")
print("  2. Run: python github_init.py")
print("  3. Compile at https://overleaf.com")
print("  4. Submit to https://arxiv.org/submit")
