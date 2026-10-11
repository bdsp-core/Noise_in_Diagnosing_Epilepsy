#!/bin/bash
# Setup script for noise analysis environment

echo "========================================================================"
echo "Setting up noise_analysis conda environment"
echo "========================================================================"

# Create conda environment
echo ""
echo "Creating conda environment 'noise_analysis' with Python 3.10..."
conda create -n noise_analysis python=3.10 -y

# Activate environment
echo ""
echo "Activating environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate noise_analysis

# Install core scientific packages
echo ""
echo "Installing core scientific packages..."
conda install -c conda-forge numpy pandas scipy matplotlib seaborn scikit-learn -y

# Install PyMC and dependencies
echo ""
echo "Installing PyMC and Bayesian packages..."
pip install pymc==5.10.0
pip install arviz==0.17.0
pip install numpyro

# Install additional utilities
echo ""
echo "Installing additional utilities..."
pip install openpyxl  # For Excel export
pip install jupyter notebook ipykernel  # For Jupyter notebooks

# Register kernel for Jupyter
echo ""
echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name noise_analysis --display-name "Python (noise_analysis)"

# Verify installation
echo ""
echo "========================================================================"
echo "Verifying installation..."
echo "========================================================================"
python -c "
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymc as pm
import arviz as az
import sklearn
print('✓ NumPy:', np.__version__)
print('✓ Pandas:', pd.__version__)
print('✓ Matplotlib:', plt.matplotlib.__version__)
print('✓ Seaborn:', sns.__version__)
print('✓ PyMC:', pm.__version__)
print('✓ ArviZ:', az.__version__)
print('✓ scikit-learn:', sklearn.__version__)
print('')
print('All packages installed successfully!')
"

echo ""
echo "========================================================================"
echo "Setup complete!"
echo "========================================================================"
echo ""
echo "To use this environment:"
echo "  1. Activate: conda activate noise_analysis"
echo "  2. Run Jupyter: jupyter notebook"
echo "  3. In Jupyter, select kernel: 'Python (noise_analysis)'"
echo ""
echo "Or run Python scripts directly:"
echo "  conda activate noise_analysis"
echo "  python your_script.py"
echo ""
echo "========================================================================"
