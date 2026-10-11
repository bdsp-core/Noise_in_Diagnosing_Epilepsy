# Killer Figure V4 - Final Version

## Summary of Changes from V3

### Problem Addressed
In V3, Rater A had operating point at sensitivity=0%, specificity=100%, which was too extreme and barely visible. The user requested:
1. Rater A should operate at FPR = 10% (more visible)
2. Rater A should have BETTER ROC curve than Rater B
3. Rater A should have LOWER accuracy than Rater B
4. Rater B should operate at optimal threshold
5. LaTeX should mention the "wasted accuracy" - how much better Rater A could do with optimal threshold

### Solution
Adjusted the noise parameters so that:
- Rater A has better discrimination (lower pattern/occasion noise) but conservative threshold
- The accuracy difference is narrow enough that bias actually hurts Rater A

## Final Parameters

### Rater A (Biased but Consistent):
- **Pattern noise:** σ_p = 0.42 (adjusted from 0.3)
- **Occasion noise:** σ_o = 0.28 (adjusted from 0.2)
- **Level noise:** σ_l = 2.0 (unchanged - high bias)
- **Discrimination noise:** σ_disc = 0.505
- **Signal:** σ_c = 2.0

### Rater B (Unbiased but Erratic):
- **Pattern noise:** σ_p = 1.2 (unchanged)
- **Occasion noise:** σ_o = 0.8 (unchanged)
- **Level noise:** σ_l = 0.2 (unchanged - low bias)
- **Discrimination noise:** σ_disc = 1.442
- **Signal:** σ_c = 2.0

## Results

### ROC Curves:
- **Rater A: AUC = 0.75** (BETTER discrimination)
- **Rater B: AUC = 0.70** (WORSE discrimination)

### Operating Points:

**Rater A (Conservative/Biased):**
- Threshold: Conservative (FPR = 10%)
- Sensitivity: 37%
- Specificity: 90%
- **Actual Accuracy: 64%**

**Rater A at Optimal Threshold (Potential):**
- Sensitivity: 68%
- Specificity: 68%
- **Potential Accuracy: 68%**
- **→ WASTED: 5 percentage points due to bias**

**Rater B (Unbiased/Optimal):**
- Threshold: Optimal (maximizes accuracy)
- Sensitivity: 65%
- Specificity: 65%
- FPR: 36%
- **Actual Accuracy: 65%**

## Key Finding

✓ **Rater A has BETTER discrimination** (AUC 0.75 > 0.70)
✓ **Rater A has LOWER accuracy** (64% < 65%)
✓ **Rater A is wasting 5 percentage points** (could achieve 68% with optimal threshold)
✓ **Rater A operates at FPR = 10%** (visible, not extreme)
✓ **Rater B operates at optimal threshold** (already maximizing their potential)

## Clinical Message

This demonstrates that:

1. **Superior discrimination ≠ higher accuracy** when threshold is biased
2. **Inferior discrimination can yield higher accuracy** when threshold is optimal
3. **Bias wastes discrimination potential** - Rater A could outperform Rater B (68% vs 65%) but doesn't due to conservative threshold
4. **Intervention priorities differ:**
   - Rater A: Threshold recalibration (high priority, low cost, +5 points)
   - Rater B: Discrimination training (lower priority, high cost, modest gains)

## LaTeX Updates

### Updated Values in Text:
- Rater A: σ_p = 0.42, σ_o = 0.28, AUC = 0.75, Sens = 37%, Spec = 90%, Acc = 64%
- Rater A optimal: Acc = 68%, wasted = 5 percentage points
- Rater B: σ_p = 1.2, σ_o = 0.8, AUC = 0.70, Sens = 65%, Spec = 65%, Acc = 65%

### Key Addition:
Explicitly mentions that Rater A is "wasting 5 percentage points of potential accuracy" and emphasizes this is a **low-cost, high-impact** intervention (just threshold adjustment, no training needed).

## Files Generated

- `generate_killer_figure_v4.py` - Python code with corrected parameters
- `killer_figure.pdf` - Vector graphics (publication quality)
- `killer_figure.png` - Raster (300 dpi)
- `sections/01_introduction.tex` - Updated LaTeX with correct values and wasted accuracy concept

## Visual Improvements

1. **Heatmaps:** Show bias (horizontal banding) vs variability (scattered pattern)
2. **ROC curves:** Rater A curve (solid) is higher than Rater B curve (dashed)
3. **Operating points:**
   - Rater A (white circle): Visible at FPR=10%, TPR=37%
   - Rater B (black circle): At FPR=36%, TPR=65% (optimal)
4. **Variance bars:** Show noise decomposition with direct labels
5. **Labels:** Clean, minimal, Tufte-style

## Technical Notes

### Binormal Model:
- ROC curve determined by: σ_disc = √(σ_p² + σ_o²)
- d' calculation: d' = Φ⁻¹(AUC) × σ_disc × √2
- Operating points:
  - Rater A: threshold = Φ⁻¹(0.90) × σ_disc_A (conservative, FPR=10%)
  - Rater B: threshold = d'_B / 2 (optimal for balanced prevalence)
- Accuracy = prevalence × sensitivity + (1 - prevalence) × specificity

### Prevalence:
- Set to 50% (balanced design)
- This simplifies optimal threshold calculation
- For balanced prevalence, optimal threshold is at d'/2
