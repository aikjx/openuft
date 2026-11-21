from pathlib import Path
import hashlib
root=Path(__file__).resolve().parent
entries=[x.strip().split('  ',1) for x in (root/'MANIFEST.sha256').read_text(encoding='utf-8').splitlines() if x.strip()]
for digest,rel in entries:
    p=(root/rel).resolve()
    assert p.is_relative_to(root) and p.is_file(),f'missing or unsafe: {rel}'
    current=hashlib.sha256(p.read_bytes()).hexdigest()
    assert current==digest,f'checksum mismatch: {rel}'
print(f'ROOT_V127_MANIFEST_OK {len(entries)} files')
