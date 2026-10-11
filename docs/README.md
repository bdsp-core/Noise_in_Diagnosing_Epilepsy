# Noise Decomposition in Clinical Diagnosis: Code Repository

Code and data to reproduce results from our paper on noise decomposition in the diagnosis of epilepsy using the Kahneman-Sibony-Sunstein (KSS) framework.

## Overview

This repository implements a Bayesian hierarchical modeling approach to decompose disagreement among clinical experts into distinct sources:
- **Signal (S)**: True variation across cases (case difficulty)
- **Level Noise (LN)**: Rater bias (systematic over/under-calling)
- **Pattern Noise (PN)**: Idiosyncratic rater-case interactions
- **Occasion Noise (ON)**: Within-rater inconsistency over time

## Files

### Core Analysis
- **[a0_Monkey2_Bayesian_v2.ipynb](a0_Monkey2_Bayesian_v2.ipynb)**: Original analysis notebook
  - Fits full KSS model (all four variance components)
  - Generates publication figures (Figure 2, Figure 3)
  - Exports estimated latent effects to CSV

- **[noise_decomposition_flexible.py](noise_decomposition_flexible.py)**: **NEW - Flexible Python script with model selection**
  - Supports three model types: IRT, SSIT, or KSS
  - Configurable via `model_type` parameter
  - Can run from command line or import as module
  - Includes `compare_models()` function to fit all three models at once

- **[example_usage.py](example_usage.py)**: Example script demonstrating the flexible framework
  - Shows how to fit single models
  - Shows how to compare all three models
  - Demonstrates post-hoc variance combination
  - Creates visualization comparing models

### Summary Statistics
- **a1_MakeSummaryStats.m**: MATLAB script for computing summary statistics

### Data Files
The notebook expects CSV files with the following structure:
```
id,item,t,Y
1,1,1,0
1,2,1,1
...
```

Where:
- `id`: Rater/expert identifier (1 to M)
- `item`: Case identifier (1 to N)
- `t`: Occasion identifier (1 to T)
- `Y`: Binary response (0 or 1)

Example datasets used in the notebook:
- `dataQ1.csv`: Question 1 responses (20 experts × 50 cases × 2 occasions = 2000 observations)
- `dataQ2.csv`: Question 2 responses (20 experts × 50 cases × 2 occasions = 2000 observations)
- `dataQEEG.csv`: QEEG responses (20 experts × 50 cases × 2 occasions = 2000 observations)

## Model Details

### Full KSS Model (Default)

The notebook fits the complete model:

```
Y_ijt ~ Bernoulli(π_ijt)
logit(π_ijt) = c_i + ℓ_j + p_ij + o_ijt + ȳ
```

Where:
- `c_i ~ Normal(0, σ_c²)`: Case effects (signal)
- `ℓ_j ~ Normal(0, σ_l²)`: Rater effects (level noise)
- `p_ij ~ Normal(0, σ_p²)`: Rater-case interactions (pattern noise)
- `o_ijt ~ Normal(0, σ_o²)`: Observation-level effects (occasion noise)
- `ȳ`: Grand mean (intercept)

### Priors

All scale parameters use weakly informative priors:
```python
sigma_c = pm.HalfNormal("sigma_c", sigma=1)
sigma_l = pm.HalfNormal("sigma_l", sigma=1)
sigma_p = pm.HalfNormal("sigma_p", sigma=1)
sigma_o = pm.HalfNormal("sigma_o", sigma=1)
intercept = pm.Normal("intercept", mu=0, sigma=10)
```

### Estimation

- **Sampler**: NUTS (No-U-Turn Sampler) via NumPyro backend
- **Chains**: 10 independent chains
- **Draws**: 5000 per chain (after 2000 tuning iterations)
- **Parameterization**: Non-centered for all latent variables (improves sampling efficiency)
- **Target acceptance**: 0.98 (high to ensure good exploration)

### Convergence Diagnostics

