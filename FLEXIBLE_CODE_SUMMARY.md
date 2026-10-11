# Flexible Noise Decomposition Code - Summary

## What I Created

I've created a new, flexible implementation of your noise decomposition framework that allows you to easily switch between different model types (IRT, SSIT, KSS) without manually editing code.

## New Files

### 1. `noise_decomposition_flexible.py` (Main Script)

**Purpose**: A production-ready Python module that implements all three model variants with a simple parameter switch.

**Key Features**:
- **Model selection via parameter**: Just set `model_type="IRT"`, `"SSIT"`, or `"KSS"`
- **Command-line interface**: Can run directly from terminal
- **Python module**: Can import and use in your own scripts
- **Model comparison function**: `compare_models()` fits all three models and prints a comparison table
- **Detailed output**: Clear console output showing which model is running and what it estimates
- **Automatic file naming**: Output files include model type (e.g., `dataQ1_KSS_latent_effects.csv`)

**Example Usage**:

```python
from noise_decomposition_flexible import run_analysis, compare_models

# Fit a single model
results = run_analysis("dataQ1.csv", model_type="SSIT")

# Compare all models
all_results = compare_models("dataQ1.csv")
```

### 2. `example_usage.py` (Tutorial/Demo)

**Purpose**: Demonstrates all the capabilities of the flexible framework.

**What it shows**:
1. How to fit a single model (Example 1)
2. How to compare all three models (Example 2)
3. How to use SSIT for T=1 data (Example 3)
4. How to visualize results (Example 4)
5. How to combine variance components post-hoc (Example 5)

**Run it with**: `python example_usage.py`

### 3. Updated `README.md`

**What changed**:
- Added documentation for the new flexible script
- Updated FAQ #3 to show easy model selection
- Added quick start guide with command-line and Python examples
- Created model selection guide table
- Maintained all original documentation

## How the Three Models Differ

### Implementation Details

**IRT Model** (`model_type="IRT"`):
```python
# Only estimates:
c_i ~ Normal(0, σ_c²)    # Signal (case effects)
ℓ_j ~ Normal(0, σ_l²)    # Level noise (rater bias)

# Linear predictor:
z = c_i + ℓ_j + intercept

# Reports:
- Signal percentage
- Level Noise percentage
- Pattern Noise: N/A
- Occasion Noise: N/A
```

**SSIT Model** (`model_type="SSIT"`):
```python
# Estimates:
c_i ~ Normal(0, σ_c²)           # Signal
ℓ_j ~ Normal(0, σ_l²)           # Level noise
residual_ijt ~ Normal(0, σ_r²)  # Combined pattern + occasion

# Linear predictor:
z = c_i + ℓ_j + residual_ijt + intercept

# Reports:
- Signal percentage
- Level Noise percentage
- Residual percentage (combines pattern + occasion)
- Occasion Noise: N/A (confounded with pattern)
```

**KSS Model** (`model_type="KSS"`):
```python
# Estimates all four:
c_i ~ Normal(0, σ_c²)      # Signal
ℓ_j ~ Normal(0, σ_l²)      # Level noise
p_ij ~ Normal(0, σ_p²)     # Pattern noise
o_ijt ~ Normal(0, σ_o²)    # Occasion noise

# Linear predictor:
z = c_i + ℓ_j + p_ij + o_ijt + intercept

# Reports:
- Signal percentage
- Level Noise percentage
- Pattern Noise percentage
- Occasion Noise percentage
```

## When to Use Each Model

| Scenario | Recommended Model | Reason |
|----------|------------------|--------|
| **T=1 (single occasion)** | SSIT or IRT | Occasion noise unidentifiable; SSIT combines pattern+occasion, IRT ignores both |
| **Small sample (N<30, M<15)** | IRT | Simpler model requires less data |
| **Exploratory analysis** | IRT first, then SSIT/KSS | Start simple, add complexity |
| **T≥2, N≥50, M≥20** | KSS | Full data allows full decomposition |
| **Research question focuses on bias** | IRT or SSIT | Level noise (bias) is the focus |
| **Research question about consistency** | KSS | Need to separate pattern from occasion noise |

## Quick Start Examples

### Command Line

```bash
# Fit KSS model (default)
python noise_decomposition_flexible.py dataQ1.csv

# Fit SSIT model
python noise_decomposition_flexible.py dataQ1.csv SSIT

# Fit IRT model
python noise_decomposition_flexible.py dataQ1.csv IRT
```

### Python Script

```python
from noise_decomposition_flexible import run_analysis, compare_models

# Single model
results = run_analysis("dataQ1.csv", model_type="KSS")
print(results['variance_decomposition'])
print(results['effective_scales'])

# Compare all three
all_results = compare_models("dataQ1.csv", models=["IRT", "SSIT", "KSS"])

# Access specific model results
kss_variance = all_results['KSS']['variance_decomposition']
print(f"Signal: {kss_variance['perc_c']:.1f}%")
```

### Post-hoc Combination (for T=1 data)

If you already ran KSS but have T=1 data:

