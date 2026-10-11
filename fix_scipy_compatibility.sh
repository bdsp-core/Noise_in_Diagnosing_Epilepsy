#!/bin/bash
# Fix SciPy compatibility issue with ArviZ

echo "Fixing SciPy compatibility issue..."

# Activate environment and downgrade SciPy
source $(conda info --base)/etc/profile.d/conda.sh
conda activate noise_analysis

echo "Downgrading SciPy to version 1.13.1 (compatible with ArviZ 0.17.0)..."
pip install 'scipy==1.13.1'

echo ""
echo "========================================================================"
echo "Fix complete!"
echo "========================================================================"
echo ""
echo "Please restart your Jupyter kernel:"
echo "  1. In Jupyter notebook, click: Kernel → Restart Kernel"
echo "  2. Run all cells again"
echo ""
