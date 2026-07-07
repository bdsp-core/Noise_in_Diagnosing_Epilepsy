# Noise in Diagnosing Epilepsy


## Published on bdsp.io

- **Project:** https://bdsp.io/content/61d040ynxbnnerpvbnt8/1.0.0/
- **DOIs:** [10.60508/zhep-m488](https://doi.org/10.60508/zhep-m488) (v1.0.0) · [10.60508/rjkx-x640](https://doi.org/10.60508/rjkx-x640) (core)
- **Paper:** Nascimento FA, et al. *Noise in the diagnosis of epilepsy by experts.* Epileptic Disorders 2026. [10.1002/epd2.70181](https://doi.org/10.1002/epd2.70181)


Code and data accompanying our paper on inter- and intra-rater noise in the diagnosis of epilepsy. The analysis decomposes variability in expert diagnostic judgments into interpretable components — signal, between-expert bias, expert-by-case interaction, and within-expert inconsistency — using a Bayesian hierarchical model, and computes supporting summary agreement statistics.

## Study design

Twenty epileptologists independently reviewed the same 50 de-identified patient vignettes on two separate occasions (test-retest), answering:

- **Q1** — Based on history alone, is this epilepsy? *(yes / order EEG / no)*
- **Q2** — Final diagnosis: epilepsy? *(yes / no, with EEG and imaging results revealed when requested)*
- **QEEG** — Would you order an EEG?

The paired readings let us separate noise that varies *between* experts (some raters systematically more likely to diagnose epilepsy) from noise that varies *within* experts across occasions (the same rater giving different answers to the same case), and to identify expert-by-case interactions (disagreements that are specific to particular case/rater pairings).

## What's in this repo

### Analysis code

- **[a0_Monkey2_Bayesian_v2.ipynb](a0_Monkey2_Bayesian_v2.ipynb)** — Main analysis. Fits the Bayesian hierarchical model (PyMC / NumPyro NUTS), computes the variance decomposition, saves per-observation posterior means of the latent effects, and produces the paper's figures.
- **[a1_MakeSummaryStats.m](a1_MakeSummaryStats.m)** — MATLAB script computing descriptive statistics: per-case and per-expert yes/no/EEG rates, mind-changing frequency, agreement with consensus, agreement with clinical diagnosis, correlations with years of experience, and EEG-ordering effects.
- **[fcnGetData.m](fcnGetData.m)** — Helper that reshapes the raw response tables into expert × case matrices for each question and time point.

### The model

For each question (Q1, Q2, QEEG) we model the log-odds of a "yes" response on trial $(i, j, t)$ — expert $i$, case $j$, occasion $t$ — as

$$\text{logit}(P_{ijt}) = \mu + c_j + l_i + p_{ij} + o_{ijt}$$

with non-centered priors

- $c_j \sim \mathcal{N}(0, \sigma_c^2)$ — **case signal** (what the case actually is)
- $l_i \sim \mathcal{N}(0, \sigma_l^2)$ — **level noise** (expert's baseline tendency)
- $p_{ij} \sim \mathcal{N}(0, \sigma_p^2)$ — **pattern noise** (expert × case interaction)
- $o_{ijt} \sim \mathcal{N}(0, \sigma_o^2)$ — **occasion noise** (within-expert inconsistency)

Variance is decomposed by reporting each component's share of the total $\sigma_c^2 + \sigma_l^2 + \sigma_p^2 + \sigma_o^2$. Derivation of this decomposition is in [M2-Supplemental-NoiseTypesEstimation_Bayesian.pdf](M2-Supplemental-NoiseTypesEstimation_Bayesian.pdf).

Sampling: 10 chains × 5,000 draws (2,000 tuning), `target_accept = 0.98`, `random_seed = 42`.

### Data

**Tidy inputs to the Bayesian model** (long format: `id`, `item`, `t`, `Y`):

- [dataQ1.csv](dataQ1.csv) — history-only diagnosis responses
- [dataQ2.csv](dataQ2.csv) — final diagnosis responses
- [dataQEEG.csv](dataQEEG.csv) — "order an EEG?" responses

**Posterior mean latent effects** (one row per observation, columns `i, j, t, c, l, p, o`):

- [dataQ1_latent_effects.csv](dataQ1_latent_effects.csv), [dataQ2_latent_effects.csv](dataQ2_latent_effects.csv), [dataQEEG_latent_effects.csv](dataQEEG_latent_effects.csv)
- [joint_dataQ1_dataQ2_latent_effects.csv](joint_dataQ1_dataQ2_latent_effects.csv) — joint fit across Q1 and Q2

**Raw / intermediate** (consumed by the MATLAB script):

- [Data.mat](Data.mat), [Data_struct.mat](Data_struct.mat) — expert response tables `T1`, `T2` and case difficulty
- [finalDx.mat](finalDx.mat) — independent clinical gold-standard diagnoses
- [Monkey2_Cases_Mastersheet_deID.xlsx](Monkey2_Cases_Mastersheet_deID.xlsx) — de-identified case metadata
- [Monkey2_Responses_deID.xlsx](Monkey2_Responses_deID.xlsx) — de-identified expert responses

### Figures

- [Figure2.png](Figure2.png), [Figure3.png](Figure3.png) — main paper figures
- [matrix_c.png](matrix_c.png), [matrix_l.png](matrix_l.png), [matrix_p.png](matrix_p.png), [matrix_o1.png](matrix_o1.png), [matrix_o2.png](matrix_o2.png) — latent-effect heatmaps sorted by case signal and expert level

## Reproducing the results

### Bayesian analysis (Python)

Requires Python 3.10+ with PyMC, ArviZ, NumPyro, NumPy, Pandas, Matplotlib, SciPy.

```bash
pip install pymc arviz numpyro pandas matplotlib scipy jupyter
jupyter lab a0_Monkey2_Bayesian_v2.ipynb
```

Running all cells will:
1. Fit the hierarchical model to `dataQ1.csv`, `dataQ2.csv`, `dataQEEG.csv`.
2. Write `*_latent_effects.csv` files with posterior-mean random effects.
3. Produce the latent-effect heatmaps and Gaussian-fit panels used in Figures 2–3.

Sampling takes roughly tens of minutes per question on a modern CPU (10 chains, 6 cores).

### Summary statistics (MATLAB)

```matlab
a1_MakeSummaryStats
```

Reads `Data.mat` and `finalDx.mat` and prints the descriptive numbers reported in the text (agreement rates, mind-changing counts, consistency-vs-accuracy correlations, EEG-ordering effects, etc.).

## Citation

If you use this code or data, please cite the accompanying paper.

## License

See [LICENSE](LICENSE) / [LICENSE.txt](LICENSE.txt).
