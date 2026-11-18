"""Verify the manifest in an extracted ROOT V67 directory."""
import hashlib,sys
from pathlib import Path
r=Path(__file__).resolve().parent
manifest=r/'FILE_SHA256_MANIFEST.txt'
if not manifest.exists():print('manifest missing');sys.exit(1)
checked=0;errors=[]
for line in manifest.read_text(encoding='utf-8').splitlines():
    if not line.strip() or line.startswith('#'):continue
    expected,rel=line.split('  ',1)
    p=r/rel
    if not p.is_file():errors.append('MISSING: '+rel);continue
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    if expected!=actual:errors.append('MODIFIED: '+rel)
    checked+=1
print('Verified',checked,'files; errors',len(errors))
for x in errors:print(x)
sys.exit(0 if not errors else 1)
