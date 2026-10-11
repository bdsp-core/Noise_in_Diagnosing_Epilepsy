# Start Here: Quick Guide to Spikes Analysis

## Current Status ✅

**Completed**:
- ✅ Descriptive statistics analyzed
- ✅ Data prepared for SSIT model
- ✅ Visualizations created (boxplots, ROC curves)
- ✅ Environment setup in progress

**Next Step**: Run SSIT model in Jupyter to estimate level noise and item difficulties

## Step-by-Step Instructions

### 1. Wait for Environment Setup to Complete

The setup script is currently running. It will:
- Create `noise_analysis` conda environment
- Install PyMC, ArviZ, NumPyro, and other packages
- Register Jupyter kernel

**Wait for this message**: "Setup complete!"

### 2. Activate the Environment

```bash
conda activate noise_analysis
```

You should see `(noise_analysis)` in your terminal prompt.

### 3. Start Jupyter Notebook

```bash
cd "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/Noise_in_Diagnosing_Epilepsy"
jupyter notebook
```

This will open Jupyter in your web browser.

### 4. Open the Spikes Analysis Notebook

In Jupyter, click on: **`Spikes_Analysis_SSIT.ipynb`**

### 5. Select the Correct Kernel

In the notebook:
1. Click **Kernel** → **Change Kernel**
2. Select **"Python (noise_analysis)"**

### 6. Run the Analysis

Click **Cell** → **Run All** (or press Shift+Enter repeatedly)

The analysis will take **~10-20 minutes** to complete.

### 7. View Results

Results will be saved to `spikes_analysis_output/`:
- `spikes_SSIT_analysis_complete.xlsx` - Full results
- `participant_estimates_SSIT.csv` - Level noise for each participant
- `item_difficulties_SSIT.csv` - Difficulty for each question
- Various PNG figures

## What You'll Get

### Variance Decomposition

The SSIT model will tell you:
- **What % is Signal** (item difficulty variation)
- **What % is Level Noise** (systematic bias across raters)
- **What % is Residual** (other noise: pattern + occasion)

### Participant Estimates

For each of 37 participants:
- **Level noise (ℓ_j)**: Bias parameter
  - Positive = tends to over-call ("yes" bias)
  - Negative = tends to under-call ("no" bias)
  - Near zero = neutral threshold
- Can compare across expertise groups

### Item Estimates

For each of 1000 questions:
- **Difficulty (c_i)**: Signal strength
  - Positive = harder (less likely to be called "spike")
  - Negative = easier (more likely to be called "spike")

## Already Completed: Descriptive Stats

Check `spikes_analysis_output/spikes_descriptive_stats.xlsx` for:

**Accuracy by Expertise**:
- Experts: 0.518 (median) [0.480-0.587]
- Experienced: 0.546 [0.496-0.628]
- Novices: 0.524 [0.496-0.546]

**ROC Metrics**:
- Experts: Sensitivity 0.573, Specificity 0.476
- Experienced: Sensitivity 0.638, Specificity 0.513
- Novices: Sensitivity 0.585, Specificity 0.468

## Troubleshooting

### If environment setup fails

Re-run manually:
```bash
conda create -n noise_analysis python=3.10 -y
conda activate noise_analysis
conda install -c conda-forge numpy pandas scipy matplotlib seaborn scikit-learn -y
pip install pymc==5.10.0 arviz==0.17.0 numpyro openpyxl jupyter ipykernel
python -m ipykernel install --user --name noise_analysis
```

### If Jupyter kernel doesn't show

```bash
conda activate noise_analysis
python -m ipykernel install --user --name noise_analysis --display-name "Python (noise_analysis)"
```

Then restart Jupyter.

### If "ModuleNotFoundError: No module named 'pymc'"

Make sure you're using the correct kernel:
1. In Jupyter notebook
2. Kernel → Change Kernel → "Python (noise_analysis)"

### If sampling is too slow

Edit the notebook cell to use fewer chains:
```python
results = run_analysis(
    ...,
    draws=2000,  # Instead of 5000
    chains=4,    # Instead of 10
    cores=4
)
```

## Files Overview

| File | Purpose | Status |
|------|---------|--------|
| `setup_environment.sh` | Creates conda environment | Running |
| `spikes_descriptive_analysis.py` | Descriptive stats | ✅ Done |
| `Spikes_Analysis_SSIT.ipynb` | SSIT model analysis | ⏳ Run next |
| `noise_analysis_lib.py` | Reusable functions | Ready |
| `noise_decomposition_flexible.py` | Model runner | Ready |
| `spikes_analysis_output/` | All results | Partial |

## Timeline

| Task | Time | Status |
|------|------|--------|
| Environment setup | 5-10 min | In progress |
| SSIT model sampling | 10-20 min | Waiting |
| Total | 15-30 min | |

## After SSIT Analysis

You'll have complete results for the spikes dataset:
1. Variance decomposition percentages
2. Level noise estimates for all 37 participants
3. Difficulty estimates for all 1000 questions
4. Statistical comparisons across expertise groups
5. Publication-ready figures

## For Your Next Dataset (KSS Model)

Same process, but:
1. Create new notebook (copy `Spikes_Analysis_SSIT.ipynb`)
2. Change `model_type="SSIT"` to `model_type="KSS"`
3. Requires T≥2 (repeated ratings)

## Questions?

See detailed documentation:
- `ENVIRONMENT_SETUP.md` - Environment help
- `SPIKES_ANALYSIS_README.md` - Analysis overview
- `README.md` - Full framework documentation
- `QUICK_REFERENCE.md` - Command cheat sheet

## Summary

**Right now**: Wait for environment setup to finish

**Then**:
1. `conda activate noise_analysis`
2. `jupyter notebook`
3. Open `Spikes_Analysis_SSIT.ipynb`
4. Select "Python (noise_analysis)" kernel
5. Run all cells
6. Wait 10-20 minutes
7. Check `spikes_analysis_output/` for results

That's it! 🚀
