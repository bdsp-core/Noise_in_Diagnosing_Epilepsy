# Environment Setup Guide

## Quick Setup (Automated)

Run the setup script to create the environment automatically:

```bash
cd "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/Noise_in_Diagnosing_Epilepsy"
bash setup_environment.sh
```

This will:
1. Create conda environment `noise_analysis` with Python 3.10
2. Install all required packages (PyMC, ArviZ, NumPyro, etc.)
3. Register Jupyter kernel
4. Verify installation

**Time**: ~5-10 minutes depending on internet speed

## Using the Environment

### For Jupyter Notebooks

```bash
# Activate environment
conda activate noise_analysis

# Start Jupyter
jupyter notebook

# In Jupyter, select kernel: "Python (noise_analysis)"
```

Then open `Spikes_Analysis_SSIT.ipynb` and run all cells.

### For Python Scripts

```bash
# Activate environment
conda activate noise_analysis

# Run your script
python your_script.py
```

### Deactivate Environment

```bash
conda deactivate
```

## Manual Setup (if automated fails)

If the automated script doesn't work, follow these steps:

### Step 1: Create Environment

```bash
conda create -n noise_analysis python=3.10 -y
conda activate noise_analysis
```

### Step 2: Install Core Packages

```bash
conda install -c conda-forge numpy pandas scipy matplotlib seaborn scikit-learn -y
```

### Step 3: Install PyMC and Dependencies

```bash
pip install pymc==5.10.0
pip install arviz==0.17.0
pip install numpyro
```

### Step 4: Install Utilities

```bash
pip install openpyxl jupyter notebook ipykernel
```

### Step 5: Register Jupyter Kernel

```bash
python -m ipykernel install --user --name noise_analysis --display-name "Python (noise_analysis)"
```

### Step 6: Verify Installation

```bash
python -c "import pymc; import arviz; print('PyMC:', pymc.__version__); print('ArviZ:', arviz.__version__)"
```

You should see:
```
PyMC: 5.10.0
ArviZ: 0.17.0
```

## Installed Packages

After setup, you'll have:

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.10 | Base interpreter |
| NumPy | Latest | Numerical arrays |
| Pandas | Latest | Data manipulation |
| PyMC | 5.10.0 | Bayesian modeling |
| ArviZ | 0.17.0 | Diagnostics & visualization |
| NumPyro | Latest | Fast MCMC sampling backend |
| Matplotlib | Latest | Plotting |
| Seaborn | Latest | Statistical visualization |
| scikit-learn | Latest | ROC curves, metrics |
| openpyxl | Latest | Excel export |
| Jupyter | Latest | Notebooks |

## Troubleshooting

### Problem: "conda: command not found"

**Solution**: Install Miniconda or Anaconda first:
```bash
# Download and install Miniconda
# Visit: https://docs.conda.io/en/latest/miniconda.html
```

### Problem: "PyMC installation fails"

**Solution 1**: Use conda-forge:
```bash
conda install -c conda-forge pymc -y
```

**Solution 2**: Try older version:
```bash
pip install pymc==5.9.0
```

### Problem: "Kernel not showing in Jupyter"

**Solution**: Manually register kernel:
```bash
conda activate noise_analysis
python -m ipykernel install --user --name noise_analysis --display-name "Python (noise_analysis)"
```

Then restart Jupyter.

### Problem: "ImportError: No module named 'numpyro'"

**Solution**: Install NumPyro separately:
```bash
pip install numpyro jax jaxlib
```

### Problem: "Sampling is very slow"

**Solutions**:
1. Ensure NumPyro is installed: `pip install numpyro`
2. Use fewer chains/draws for testing: `draws=2000, chains=4`
3. Check CPU usage - NUTS should use multiple cores

### Problem: "M1/M2 Mac - Architecture issues"

**Solution**: Use x86_64 environment:
```bash
CONDA_SUBDIR=osx-64 conda create -n noise_analysis python=3.10
conda activate noise_analysis
conda config --env --set subdir osx-64
# Then proceed with installation
```

## Verifying Everything Works

Test with this minimal script:

```python
import pymc as pm
import numpy as np

# Create simple model
with pm.Model() as model:
    mu = pm.Normal('mu', mu=0, sigma=1)
    obs = pm.Normal('obs', mu=mu, sigma=1, observed=[1, 2, 3])
    trace = pm.sample(100, tune=100, chains=2, progressbar=False)

print("✓ PyMC is working correctly!")
print(f"  Posterior mean: {trace.posterior['mu'].mean():.3f}")
```

If this runs without errors, you're all set!

## Environment Management

### List all environments
```bash
conda env list
```

### Remove environment (if needed)
```bash
conda remove -n noise_analysis --all
```

### Export environment (for sharing)
```bash
conda activate noise_analysis
conda env export > environment.yml
```

### Recreate from export
```bash
conda env create -f environment.yml
```

## Next Steps

Once the environment is set up:

1. **Activate it**: `conda activate noise_analysis`
2. **Start Jupyter**: `jupyter notebook`
3. **Open**: `Spikes_Analysis_SSIT.ipynb`
4. **Select kernel**: "Python (noise_analysis)"
5. **Run all cells** (Shift+Enter or Cell → Run All)

The SSIT analysis will take ~10-20 minutes to complete.

## Support

If you encounter issues not covered here:
1. Check PyMC documentation: https://www.pymc.io/
2. Check conda documentation: https://docs.conda.io/
3. Look for error messages in the terminal output

## Quick Reference

```bash
# Activate
conda activate noise_analysis

# Start Jupyter
jupyter notebook

# Deactivate
conda deactivate

# Verify PyMC
python -c "import pymc; print(pymc.__version__)"

# Test sampling
python -c "import pymc as pm; pm.sample(100, tune=100, chains=2, progressbar=False)"
```