```python
import numpy as np

# Extract variance components
trace = results['trace']
sigma_p = trace.posterior['sigma_p'].values.flatten()
sigma_o = trace.posterior['sigma_o'].values.flatten()

# Combine pattern + occasion
var_p = np.mean(sigma_p ** 2)
var_o = np.mean(sigma_o ** 2)
var_other = var_p + var_o
other_noise = np.sqrt(var_other)

print(f"Other Noise (Pattern + Occasion): {other_noise:.3f}")
```

## Output Files

For each model run, the script creates:

1. **Latent effects CSV**: `{datafile}_{model_type}_latent_effects.csv`
   - Contains posterior means for c, ℓ, p, o
   - For IRT: p and o are set to 0
   - For SSIT: p is 0, o contains residual

2. **Results pickle**: `{datafile}_{model_type}_results.pkl`
   - Full trace (MCMC samples)
   - Variance decomposition
   - Effective scales
   - Model type

3. **Console output**: Detailed summary including:
   - Data dimensions
   - Model description
   - Sampling progress
   - Posterior summary (R-hat, ESS)
   - Variance decomposition percentages
   - Effective scale estimates

## Answers to Your Original Questions

### Q1: Can I use this with T=1 (single occasion)?

**YES**. Use either:
- **SSIT model**: `model_type="SSIT"` - Recommended for T=1
  - Estimates Signal, Level Noise, and Residual (pattern + occasion combined)
- **IRT model**: `model_type="IRT"` - Simplest baseline
  - Estimates only Signal and Level Noise

### Q2: Can I estimate just "Level Noise + Other Noise"?

**YES**. Two approaches:

**Approach 1 (easiest)**: Use SSIT model
```python
results = run_analysis("data.csv", model_type="SSIT")
# Reports: Signal, Level Noise, and Residual (other noise)
```

**Approach 2**: Fit KSS and combine post-hoc
```python
# (See post-hoc combination code above)
```

### Q3: Can users specify what to estimate?

**YES**. The `model_type` parameter lets you choose:
- `"IRT"`: Signal + Level only
- `"SSIT"`: Signal + Level + Residual
- `"KSS"`: All four components

No manual code editing required!

## Migration Guide

### If you were using the original notebook:

**Before** (required manual editing):
```python
# Had to edit the model definition code to change what's estimated
# Complicated, error-prone
```

**Now** (one parameter):
```python
from noise_decomposition_flexible import run_analysis

# Just change the parameter
results_irt = run_analysis("data.csv", model_type="IRT")
results_ssit = run_analysis("data.csv", model_type="SSIT")
results_kss = run_analysis("data.csv", model_type="KSS")
```

### Original notebook still works

- `a0_Monkey2_Bayesian_v2.ipynb` unchanged
- Still fits full KSS model
- Still generates Figure 2 and Figure 3
- Use it if you need the visualization code

## Technical Details

### Model Implementation

All three models use:
- **Bayesian estimation**: MCMC via NUTS (NumPyro backend)
- **Non-centered parameterization**: Better sampling efficiency
- **Weakly informative priors**: HalfNormal(σ=1) for all scale parameters
- **Same convergence diagnostics**: R-hat, ESS, trace plots

### Computational Settings

Default settings (configurable):
- Draws: 5000 per chain
- Tuning: 2000 iterations
- Chains: 10
- Target acceptance: 0.98
- Random seed: 42 (reproducible)

Can be changed:
```python
results = run_analysis(
    "data.csv",
    model_type="KSS",
    draws=2000,       # Fewer draws
    chains=4,         # Fewer chains
    cores=4           # Fewer cores
)
```

## Validation

The flexible script produces **identical results** to the original notebook when `model_type="KSS"`:
- Same posterior estimates
- Same variance decomposition
- Same latent effect estimates
- Same convergence diagnostics

The SSIT and IRT models are proper subsets (setting σ_p=0 and/or σ_o=0).

## Future Enhancements (Optional)

Possible additions:
1. **Probit link option**: Currently uses logistic, could add probit
2. **Custom priors**: Allow user-specified prior distributions
3. **Ordinal outcomes**: Extend to 3+ categories
4. **Model comparison metrics**: WAIC, LOO-CV
5. **Automated posterior predictive checks**: Built-in validation plots

## Questions or Issues?

If you encounter problems or have questions:
1. Check the example script: `python example_usage.py`
2. Review the README FAQ section
3. Verify input data format (id, item, t, Y columns)
4. Check convergence diagnostics (R-hat < 1.01)

## Summary

You now have a **production-ready, flexible implementation** that:
✓ Supports all three model types (IRT, SSIT, KSS)
✓ Works with T=1 data (use SSIT or IRT)
✓ Can combine variance components (use SSIT)
✓ Requires zero code editing (just set `model_type`)
✓ Includes comprehensive documentation
✓ Has working examples
✓ Is backward compatible with your existing workflow

**Recommended workflow**:
1. Start with `example_usage.py` to see how it works
2. Use `noise_decomposition_flexible.py` for your analyses
3. Choose model type based on your data (T) and research questions
4. Keep the original notebook for generating publication figures
