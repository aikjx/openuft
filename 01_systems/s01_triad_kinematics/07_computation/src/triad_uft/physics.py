# Shared historical constants; no independent copy.
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_shared" / "computation" / "src").is_dir())
sys.path.insert(0, str(ROOT / "02_shared" / "computation" / "src"))
from physics_constants import *
