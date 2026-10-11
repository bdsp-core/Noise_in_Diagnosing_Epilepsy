# Spikes Dataset Analysis - Summary

## What We've Done

I've created a complete, modular analysis framework for your spikes dataset and completed the descriptive statistics portion. Here's what you have:

### 1. Core Library Module: `noise_analysis_lib.py`

**Purpose**: Reusable functions for all case studies

**Key Functions**:
- `prepare_data_for_analysis()` - Convert matrices to long format for modeling
- `run_noise_analysis()` - Run SSIT/IRT/KSS models
- `compute_descriptive_stats()` - Accuracy by expertise group
- `compute_roc_points()` - TPR, FPR, sensitivity, specificity for each rater
- `extract_participant_estimates()` - Get level noise, skill for each participant
- `extract_item_difficulties()` - Get difficulty for each question
- `plot_variance_decomposition()` - Visualization
- `plot_roc_curves()` - ROC plots by group
- `save_results_summary()` - Export to Excel

### 2. Spikes Descriptive Analysis: `spikes_descriptive_analysis.py`

**What it does** (already completed):
- ✅ Loads the 3 data files (expertise, true answers, responses)
- ✅ Computes accuracy by expertise group
- ✅ Computes ROC operating points for all 37 participants
- ✅ Prepares data in long format for SSIT model
- ✅ Creates visualizations
- ✅ Saves results to Excel and CSV

**Run with**: `python3 spikes_descriptive_analysis.py`

**Output files** (already created):
- `spikes_analysis_output/spikes_data_for_analysis.csv` - Ready for SSIT model
- `spikes_analysis_output/spikes_descriptive_stats.xlsx` - Descriptive statistics
- `spikes_analysis_output/accuracy_by_expertise.png`
- `spikes_analysis_output/roc_operating_points.png`
- `spikes_analysis_output/sensitivity_vs_specificity.png`

### 3. SSIT Model Analysis Notebook: `Spikes_Analysis_SSIT.ipynb`

**What it will do** (you need to run this in Jupyter):
- Runs SSIT model on prepared data
- Estimates level noise for each of 37 participants
- Estimates population skill level
- Estimates difficulty for each of 1000 questions
- Creates additional visualizations
- Exports complete results

**Requirements**:
- Jupyter environment with PyMC installed
- Run this after the descriptive analysis

## Results So Far (Descriptive Statistics)

### Dataset Overview
- **Items**: 1000 spike identification questions
- **Participants**: 37 (13 Experts, 17 Experienced, 7 Novices)
- **Observations**: 37,000 (1000 × 37)

### Accuracy by Expertise Group

| Expertise | N | Median | Range |
|-----------|---|--------|-------|
| Experts | 13 | 0.518 | [0.480, 0.587] |
| Experienced | 17 | 0.546 | [0.496, 0.628] |
| Novices | 7 | 0.524 | [0.496, 0.546] |

**Finding**: Experienced group has slightly higher median accuracy than Experts and Novices.

### ROC Metrics by Expertise

| Expertise | Sensitivity (TPR) | Specificity | FPR |
|-----------|------------------|-------------|-----|
| Experts | 0.573 ± 0.016 | 0.476 ± 0.047 | 0.524 ± 0.047 |
| Experienced | 0.638 ± 0.063 | 0.513 ± 0.053 | 0.487 ± 0.053 |
| Novices | 0.585 ± 0.019 | 0.468 ± 0.016 | 0.532 ± 0.016 |

**Finding**: Experienced group has highest sensitivity (best at detecting true spikes).

## Next Steps: Complete SSIT Model Analysis

### Option 1: Run in Jupyter Notebook (Recommended)

If you have Jupyter with PyMC installed:

1. Open `Spikes_Analysis_SSIT.ipynb`
2. Run all cells
3. This will estimate:
   - Level noise (bias) for each of 37 participants
   - Population skill level (1/σ_residual)
   - Difficulty for each of 1000 questions

### Option 2: Run in Python Script

If you prefer a script, you can adapt the notebook code:

```python
from noise_decomposition_flexible import run_analysis

# Run SSIT model
results = run_analysis(
    'spikes_analysis_output/spikes_data_for_analysis.csv',
    model_type='SSIT',
    draws=5000,
    tune=2000,
    chains=10,
    cores=6
)

# Results contain:
# - results['variance_decomposition']: percentages
# - results['effective_scales']: σ estimates
# - results['trace']: full MCMC samples
```

## What You'll Get from SSIT Model

### 1. Variance Decomposition

Estimates of:
- **Signal %**: Variation due to item difficulty
- **Level Noise %**: Variation due to systematic bias across raters
- **Residual %**: Remaining variation (pattern + occasion noise)

