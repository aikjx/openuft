# ArXiv Submission Checklist

## Before Submission

### 1. Prepare Files
- [x] main.tex - Main paper (LaTeX, revtex4-2)
- [x] references.bib - Bibliography
- [x] figures/ - Diagrams (helix, four forces, coupling ratios)
- [ ] CITATION.cff - (run: python build_package.py)
- [ ] .gitignore
- [ ] LICENSE (MIT)
- [ ] Makefile
- [ ] code/verify_core.py
- [ ] code/gauge_couplings.py
- [ ] code/alpha_ratio.py
- [ ] requirements.txt
- [ ] README.md

### 2. Test Locally (requires LaTeX)
```bash
# Install LaTeX (Windows):
# Download from https://miktex.org/download
# Or: winget install MiKTeX.MiKTeX

# Build PDF
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Check output: main.pdf
```

### 3. Create arXiv Account
1. Go to https://arxiv.org
2. Click "Register for an account"
3. Use institutional email if possible (reduces spam)
4. Complete registration

### 4. Prepare Abstract
```
We propose that the four fundamental forces arise from four
perpendicular oscillation modes of a light-speed helix structure
in space. The electromagnetic, strong, weak, and gravitational
forces correspond respectively to the radial, tangential, chiral,
and axial modes of this geometry. The framework derives the gauge
coupling ratio alpha_S : alpha_W : alpha_EM = 15 : 4 : 1 from
integer coefficients on a unified base Phi_T^2 = 2^-7. We identify
alpha_S/alpha_W = 3.75 as a weak falsifiable prediction (7.4% deviation from independent experiment; best match alpha_S/alpha_EM = 15 at 0.6%) testable at
collider experiments. LIMITATION: The absolute value of alpha
(Phi_T^2 = 1/128 vs 1/137) cannot be derived from first principles
within this framework. The framework is 60-63% complete as a weak geometric
interpretation (3.75 prediction has 7.4% deviation, not 1.2% as earlier claimed).
```

### 5. Choose Subject Categories
Primary:   hep-th (High Energy Physics - Theory)
Secondary: physics.gen-ph (General Physics)

### 6. Comments / Notes
```
6 pages, 1 table. Code available at GitHub repository.
Honest acknowledgment of unsolved problems (H1: alpha absolute
value, H3: particle masses).
```

## During Submission

- [ ] Upload main.tex + references.bib + figures/
- [ ] Or upload main.tar.gz
- [ ] Set primary category: hep-th
- [ ] Set secondary category: physics.gen-ph
- [ ] Paste abstract
- [ ] Add comments
- [ ] Preview PDF
- [ ] Submit

## After Submission

- [ ] Note arXiv ID (e.g., 2608.XXXXX)
- [ ] Wait ~24h for processing
- [ ] Check for any issues
- [ ] Share link on social media / physics blogs
- [ ] Post to Twitter/X with paper link
- [ ] Consider posting to Physics StackExchange

## Alternative: Submit to Journal First

If preferring peer review before arXiv:

1. Submit to Foundations of Physics (easier acceptance)
2. If accepted → publish → arXiv with link
3. If rejected → still can post to arXiv

## Realistic Timeline

- Week 1: Install LaTeX, compile, fix errors
- Week 2: Create figures, finalize paper
- Week 3: Create GitHub repo, test code
- Week 4: Register arXiv, submit
- Week 5-8: Wait for feedback, respond

## If LaTeX Not Available

Options:
1. Install MiKTeX: https://miktex.org/download
2. Use Overleaf (browser-based, free): https://overleaf.com
3. Upload main.tex to Overleaf, compile there
4. Download compiled PDF, upload to arXiv

Overleaf is EASIEST if no local LaTeX.