The notebook reports:
- **R-hat**: Should be < 1.01 (values shown are all 1.0 ✓)
- **ESS (effective sample size)**: Should be > 1000 for reliable inference
- **MCSE (Monte Carlo standard error)**: Quantifies uncertainty in posterior estimates

## Frequently Asked Questions

### 1. Can I use this code with T=1 (single occasion)?

**YES**, but with important caveats:

- When T=1, **occasion noise becomes unidentifiable** because there's no within-rater replication
- The model will still run and estimate σ_o, but it will shrink toward zero with high uncertainty
- **Practically, you get the SSIT model** where pattern and occasion noise are confounded

**What you'll observe with T=1:**
```
Variance Decomposition:
  Signal (S):           ~60-70%
  Level Noise (LN):     ~20-30%
  Pattern Noise (PN):   ~5-10%
  Occasion Noise (ON):  ~0-5%  ← Will be near zero with wide credible intervals
```

**Recommendation for T=1:**
- Run the full model as-is
- Report the results as measuring Signal, Level Noise, and "Pattern + Occasion Noise" (combined)
- Alternatively, modify the code to set σ_o = 0 (see Option 2 below)

### 2. Can I estimate just "Level Noise + Other Noise"?

**YES**, you have two options:

#### Option 1: Post-hoc Aggregation (Easiest)

Run the full model, then combine variance components:

```python
# After running the analysis
var_l = np.mean(sigma_l_samples ** 2)
var_p = np.mean(sigma_p_samples ** 2)
var_o = np.mean(sigma_o_samples ** 2)

# Combine pattern and occasion into "other noise"
var_other = var_p + var_o
other_noise = np.sqrt(var_other)

print(f"Level Noise: {np.sqrt(var_l):.2f}")
print(f"Other Noise (PN + ON): {other_noise:.2f}")
```

#### Option 2: Model Modification (More Principled)

Modify the model definition to collapse components:

**To get IRT model (Level Noise only, no Pattern/Occasion):**
```python
# In the model definition, comment out pattern and occasion terms:
with pm.Model() as model:
    sigma_c = pm.HalfNormal("sigma_c", sigma=1)
    sigma_l = pm.HalfNormal("sigma_l", sigma=1)
    # sigma_p = pm.HalfNormal("sigma_p", sigma=1)  # COMMENTED OUT
    # sigma_o = pm.HalfNormal("sigma_o", sigma=1)  # COMMENTED OUT
    intercept = pm.Normal("intercept", mu=0, sigma=10)

    z_c = pm.Normal("z_c", mu=0, sigma=1, shape=n_cases)
    c = pm.Deterministic("c", z_c * sigma_c)

    z_l = pm.Normal("z_l", mu=0, sigma=1, shape=n_experts)
    l = pm.Deterministic("l", z_l * sigma_l)

    # Linear predictor (no p or o terms)
    z = intercept + c[data['case_idx'].values] + l[data['expert_idx'].values]

    y_obs = pm.Bernoulli("y_obs", logit_p=z, observed=data['Y'].values)
```

**To get Level Noise + "Other Noise" (single aggregated term):**
```python
# Replace pattern and occasion with a single residual term
with pm.Model() as model:
    sigma_c = pm.HalfNormal("sigma_c", sigma=1)
    sigma_l = pm.HalfNormal("sigma_l", sigma=1)
    sigma_residual = pm.HalfNormal("sigma_residual", sigma=1)  # Combines PN + ON
    intercept = pm.Normal("intercept", mu=0, sigma=10)

    z_c = pm.Normal("z_c", mu=0, sigma=1, shape=n_cases)
    c = pm.Deterministic("c", z_c * sigma_c)

    z_l = pm.Normal("z_l", mu=0, sigma=1, shape=n_experts)
    l = pm.Deterministic("l", z_l * sigma_l)

    z_residual = pm.Normal("z_residual", mu=0, sigma=1, shape=n_obs)
    residual = pm.Deterministic("residual", z_residual * sigma_residual)

    z = intercept + c[data['case_idx'].values] + l[data['expert_idx'].values] + residual

    y_obs = pm.Bernoulli("y_obs", logit_p=z, observed=data['Y'].values)
```