### 2. Participant-Level Estimates

For each of 37 participants:
- **Level noise (ℓ_j)**: Bias parameter
  - Positive → Tends to over-call (more "yes" responses)
  - Negative → Tends to under-call (more "no" responses)
  - Near zero → Neutral threshold
- **Expertise group**: For comparison

### 3. Item-Level Estimates

For each of 1000 questions:
- **Difficulty (c_i)**: Signal strength
  - Positive → More difficult (less likely to be called "spike")
  - Negative → Easier (more likely to be called "spike")

### 4. Population-Level Estimates

- **Population skill**: 1/σ_residual
  - Higher = Better discrimination ability
- **Effective scales**: σ for signal, level noise, residual

## File Organization

```
Noise_in_Diagnosing_Epilepsy/
├── noise_analysis_lib.py              # Core library (reusable functions)
├── noise_decomposition_flexible.py    # Flexible model runner
├── spikes_descriptive_analysis.py     # Descriptive stats (already run)
├── Spikes_Analysis_SSIT.ipynb        # SSIT model notebook (run this next)
├── spikes_analysis_output/            # All results
│   ├── spikes_data_for_analysis.csv   # Prepared data for SSIT
│   ├── spikes_descriptive_stats.xlsx  # Descriptive stats
│   ├── accuracy_by_expertise.png
│   ├── roc_operating_points.png
│   └── sensitivity_vs_specificity.png
└── (future outputs from SSIT notebook)
    ├── participant_estimates_SSIT.csv
    ├── item_difficulties_SSIT.csv
    ├── spikes_SSIT_analysis_complete.xlsx
    └── additional visualizations
```

## Why This Modular Approach?

**Benefits**:
1. ✓ **No code duplication**: Core functions in `noise_analysis_lib.py`
2. ✓ **Easy to maintain**: Update library once, all analyses benefit
3. ✓ **Clear narratives**: Each notebook tells a case study story
4. ✓ **Reusable**: Use same framework for future datasets

**For your next dataset (full KSS model)**:
- Create a new notebook (e.g., `CaseStudy_KSS.ipynb`)
- Import from `noise_analysis_lib.py`
- Use `model_type="KSS"` instead of `"SSIT"`
- Same structure, different dataset

## Troubleshooting

### If you don't have PyMC installed

```bash
# Create conda environment
conda create -n noise_analysis python=3.9
conda activate noise_analysis

# Install packages
pip install pymc arviz numpyro matplotlib seaborn pandas scikit-learn openpyxl
```

### If sampling is slow

Reduce computational load:
```python
results = run_analysis(
    '...',
    model_type='SSIT',
    draws=2000,      # Fewer draws
    chains=4,        # Fewer chains
    cores=4
)
```

### If you get convergence warnings

Check R-hat values in output:
- R-hat < 1.01 is good
- R-hat > 1.01 means increase `tune` or `draws`

## Questions About the Analysis

### Q: Why SSIT model for spikes?

**A**: You have T=1 (single occasion). SSIT is appropriate because:
- Combines pattern + occasion noise into single residual
- More stable estimates with T=1
- Still estimates level noise (bias) for each participant

### Q: What if I want to separate pattern from occasion?

**A**: You need T≥2 (repeated ratings). Then use KSS model:
```python
results = run_analysis(..., model_type='KSS')
```

### Q: How do I interpret level noise?

**A**:
- **ℓ_j > 0**: Over-caller (liberal threshold, says "yes" more often)
- **ℓ_j < 0**: Under-caller (conservative threshold, says "no" more often)
- **ℓ_j ≈ 0**: Neutral threshold

### Q: How do I compare expertise groups?

**A**: After running SSIT model:
```python
# Statistical test
from scipy.stats import kruskal
stat, p = kruskal(experts_ln, experienced_ln, novices_ln)

# Effect size
mean_diff = experts_ln.mean() - novices_ln.mean()
```

## Summary

**Completed**:
- ✅ Created reusable analysis library
- ✅ Ran descriptive statistics for spikes dataset
- ✅ Generated visualizations
- ✅ Prepared data for SSIT model
- ✅ Created Jupyter notebook template

**To Do**:
- ⏳ Run `Spikes_Analysis_SSIT.ipynb` in Jupyter environment
- ⏳ This will estimate level noise, skill, and difficulties
- ⏳ Interpret results and write up for paper

**For Paper**:
You'll be able to report:
1. Variance decomposition (Signal vs Level vs Residual)
2. Level noise by expertise group (with statistical tests)
3. Population skill level
4. Item difficulty distribution
5. Relationship between bias and accuracy

All results will be in:
- `spikes_SSIT_analysis_complete.xlsx`
- Publication-ready figures in `spikes_analysis_output/`
