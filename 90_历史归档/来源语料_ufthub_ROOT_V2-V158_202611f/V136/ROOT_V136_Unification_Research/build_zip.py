"""Build reproducible listing ZIP archive. No network required."""
import pathlib,hashlib,zipfile
root=pathlib.Path(__file__).resolve().parent
archive=root.parent/(root.name+'_Complete.zip')
manifest=root/'results'/'SHA256_SOURCES.txt'
paths=sorted(p for p in root.rglob('*') if p.is_file() and not any(c in ('__pycache__','.pytest_cache') for c in p.parts)
             and p.suffix not in ('.pyc',) and p!=manifest)
# Only immutable sources/documentation covered; regenerated results are intentionally excluded.
sourcepaths=[p for p in paths if 'results' not in p.relative_to(root).parts and 'figures' not in p.relative_to(root).parts]
manifest.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(root).as_posix()}\n' for p in sourcepaths),encoding='utf-8')
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(paths+[manifest]):
        z.write(p,f'{root.name}/{p.relative_to(root).as_posix()}')
with zipfile.ZipFile(archive) as z:
    bad=z.testzip()
    if bad:raise ValueError(f'ZIP member CRC issue: {bad}')
print('BUILT',archive,'FILES',len(paths)+1,'SIZE',archive.stat().st_size,'SHA256',hashlib.sha256(archive.read_bytes()).hexdigest())
