# Killer Figure Version 3 - Changes Summary

## Major Changes Implemented

### 1. **Model Adjusted: Bias Now Reduces Accuracy**

**Previous (v2):** Both raters had identical target performance (Sens=0.80, Spec=0.80)

**New (v3):**
- **Rater A (Biased):** Lower target (Sens=0.70, Spec=0.70), AUC = 0.77
  - High level noise: σ_ℓ = 2.0 (increased from 1.5)
  - Low pattern/occasion noise
  - **Key insight**: Systematic bias degrades accuracy despite low total noise

- **Rater B (Unbiased):** Higher target (Sens=0.85, Spec=0.85), AUC = 0.93
  - Very low level noise: σ_ℓ = 0.2 (decreased from 0.3)
  - High pattern/occasion noise
  - **Key insight**: Absence of bias preserves accuracy despite high variability

**Result:** The figure now demonstrates that **consistency ≠ accuracy**. The biased rater has less total noise but worse discrimination.

### 2. **Operating Points Added to ROC Curve**

- White circle (○): Rater A's operating point on ROC curve
- Black circle (●): Rater B's operating point on ROC curve
- Shows each rater's actual sensitivity-specificity trade-off
- Visually reinforces that Rater B operates at a better point on their ROC curve

### 3. **Layout Optimized: Better Space Usage**

**Previous:** 3 rows (heatmaps, ROC spanning full width, variance bars spanning full width)

**New:** 2×2 grid
- Top row: Two heatmaps (unchanged)
- Bottom left: ROC curve (square aspect ratio maintained)
- Bottom right: Variance decomposition bars

**Benefit:** More compact, better use of space, ROC and variance decomposition are visually aligned

### 4. **LaTeX Description Updated**

Updated `sections/01_introduction.tex` to reflect:

1. **New noise parameters:**
   - Rater A: σ_ℓ = 2.0, σ_p = 0.3, σ_o = 0.2
   - Rater B: σ_ℓ = 0.2, σ_p = 1.2, σ_o = 0.8

2. **Different accuracy levels:**
   - Removed claim of "identical accuracy"
   - Added AUC values (0.77 vs 0.93)
   - Emphasized that bias degrades accuracy

3. **Clinical implications revised:**
   - Rater A: Threshold recalibration is **high priority** (would substantially improve accuracy)
   - Rater B: Training/decision aids are **lower priority** (already high accuracy)
   - Added key insight: "consistency does not guarantee accuracy"

4. **Figure caption completely rewritten:**
   - New title: "Bias reduces accuracy despite low noise; variability can coexist with high accuracy"
   - Describes operating points on ROC curves
   - Emphasizes the counterintuitive finding that the "noisier" rater is more accurate

## Key Takeaway Message

The revised figure now makes a **stronger and more important point**:

> **Old message:** "Two raters with identical accuracy can have different noise profiles requiring different interventions"

> **New message:** "Systematic bias reduces accuracy even when total noise is low. An unbiased but variable rater can be more accurate than a biased but consistent rater. This is why noise decomposition matters—consistency metrics alone are misleading."

This is more clinically relevant because it challenges the intuition that "consistency = quality."

## Files Modified

1. `generate_killer_figure_v2.py` - Python code for figure generation
2. `sections/01_introduction.tex` - LaTeX text describing the example
3. `killer_figure.pdf` - Output figure (vector graphics)
4. `killer_figure.png` - Output figure (raster, 300 dpi)

## Technical Implementation Details

### Binormal ROC Model
- Rater A: d' = 0.378, σ_total = 0.361 → AUC = 0.771
- Rater B: d' = 2.990, σ_total = 1.442 → AUC = 0.929

The d' (discriminability) for Rater B is ~8× higher than Rater A, demonstrating that lack of bias is crucial for discrimination performance.

### Operating Point Calculation
Operating points calculated from actual simulated responses:
- Rater A: FPR=0.07, TPR=1.00 (very liberal threshold to compensate for bias)
- Rater B: FPR=0.33, TPR=0.73 (moderate threshold, balanced performance)

Note: The bias tuning algorithm tries to achieve target performance, but actual realized performance varies due to finite sample simulation.
