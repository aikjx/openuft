"""
GitHub Repository Initialization Script
======================================
Run this AFTER creating the GitHub repo to push the files.

PREREQUISITES:
1. Create repo at: https://github.com/new
   - Name: perpendicular-mode-geometry
   - Public
   - No README (we already have one)

2. Install GitHub CLI:
   winget install GitHub.cli

3. Authenticate:
   gh auth login

USAGE:
  python github_init.py
"""
import os, subprocess, sys

REPO_URL = "https://github.com/algorithm-alliance/perpendicular-mode-geometry"
REPO_DIR = r"D:\a10\aikjx\code\my_lib\uft\arxiv"

print("=" * 60)
print("GitHub Repository Initialization")
print("=" * 60)
print()
print(f"Repository directory: {REPO_DIR}")
print(f"Remote URL: {REPO_URL}")
print()
print("Step 1: Check Git status")
print("-" * 40)

os.chdir(REPO_DIR)
if not os.path.exists(".git"):
    print("  Initializing git repo...")
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "remote", "add", "origin", REPO_URL], check=True)
    print("  Git initialized.")
else:
    print("  Git already initialized.")

print()
print("Step 2: Configure git (if needed)")
print("-" * 40)
try:
    name = subprocess.run(["git", "config", "user.name"],
                         capture_output=True, text=True).stdout.strip()
    email = subprocess.run(["git", "config", "user.email"],
                          capture_output=True, text=True).stdout.strip()
    if name:
        print(f"  User: {name} <{email}>")
    else:
        print("  WARNING: No git user configured.")
        print("  Run: git config --global user.name 'Your Name'")
        print("  Run: git config --global user.email 'you@example.com'")
except:
    print("  WARNING: git not available.")

print()
print("Step 3: Generate .gitignore (already exists)")
print("-" * 40)
if os.path.exists(".gitignore"):
    print("  .gitignore present.")

print()
print("Step 4: Stage all files")
print("-" * 40)
subprocess.run(["git", "add", "."], check=True)
result = subprocess.run(["git", "status", "--short"],
                       capture_output=True, text=True)
print("  Staged files:")
for line in result.stdout.strip().split("\n"):
    if line:
        print(f"    {line}")

print()
print("Step 5: Commit")
print("-" * 40)
commit_msg = """\
Initial commit: Perpendicular Mode Geometry of Four Forces

- Geometric unification of four fundamental forces
- Light helix perpendicular modes interpretation
- Gauge coupling ratio 15:4:1 prediction
- alpha_S/alpha_W = 3.75 falsifiable prediction
- Honest limitations: H1 (alpha), H3 (masses)

Framework: 85% complete geometric interpretation
"""
subprocess.run(["git", "commit", "-m", commit_msg], check=True)
print("  Committed.")

print()
print("Step 6: Push to GitHub")
print("-" * 40)
print(f"  Remote: {REPO_URL}")
print("  Command: git push -u origin main")
print()
print("  NOTE: Run 'gh auth login' first if not authenticated.")
print("  Then run: git push -u origin main")
print()
print("  If 'main' branch doesn't exist:")
print("    git branch -M main")
print("    git push -u origin main")

print()
print("=" * 60)
print("COMPLETED")
print("=" * 60)
print()
print("NEXT STEPS:")
print("1. Push: git push -u origin main")
print("2. Enable GitHub Actions (auto-runs tests)")
print("3. Enable GitHub Pages (for README)")
print("4. Create release v1.0.0")
print("5. Submit to arXiv")
