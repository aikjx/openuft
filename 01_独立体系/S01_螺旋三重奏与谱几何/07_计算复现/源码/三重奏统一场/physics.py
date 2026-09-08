# Shared historical constants; no independent copy.
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "02_共享基础" / "公共计算" / "源码").is_dir())
sys.path.insert(0, str(ROOT / "02_共享基础" / "公共计算" / "源码"))
from physics_constants import *
