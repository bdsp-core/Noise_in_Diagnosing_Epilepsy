# Noise in Medical Decision Making - LaTeX Manuscript

## Main Files
- `kilt_main.tex` - Main LaTeX document
- `wiley-article.cls` - Wiley article document class
- `LICENSE`, `LICENSE.txt` - Project licenses

## Directory Structure

### `sections/`
LaTeX source files for each section of the paper:
- `01_introduction.tex`
- `02_methods.tex`
- `03_case_study.tex`
- `04_discussion.tex`
- `05_conclusion.tex`
- `appendix_A_bayesian.tex`
- `appendix_B_practical.tex`
- `99_backmatter.tex`

### `bibliography/`
BibTeX bibliography files

### `code/`
Python scripts, Jupyter notebooks, MATLAB code, and shell scripts:
- Analysis scripts (`noise_analysis_lib.py`, `noise_decomposition_flexible.py`)
- Figure generation (`generate_killer_figure_v5.py`)
- Case studies (`case_study_spikes.py`, `spikes_descriptive_analysis.py`)
- Utility scripts (`calculate_kappa.py`, `check_latex_errors.py`)
- Notebooks (`a0_Monkey2_Bayesian_v2.ipynb`)
- Environment setup (`setup_environment.sh`, `fix_*.sh`)
- Output directories (`spikes_analysis_output/`, `__pycache__/`)

### `data/`
Data files for analysis:
- CSV files (`dataQ1.csv`, `dataQ2.csv`, `dataQEEG.csv`, etc.)
- MATLAB data files (`Data_struct.mat`, `finalDx.mat`)
- Excel spreadsheets (`Monkey2_*.xlsx`)

### `figures/`
Additional figures and matrices not directly used in the paper:
- Matrix visualizations (`matrix_c.png`, `matrix_l.png`, etc.)
- Unused figures (`Figure2.png`)

### `docs/`
Documentation and reference materials:
- Setup guides (`ENVIRONMENT_SETUP.md`, `README_LATEX_STRUCTURE.md`)
- Analysis summaries (`SPIKES_ANALYSIS_README.md`, `FLEXIBLE_CODE_SUMMARY.md`)
- Development notes (`KILLER_FIGURE_*.md`, `IMPROVEMENTS_SUMMARY.md`)
- Reference papers (`nitish-paper.pdf`, `M2-Supplemental-NoiseTypesEstimation_Bayesian.pdf`)
- Annotated manuscript (`Noise_And_Skill_SiM_1.29-fabs.pdf`)
- Office documents (`ms_12.29-mbw.docx`, `Noise-Methods-Figures.pptx`)
- Test files (`test_*.tex`, `test_*.pdf`)

### `aux_files/`
LaTeX auxiliary files (auto-generated during compilation):
- `.aux`, `.log`, `.bbl`, `.blg`, `.fdb_latexmk`, `.fls`, `.out`

### `old/`
Archived files from previous versions

## Figures Used in Paper
These files remain in the root directory for easy LaTeX access:
- `Fig1-Noise-Model.png`
- `Figure3.png`
- `KSS-Model.png`
- `SSIT-ROCs.png`
- `killer_figure.pdf`
- `posterior_predictive_checks.png`

## Compilation
To compile the paper:
```bash
pdflatex kilt_main.tex
bibtex kilt_main
pdflatex kilt_main.tex
pdflatex kilt_main.tex
```

Or with synctex for PDF-LaTeX synchronization:
```bash
pdflatex -synctex=1 kilt_main.tex
```
