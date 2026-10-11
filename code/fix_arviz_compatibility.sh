#!/bin/bash
# Fix ArviZ compatibility issue with SciPy

echo "Fixing ArviZ compatibility issue..."

# Activate environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate noise_analysis

echo "Upgrading ArviZ to version 0.18.0 (compatible with newer SciPy)..."
pip install --upgrade 'arviz>=0.18.0'

echo ""
echo "========================================================================"
echo "Fix complete!"
echo "========================================================================"
echo ""
echo "Please restart your Jupyter kernel:"
echo "  1. In Jupyter notebook, click: Kernel → Restart Kernel"
echo "  2. Run all cells again"
echo ""
echo "Verifying installation..."
python -c "import arviz; import scipy; print('ArviZ version:', arviz.__version__); print('SciPy version:', scipy.__version__); import pymc; print('PyMC version:', pymc.__version__); print('✓ All packages compatible!')"
echo ""
