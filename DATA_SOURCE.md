# Data source & provenance — Noise in the Diagnosis of Epilepsy

## Paper
Nascimento FA, McLaren JR, Zhao W, … Westover MB. *Noise in the diagnosis of
epilepsy by experts.* Epileptic Disorders, 2026. PMID 41556879.

## Data (committed in this repo — de-identified)
All analysis data are small and committed directly (no external download):
- `Monkey2_Cases_Mastersheet_deID.xlsx` — the 50 de-identified patient vignettes (history, EEG/imaging results, clinical diagnosis). No names/MRNs/dates.
- `Monkey2_Responses_deID.xlsx` — the 20 experts' responses (Q1 history-only, Q2 final, QEEG) across two occasions.
- `dataQ1.csv`, `dataQ2.csv`, `dataQEEG.csv` — expert × case response matrices per question.
- `*_latent_effects.csv` — committed MCMC posterior summaries (per-observation latent effects), so figures regenerate without re-sampling.
- `Data.mat`, `Data_struct.mat`, `finalDx.mat` — MATLAB inputs for the summary-statistics script.

Experts and cases are anonymized (expert index / case index only). **PHI-scanned 2026-07-07: clean.**

## Raw → derived lineage
1. 20 epileptologists reviewed the 50 vignettes on two occasions → `Monkey2_Responses_deID.xlsx`.
2. `fcnGetData.m` / the notebook reshape responses into per-question matrices (`dataQ*.csv`).
3. `a0_Monkey2_Bayesian_v2.ipynb` fits the Bayesian hierarchical model → `*_latent_effects.csv` (the variance decomposition: signal / level / pattern / occasion noise).
4. Figures + summary stats are computed from (2)-(3).

No credentialed S3 dataset is required — the de-identified vignette/response data are entirely in-repo.
