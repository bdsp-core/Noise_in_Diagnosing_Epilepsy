# Killer Figure V5 - Final Version (Larger AUC Gap)

## Summary of Changes from V4

### User Request
"Can we make the difference in AUC somewhat more, but still satisfy the constraints (better accuracy for the rater with lower AUC)?"

### Solution: Option 2
- Increased AUC gap from 0.05 to **0.08** (60% larger)
- Changed Rater A's operating point from FPR=10% to **FPR=5%** (more conservative, still visible)
- Increased wasted potential from 5 points to **8.7 points** (74% more dramatic)
- All constraints still satisfied: Rater A has better AUC but lower accuracy

## Final Parameters

### Rater A (Biased but Consistent):
- **Pattern noise:** σ_p = 0.17 (decreased from 0.42 - even better discrimination)
- **Occasion noise:** σ_o = 0.11 (decreased from 0.28 - even better discrimination)
- **Level noise:** σ_l = 2.0 (unchanged - high bias)
- **Discrimination noise:** σ_disc = 0.202
- **Signal:** σ_c = 2.0

### Rater B (Unbiased but Erratic):
- **Pattern noise:** σ_p = 1.2 (unchanged)
- **Occasion noise:** σ_o = 0.8 (unchanged)
- **Level noise:** σ_l = 0.2 (unchanged - low bias)
- **Discrimination noise:** σ_disc = 1.442
- **Signal:** σ_c = 2.0

## Results

### ROC Curves:
- **Rater A: AUC = 0.78** (BETTER discrimination) - up from 0.75
- **Rater B: AUC = 0.70** (WORSE discrimination) - unchanged
- **AUC GAP: 0.08** (increased from 0.05)

### Operating Points:

**Rater A (Very Conservative/Biased):**
- Threshold: Very conservative (FPR = **5%**)
- Sensitivity: 29%
- Specificity: 95%
- **Actual Accuracy: 62%** (LOWER than B)

**Rater A at Optimal Threshold (Potential):**
- Sensitivity: 71%
- Specificity: 71%
- **Potential Accuracy: 71%**
- **→ WASTED: 8.7 percentage points** (increased from 4.8)

**Rater B (Unbiased/Optimal):**
- Threshold: Optimal (maximizes accuracy)
- Sensitivity: 65%
- Specificity: 65%
- FPR: 36%
- **Actual Accuracy: 65%** (HIGHER than A)

## Key Improvements Over V4

| Metric | V4 | V5 | Change |
|--------|----|----|--------|
| AUC Gap | 0.05 | 0.08 | +60% |
| Rater A AUC | 0.75 | 0.78 | +0.03 |
| Rater A FPR | 10% | 5% | More conservative |
| Rater A Accuracy | 64% | 62% | -2 points |
| Wasted Potential | 4.8 points | 8.7 points | +81% |
| Message Impact | Good | **Stronger** | More dramatic |

## Clinical Message

This demonstrates:

1. **Larger AUC gap makes discrimination difference more obvious** (0.78 vs 0.70)
2. **More conservative threshold wastes more potential** (9 points vs 5)
3. **Even with substantially better discrimination, bias causes lower accuracy**
4. **The intervention is even more urgent** (recovering 9 points vs 5)
5. **Cost-benefit is even more favorable** (simple threshold fix vs intensive training for similar gains)

## LaTeX Updates

### Updated Values in Text:
- Rater A: σ_p = 0.17, σ_o = 0.11, AUC = 0.78, FPR = 5%, Sens = 29%, Spec = 95%, Acc = 62%
- Rater A optimal: Acc = 71%, wasted = 9 percentage points
- Rater B: σ_p = 1.2, σ_o = 0.8, AUC = 0.70, Sens = 65%, Spec = 65%, Acc = 65%

### Key Additions:
- Emphasized "very low" pattern/occasion noise for Rater A
- Emphasized "very conservative" threshold (FPR = 5%)
- Updated wasted potential to 9 points
- Added "The large wasted potential (9 points) makes this especially urgent"
- Changed "substantially superior" discrimination for larger AUC gap
- Changed "much better curve" and "substantial discrimination potential"

## Visual Impact

1. **ROC curves:** Larger gap between curves (0.78 vs 0.70)
2. **Operating points:**
   - Rater A (white circle): At FPR=5%, TPR=29% (more extreme, still visible)
   - Rater B (black circle): At FPR=36%, TPR=65% (optimal)
3. **Heatmaps:** More dramatic bias pattern for Rater A
4. **Variance bars:** Smaller pattern/occasion noise for Rater A

## Files Generated

- `generate_killer_figure_v5.py` - Python code with larger AUC gap parameters
- `killer_figure.pdf` - Vector graphics (publication quality)
- `killer_figure.png` - Raster (300 dpi)
- `sections/01_introduction.tex` - Updated LaTeX with V5 values

## Comparison to V4

### V4 Message:
"Better discrimination doesn't guarantee higher accuracy if threshold is biased"
- Moderate demonstration (5 points wasted)
- AUC gap: 0.05 (small difference)

### V5 Message:
"**Substantially** better discrimination can yield **much** lower accuracy if threshold is very biased"
- **Dramatic demonstration (9 points wasted)**
- **AUC gap: 0.08 (noticeable difference)**
- **Stronger clinical urgency**

## Why This Is Better

1. **More impactful:** 9 wasted points is dramatic (vs 5)
2. **Clearer discrimination difference:** AUC 0.78 vs 0.70 is more obvious than 0.75 vs 0.70
3. **Stronger message:** "Very conservative" threshold at FPR=5% emphasizes the problem
4. **Better cost-benefit:** Same threshold fix recovers almost twice as much (9 vs 5 points)
5. **Still satisfies all constraints:**
   - Rater A has better AUC ✓
   - Rater A has lower accuracy ✓
   - Operating point is visible (FPR=5%) ✓
   - Rater B operates at optimal ✓

## Technical Notes

### Binormal Model:
- ROC curves determined by: σ_disc = √(σ_p² + σ_o²)
- Rater A: σ_disc = 0.202 → AUC = 0.78
- Rater B: σ_disc = 1.442 → AUC = 0.70
- Operating points:
  - Rater A: threshold = Φ⁻¹(0.95) × σ_disc_A (very conservative, FPR=5%)
  - Rater B: threshold = d'_B / 2 (optimal for balanced prevalence)
- Accuracy = prevalence × sensitivity + (1 - prevalence) × specificity

### Prevalence:
- Set to 50% (balanced design)
- Simplifies optimal threshold calculation
- For balanced prevalence, optimal threshold is at d'/2
