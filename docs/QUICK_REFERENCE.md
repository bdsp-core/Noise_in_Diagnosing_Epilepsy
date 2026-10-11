# Noise Decomposition - Quick Reference Card

## Three Model Types

| Model | What it Estimates | Use When |
|-------|------------------|----------|
| **IRT** | Signal + Level Noise | T=1, small sample, or baseline |
| **SSIT** | Signal + Level Noise + Residual | T=1, want combined "other noise" |
| **KSS** | Signal + Level + Pattern + Occasion | T≥2, full decomposition |

## Command Line Usage

```bash
# Full KSS model (all four components)
python noise_decomposition_flexible.py dataQ1.csv

# SSIT model (good for T=1)
python noise_decomposition_flexible.py dataQ1.csv SSIT

# IRT model (simplest)
python noise_decomposition_flexible.py dataQ1.csv IRT
```

## Python Usage

```python
from noise_decomposition_flexible import run_analysis, compare_models

# Fit one model
results = run_analysis("data.csv", model_type="KSS")

# Compare all models
all_results = compare_models("data.csv")

# Access results
vd = results['variance_decomposition']
scales = results['effective_scales']
trace = results['trace']
```

## What Each Model Reports

### IRT Output
```
Signal (case) variance:         65.7%
Level Noise (expert) variance:  23.0%
Pattern Noise:                  N/A (not estimated)
Occasion Noise:                 N/A (not estimated)

Effective scales:
  Signal (S):        3.14
  Level Noise (LN):  1.86
  Pattern Noise:     N/A
  Occasion Noise:    N/A
```

### SSIT Output
```
Signal (case) variance:         65.7%
Level Noise (expert) variance:  23.0%
Residual (Pattern + Occasion):  11.3%
Occasion Noise:                 N/A (confounded)

Effective scales:
  Signal (S):        3.14
  Level Noise (LN):  1.86
  Residual:          1.24
  Occasion Noise:    N/A
```

### KSS Output
```
Signal (case) variance:         65.7%
Level Noise (expert) variance:  23.0%
Pattern Noise (interaction):     9.8%
Occasion Noise (within-rater):   1.4%

Effective scales:
  Signal (S):         3.14
  Level Noise (LN):   1.86
  Pattern Noise (PN): 1.21
  Occasion Noise (ON): 0.47
```

## Common Tasks

### Task 1: Analyze T=1 data
```python
# Use SSIT (combines pattern + occasion)
results = run_analysis("data.csv", model_type="SSIT")
```

### Task 2: Get only Level Noise + "Other"
```python
# Option A: Use SSIT
results = run_analysis("data.csv", model_type="SSIT")
print(f"Level Noise: {results['effective_scales']['LN_est']:.2f}")
print(f"Other Noise: {results['effective_scales']['PN_est']:.2f}")

# Option B: Fit KSS and combine post-hoc
results = run_analysis("data.csv", model_type="KSS")
import numpy as np
var_p = results['effective_scales']['PN_est'] ** 2
var_o = results['effective_scales']['ON_est'] ** 2
other = np.sqrt(var_p + var_o)
print(f"Other Noise: {other:.2f}")
```

### Task 3: Compare models
```python
all_results = compare_models("data.csv", models=["IRT", "SSIT", "KSS"])
# Prints comparison table automatically
```

### Task 4: Faster sampling (for testing)
```python
results = run_analysis(
    "data.csv",
    model_type="KSS",
    draws=2000,    # Instead of 5000
    chains=4,      # Instead of 10
    cores=4
)
```

## Input Data Format

Your CSV must have these columns:

| Column | Description | Example Values |
|--------|-------------|----------------|
| `id` | Rater/expert ID | 1, 2, 3, ..., M |
| `item` | Case ID | 1, 2, 3, ..., N |
| `t` | Occasion | 1, 2, ..., T |
| `Y` | Binary response | 0 or 1 |

Example:
```csv
id,item,t,Y
1,1,1,0
1,1,2,1
1,2,1,1
2,1,1,0
...
```

## Output Files

For each run, you get:

1. **Latent effects CSV**: `{datafile}_{model}_latent_effects.csv`
   - Columns: i, j, t, c, l, p, o
   - Posterior means for all latent variables