### 3. How flexible is the code for different model specifications?

**NEW: Use `noise_decomposition_flexible.py`** - We now provide a flexible script that accepts a `model_type` parameter!

**Easy model selection:**

```python
from noise_decomposition_flexible import run_analysis

# Fit IRT model (Signal + Level Noise only)
results_irt = run_analysis("data.csv", model_type="IRT")

# Fit SSIT model (Signal + Level Noise + Residual)
results_ssit = run_analysis("data.csv", model_type="SSIT")

# Fit full KSS model (all four components)
results_kss = run_analysis("data.csv", model_type="KSS")
```

**Model comparison table:**

| Model | Components Estimated | When to Use | How to Use |
|-------|---------------------|-------------|------------|
| **IRT (1PL Rasch)** | Signal + Level Noise only | Exploratory analysis, benchmark | `model_type="IRT"` |
| **SSIT** | Signal + Level + Residual | T=1, or when occasion noise is negligible | `model_type="SSIT"` |
| **KSS (Full)** | All four components | T≥2, full decomposition needed | `model_type="KSS"` |

**Original notebook**: The `a0_Monkey2_Bayesian_v2.ipynb` notebook always fits the full KSS model. To fit different models with the notebook, you need to manually modify the model definition (see Option 2 in FAQ #2).

## Outputs

### Console Output

For each dataset, the notebook prints:
1. Data summary (number of experts, cases, observations)
2. Posterior summary statistics for scale parameters
3. Variance decomposition percentages
4. Effective scale estimates (σ values)

Example:
```
Variance Decomposition:
Total Variance (sum of components): 15.035
Percentage contributions:
  Signal (case) variance:         65.74%
  Level noise (expert) variance:    23.01%
  Pattern noise (interaction) variance: 9.81%
  Occasion noise (observation-level) variance: 1.44%

Effective scale estimates:
Signal (S): 3.14
Level Noise (LN): 1.86
Pattern Noise (PN): 1.21
Occasion Noise (ON): 0.47
```

### CSV Files

For each input dataset (e.g., `dataQ1.csv`), the notebook creates a corresponding latent effects file (e.g., `dataQ1_latent_effects.csv`) with columns:

| Column | Description |
|--------|-------------|
| `i` | Expert index (0 to M-1) |
| `j` | Case index (0 to N-1) |
| `t` | Occasion index (0 to T-1) |
| `c` | Estimated case effect (signal) |
| `l` | Estimated expert effect (level noise) |
| `p` | Estimated expert-case interaction (pattern noise) |
| `o` | Estimated observation-level effect (occasion noise) |

**Note**: These are the posterior means of the latent variables averaged across all MCMC samples.

### Figures

The notebook generates:

- **Matrix visualizations** (`matrix_c.png`, `matrix_l.png`, `matrix_p.png`, `matrix_o1.png`, `matrix_o2.png`):
  - Grayscale heatmaps showing latent effects
  - Rows sorted by expert effect, columns by case effect

- **Figure 2** (`Figure2.png`): Percent Yes and Percent Agreement vs Signal for Q1 and Q2

- **Figure 3** (`Figure3.png`): Variance decomposition visualization with Gaussian distributions and stacked bar charts

## Requirements

### Python Packages

```bash
pip install numpy pandas pymc arviz matplotlib pytensor numpyro
```

### Specific Versions (tested)

- Python: 3.9+
- PyMC: 5.0+
- NumPyro: 0.13+ (for fast NUTS sampling)
- ArviZ: 0.16+ (for diagnostics and plotting)

## Usage

### Quick Start with Flexible Script (Recommended)

The new flexible script makes it easy to fit different model types:

**Command Line Usage:**

```bash
# Fit the full KSS model (default)
python noise_decomposition_flexible.py dataQ1.csv

# Fit the SSIT model (no occasion noise)
python noise_decomposition_flexible.py dataQ1.csv SSIT

# Fit the IRT model (only signal and level noise)
python noise_decomposition_flexible.py dataQ1.csv IRT
```

**Python Script Usage:**

```python
from noise_decomposition_flexible import run_analysis, compare_models

# Fit a single model
results = run_analysis("dataQ1.csv", model_type="KSS")

# Compare all three models on the same data
all_results = compare_models("dataQ1.csv", models=["IRT", "SSIT", "KSS"])

# Access results
print(results['variance_decomposition'])
print(results['effective_scales'])
```

**Model Selection Guide:**

| Use Case | Model Type | What Gets Estimated |
|----------|-----------|---------------------|
| **Exploratory analysis, baseline** | IRT | Signal (c_i) + Level Noise (ℓ_j) only |
| **T=1 or limited data** | SSIT | Signal + Level Noise + Residual (pattern + occasion combined) |
| **Full decomposition, T≥2** | KSS | Signal + Level + Pattern + Occasion (all separate) |

### Original Notebook Usage

1. **Prepare your data** in the required CSV format (id, item, t, Y)

2. **Run the notebook** which fits the full KSS model, or use the original function:

```python
# From the notebook
results = run_analysis("your_data.csv", "your_results.pkl")
```

3. **Check convergence diagnostics**:
   - All R-hat values should be < 1.01
   - ESS should be > 1000 for all parameters
   - Review trace plots if needed: `az.plot_trace(results['trace'])`

4. **Extract results**:

```python
# Variance decomposition
print(results['variance_decomposition'])

# Effective scales
print(results['effective_scales'])

# Full posterior samples
trace = results['trace']
```

## Sample Size Recommendations

Based on simulation studies (see paper), we recommend:

| To estimate | Minimum N (cases) | Minimum M (experts) | Minimum T (occasions) |
|-------------|------------------|---------------------|----------------------|
| Signal + Level Noise | 30 | 10 | 1 |
| + Pattern Noise | 50 | 15 | 1 |
| + Occasion Noise | 50 | 15 | 2 |

**Rules of thumb:**
- More cases (N) → Better signal estimation
- More experts (M) → Better level and pattern noise estimation
- More occasions (T≥2) → Separates pattern from occasion noise
- Balanced designs work best (similar number of responses per expert-case-occasion combination)

## Troubleshooting

### Convergence Issues

If you see R-hat > 1.01 or low ESS:

1. **Increase tuning iterations**: Change `tune=2000` to `tune=5000`
2. **Increase target acceptance**: Already at 0.98 (very high)
3. **Check for label switching**: Examine trace plots
4. **Reduce model complexity**: Try IRT or SSIT instead of full KSS
5. **Add more informative priors**: If you have domain knowledge about expected variance magnitudes

### Memory Issues

If sampling runs out of memory:

1. **Reduce number of chains**: Change `chains=10` to `chains=4`
2. **Reduce draws**: Change `draws=5000` to `draws=2000`
3. **Use fewer cores**: Change `cores=6` to match your CPU

### Numerical Instabilities

If you see divergences or integration warnings:

1. **Already using non-centered parameterization** (good!)
2. **Increase target_accept**: Try 0.99 or 0.995
3. **Check for extreme values**: Look at raw data for outliers or imbalanced designs

## Citation

If you use this code, please cite our paper:

```bibtex
@article{YourPaper2024,
  title={Decomposing Noise in Clinical Diagnosis: A Bayesian Framework},
  author={[Your Authors]},
  journal={[Journal Name]},
  year={2024}
}
```

## License

[Specify your license here]

## Contact

For questions about the code or methods, please [open an issue](https://github.com/yourusername/yourrepo/issues) or contact [your email].

## References

- Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*. Little, Brown Spark.
- PyMC Development Team. (2023). PyMC: Probabilistic Programming in Python.
- [Your paper reference]
