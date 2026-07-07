# Reproduce — Noise in the Diagnosis of Epilepsy (Nascimento et al., Epileptic Disorders 2026)

All data are **committed and de-identified** (patient vignettes + expert responses;
no PHI). Two tiers:

## 1. Figures from committed model outputs (fast — verified 2026-07-07)
The MCMC posterior summaries are committed (`*_latent_effects.csv`), so the figures
regenerate without re-running the sampler:

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute a0_Monkey2_Bayesian_v2.ipynb
```
Regenerates `Figure2.png`, `Figure3.png`, and the variance-component matrices
(`matrix_c/l/p/o1/o2.png`) from `dataQ1/Q2/QEEG_latent_effects.csv`.

## 2. Full Bayesian model from scratch (re-run MCMC)
The first cell of `a0_Monkey2_Bayesian_v2.ipynb` fits the hierarchical model
(PyMC NUTS) on `dataQ1.csv` / `dataQ2.csv` / `dataQEEG.csv`, writing the
`*_latent_effects.csv`. Re-run it to reproduce the variance decomposition end-to-end
(minutes on CPU; the dataset is 20 experts × 50 cases × 2 occasions).

## Summary statistics (MATLAB)
`a1_MakeSummaryStats.m` (uses `fcnGetData.m`, `Data.mat`) computes the descriptive
agreement statistics (per-case/per-expert rates, mind-changing, consensus/clinical
agreement, experience correlations).

| Paper item | Script | Input (committed) | Output |
|---|---|---|---|
| Figure 2 (variance decomposition) | `a0_…ipynb` | `*_latent_effects.csv` | `Figure2.png` |
| Figure 3 | `a0_…ipynb` | `dataQ2_latent_effects.csv` | `Figure3.png` |
| Component matrices | `a0_…ipynb` | `*_latent_effects.csv` | `matrix_*.png` |
| Summary agreement stats | `a1_MakeSummaryStats.m` | `Data.mat` | stdout |

## Requirements
Python 3.10+ (`requirements.txt`: pymc, arviz, numpy, pandas, scipy, matplotlib, openpyxl); MATLAB for the summary stats. See `DATA_SOURCE.md`.