2. **Results pickle**: `{datafile}_{model}_results.pkl`
   - Full trace (MCMC samples)
   - Variance decomposition dict
   - Effective scales dict

3. **Console output**: Detailed summary with diagnostics

## Convergence Checks

Look for:
- ✓ **R-hat < 1.01** for all parameters
- ✓ **ESS > 1000** (effective sample size)
- ✗ If R-hat > 1.01: Increase `tune` or `draws`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| R-hat > 1.01 | Increase `tune=5000`, `draws=10000` |
| Out of memory | Reduce `chains=4`, `draws=2000` |
| Slow sampling | Reduce `chains=4`, use fewer `cores` |
| "Model failed" | Check data format, ensure Y is 0/1 |
| T=1 and KSS | Use SSIT instead, or expect σ_o ≈ 0 |

## Model Selection Decision Tree

```
Do you have T≥2 (repeated ratings)?
│
├─ YES: Do you need to separate pattern from occasion?
│   ├─ YES → Use KSS (full decomposition)
│   └─ NO → Use SSIT (combined residual)
│
└─ NO (T=1): What's your goal?
    ├─ Just bias → Use IRT
    └─ Bias + other → Use SSIT
```

## Sample Size Guidelines

| To estimate | Min N | Min M | Min T |
|-------------|-------|-------|-------|
| Signal + Level | 30 | 10 | 1 |
| + Pattern | 50 | 15 | 1 |
| + Occasion | 50 | 15 | 2 |

## Key References in Code

```python
# Main analysis function
results = run_analysis(data_filename, model_type="KSS")

# Model comparison
all_results = compare_models(data_filename)

# Results structure
results = {
    "model_type": str,
    "trace": InferenceData,
    "variance_decomposition": {
        "total_variance": float,
        "perc_c": float,  # Signal %
        "perc_l": float,  # Level %
        "perc_p": float,  # Pattern %
        "perc_o": float   # Occasion %
    },
    "effective_scales": {
        "S_est": float,   # σ_c
        "LN_est": float,  # σ_l
        "PN_est": float,  # σ_p
        "ON_est": float   # σ_o
    },
    "data": DataFrame
}
```

## Common Patterns

### Pattern 1: Analyze new dataset
```python
# 1. Fit SSIT (works for T=1 or T≥2)
results = run_analysis("my_data.csv", model_type="SSIT")

# 2. Check convergence
trace = results['trace']
# Look at R-hat values in console output

# 3. Extract key findings
vd = results['variance_decomposition']
print(f"Signal: {vd['perc_c']:.1f}%")
print(f"Level Noise: {vd['perc_l']:.1f}%")
print(f"Other Noise: {vd['perc_p']:.1f}%")
```

### Pattern 2: Model comparison for paper
```python
# Compare all three models
all_results = compare_models(
    "data.csv",
    draws=5000,
    chains=10
)

# Automatic comparison table printed
# Access individual results as needed
for model in ["IRT", "SSIT", "KSS"]:
    vd = all_results[model]['variance_decomposition']
    # ... extract for table
```

### Pattern 3: Group comparison
```python
# Analyze two groups
results_experts = run_analysis("experts.csv", model_type="SSIT")
results_novices = run_analysis("novices.csv", model_type="SSIT")

# Compare level noise
ln_experts = results_experts['effective_scales']['LN_est']
ln_novices = results_novices['effective_scales']['LN_est']

print(f"Experts: σ_l = {ln_experts:.2f}")
print(f"Novices: σ_l = {ln_novices:.2f}")
```

## Help & Documentation

- **Full documentation**: See README.md
- **Examples**: Run `python example_usage.py`
- **Details**: See FLEXIBLE_CODE_SUMMARY.md
- **Original paper methods**: See kilt.tex

## One-Liners

```bash
# Quick KSS analysis
python noise_decomposition_flexible.py data.csv

# Quick SSIT analysis (T=1 safe)
python noise_decomposition_flexible.py data.csv SSIT

# Compare all models
python -c "from noise_decomposition_flexible import compare_models; compare_models('data.csv')"

# Run examples
python example_usage.py
```
