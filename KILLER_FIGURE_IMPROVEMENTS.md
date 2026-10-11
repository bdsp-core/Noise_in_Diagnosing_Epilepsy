# Killer Figure Improvements (Version 2)

## Problems Fixed

### 1. **ROC Curves Now Use Binormal Model**
   - **Old**: Empirical ROC curves calculated from discrete threshold sweeps (lines 144-165 in v1)
   - **New**: Smooth theoretical curves using the binormal signal detection model described in the paper
   - **Method**: Uses `calculate_binormal_roc()` function based on:
     ```
     TPR = Φ((d' - threshold) / σ)
     FPR = Φ(-threshold / σ)
     AUC = Φ(d' / (σ√2))
     ```
   - **Result**: Smooth, publication-quality curves that match the paper's theoretical framework

### 2. **Black and White Color Scheme**
   - **Old**: Red-blue colormap for heatmaps, colored lines for ROC curves
   - **New**: Grayscale throughout
     - Heatmaps: `gray_r` (white=No, black=Yes)
     - ROC curves: solid black line (Rater A), dashed black line (Rater B)
     - Variance bars: Three shades of gray (0.3, 0.6, 0.85)
   - **Result**: Publication-ready for journals that don't accept color

### 3. **Square Aspect Ratio for ROC Plot**
   - **Old**: ROC curve in rectangular box (misleading geometry)
   - **New**: `ax.set_aspect('equal', adjustable='box')` enforces square plot
   - **Result**: Proper representation of ROC space where FPR and TPR have equal scaling

### 4. **Tufte-Style Annotations**
   - **Old**: Traditional legends and titles separated from data
   - **New**: Edward Tufte principles applied:
     - Text annotations placed directly on/near elements
     - "True boundary" label appears right next to the dotted line
     - Rater names annotated directly on ROC curves
     - Intervention recommendations placed below bars
     - Titles integrated as text annotations above subplots
   - **Result**: Higher data-ink ratio, less eye movement needed

### 5. **Minimal Chartjunk Removed**
   - Removed top and right spines from ROC and variance plots
   - Lightened grid lines (alpha=0.2)
   - Removed tick marks from colorbar
   - Simplified colorbar to just essential labels (No/Yes)
   - Clean, professional appearance

## Key Technical Details

### Binormal Model Implementation

The ROC curves are now calculated using the signal detection theory binormal model:

- **Total noise**: σ_total = √(σ_p² + σ_o²)
- **Discriminability**: d' = 2 × Φ⁻¹(target_sensitivity) × σ_total
- **ROC curve**: Parameterized by threshold τ
  - TPR(τ) = Φ((d' - τ) / σ)
  - FPR(τ) = Φ(-τ / σ)
- **AUC**: Φ(d' / (σ√2))

This matches exactly the methodology described in Section "ROC curves, skill, and noise in SSIT" of the paper.

### Color Palette

Grayscale values chosen for maximum contrast while remaining printable:
- Level noise: 0.3 (dark gray)
- Pattern noise: 0.6 (medium gray)
- Occasion noise: 0.85 (light gray)
- All with black edges for clarity

## Files

- **generate_killer_figure_v2.py**: New improved version (use this going forward)
- **generate_killer_figure.py**: Original version (preserved for reference)
- **killer_figure.pdf**: Output figure in PDF format (vector graphics)
- **killer_figure.png**: Output figure in PNG format (high-res raster, 300 dpi)

## Usage

```bash
cd "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/Noise_in_Diagnosing_Epilepsy"
python generate_killer_figure_v2.py
```

Output files will be overwritten in the same directory.
