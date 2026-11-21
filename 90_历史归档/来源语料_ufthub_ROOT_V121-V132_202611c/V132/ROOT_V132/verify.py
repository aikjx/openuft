"""ROOT V132 acceptance. No web and no modifications to external systems."""
from pathlib import Path
import subprocess,sys,hashlib,zipfile,json,math
p=Path(__file__).resolve().parent

def run(*args):
 r=subprocess.run([sys.executable,*args],cwd=p,capture_output=True,text=True)
 if r.returncode:
  raise RuntimeError(f'failed: {args}\n{r.stdout}\n{r.stderr}')
 return r.stdout+r.stderr

if __name__=='__main__':
 print('V132 verify: c=1, retaining hbar and G')
 summary=run('-m','unittest','discover','-s','tests','-v')
 assert 'Ran 43 tests' in summary and 'OK' in summary
 print('43 tests: PASS; random properties 2000+500')
 symbol=run('scripts/symbolic_audit.py')
 assert 'Pass: all symbolic checks.' in symbol
 print('SymPy independent derivation: PASS')
 j=json.loads((p/'data/calculation_results.json').read_text())
 assert abs(j['alpha']-1/137.035999177)<1e-16
 assert abs(j['boosted_example']['u_after_boost']+0.5953091559129513)<1e-12
 book=p/'book/ROOT_V132_空间螺旋与量子常数_研究专著_第一卷.md'
 assert len(book.read_text()) > 22000
 html=(p/'book/ROOT_V132_研究专著_第一卷.html').read_text()
 assert html.count('<math')>=200
 with zipfile.ZipFile(p/'book/ROOT_V132_研究专著_第一卷.epub') as z:
  assert z.testzip() is None
  assert len([k for k in z.namelist() if k.endswith('.png')])==4
 with zipfile.ZipFile(p/'history/ROOT_V131_原始科研归档.zip') as z:
  assert z.testzip() is None
 print('book, HTML, EPUB, data, preserved historical ZIP: PASS')
 hashes=(p/'SHA256SUMS.txt').read_text().splitlines()
 count=0
 for line in hashes:
  if not line.strip():continue
  digest,relative=line.split('  ',1)
  candidate=p/relative
  assert candidate.is_file(),relative
  h=hashlib.sha256(candidate.read_bytes()).hexdigest()
  assert h==digest,relative
  count+=1
 print('SHA-256 files verified:',count)
 print('V132 acceptance: PASS')
