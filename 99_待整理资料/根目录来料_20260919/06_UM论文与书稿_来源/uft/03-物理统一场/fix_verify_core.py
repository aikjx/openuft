# -*- coding: utf-8 -*-
path = r"D:\a10\aikjx\code\my_lib\uft\arxiv\code\verify_core.py"
with open(path, 'r', encoding='utf-8') as f:
    code = f.read()

repls = [
    # A. Circular alpha_W_exp -> independent alpha_2
    ("alpha_W_exp = mp.mpf('0.03106')",
     "alpha_W_exp = mp.mpf('0.0338')  # INDEPENDENT alpha_2(M_Z)=g_2^2/4pi. "
     "NOTE: older 0.03106 = 4*alpha_EM (circular, see E10)"),

    # B. [E] section comment
    ("print(\"  [E] alpha_S/alpha_W = 3.75\")\n"
     "ratio_geom = alpha_S_geom / alpha_W_geom\n"
     "ratio_exp = alpha_S_exp / alpha_W_exp\n"
     "print(f\"      ratio_geom = {ratio_geom:.8f} (15/4)\")\n"
     "print(f\"      ratio_exp  = {ratio_exp:.8f}\")\n"
     "rel = abs(ratio_geom - ratio_exp) / ratio_exp\n"
     "verify(\"alpha_S/alpha_W = 3.75\", ratio_geom, ratio_exp, rel_err=rel)",
     "print(\"  [E] alpha_S/alpha_W = 3.75 (assigned integers)\")\n"
     "ratio_geom = alpha_S_geom / alpha_W_geom\n"
     "ratio_exp = alpha_S_exp / alpha_W_exp  # now INDEPENDENT alpha_2=0.0338\n"
     "print(f\"      ratio_geom = {ratio_geom:.8f} (15/4)\")\n"
     "print(f\"      ratio_exp  = {ratio_exp:.8f}  (INDEPENDENT: alpha_2=0.0338)\")\n"
     "rel = abs(ratio_geom - ratio_exp) / ratio_exp\n"
     "verify(\"alpha_S/alpha_W = 3.75 (weak, 7.4% dev)\", ratio_geom, ratio_exp, rel_err=rel)\n"
     "print(\"  NOTE (E10): older 1.2% used circular alpha_W=4*alpha_EM=0.03106; retracted.\")\n"
     "print(\"  Best match is alpha_S/alpha_EM=15 (0.6%, trivial integer ratio).\")\n"),

    # C1. Summary line 1
    ('print("  [E] alpha_S/alpha_W = 3.75 -- OK (1.2% from exp)")',
     'print("  [E] alpha_S/alpha_W = 3.75 -- WEAK (7.4% dev from independent exp; 1.2% was circular)")'),

    # C2. Summary line 2
    ('print("  Framework is 85% complete as geometric interpretation.")',
     'print("  Framework is 60-63% complete as WEAK geometric interpretation (E10 retraction).")'),

    # C3. Summary line 3
    ('print("  Only alpha_S/alpha_W = 3.75 is a genuine falsifiable prediction.")',
     'print("  Best match: alpha_S/alpha_EM=15 (0.6%, trivial). 3.75 prediction: 7.4% dev (E10).")'),
]

count = 0
for old, new in repls:
    if old in code:
        code = code.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND: %s" % repr(old[:50]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(code)

print("Replaced %d/%d" % (count, len(repls)))

# Test run
import subprocess
r = subprocess.run(["python", path], capture_output=True, text=True, encoding='utf-8',
                   cwd=r"D:\a10\aikjx\code\my_lib\uft\arxiv\code")
print("=== TEST RUN ===")
print(r.stdout[-1500:])
print(r.stderr[-500:])
