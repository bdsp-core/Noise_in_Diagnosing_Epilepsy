"""
Generate the "killer figure" showing two raters with different noise profiles.

VERSION 5: Larger AUC gap with more dramatic wasted potential
- Rater A: AUC = 0.78 (BETTER) BUT FPR=5% (conservative) → Accuracy = 62%
- Rater B: AUC = 0.70 (WORSE) BUT optimal threshold → Accuracy = 65%
- Wasted potential: 8.7 percentage points (if A used optimal threshold: 71%)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.special import expit
import os

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_cases = 30
n_occasions = 3
prevalence = 0.5  # Balanced prevalence

# Noise profiles - ADJUSTED for larger AUC gap
# Rater A: Very low discrimination noise (excellent ROC) BUT very conservative threshold
sigma_p_A = 0.17   # Very low pattern noise
sigma_o_A = 0.11   # Very low occasion noise
sigma_l_A = 2.0    # High level noise (bias)

# Rater B: Higher discrimination noise (worse ROC) BUT optimal threshold
sigma_p_B = 1.2    # High pattern noise
sigma_o_B = 0.8    # High occasion noise
sigma_l_B = 0.2    # Low level noise (unbiased)

# Signal (same for both)
sigma_c = 2.0

print("="*70)
print("NOISE DECOMPOSITION MODEL - VERSION 5 (LARGER AUC GAP)")
print("="*70)
print(f"\nRater A (Biased but Consistent):")
print(f"  Pattern noise:  σ_p = {sigma_p_A:.2f}")
print(f"  Occasion noise: σ_o = {sigma_o_A:.2f}")
print(f"  Level noise:    σ_l = {sigma_l_A:.1f} (BIASED - very conservative threshold)")
print(f"  Signal:         σ_c = {sigma_c:.1f}")

print(f"\nRater B (Unbiased but Erratic):")
print(f"  Pattern noise:  σ_p = {sigma_p_B:.2f}")
print(f"  Occasion noise: σ_o = {sigma_o_B:.2f}")
print(f"  Level noise:    σ_l = {sigma_l_B:.1f} (UNBIASED - optimal threshold)")
print(f"  Signal:         σ_c = {sigma_c:.1f}")

# Calculate discrimination noise (pattern + occasion)
sigma_disc_A = np.sqrt(sigma_p_A**2 + sigma_o_A**2)
sigma_disc_B = np.sqrt(sigma_p_B**2 + sigma_o_B**2)

print(f"\n{'='*70}")
print("ROC CURVES (determined by discrimination noise only)")
print("="*70)
print(f"Rater A: σ_disc = {sigma_disc_A:.3f} → BETTER discrimination")
print(f"Rater B: σ_disc = {sigma_disc_B:.3f} → WORSE discrimination")

# Target AUCs
target_auc_A = 0.78  # Rater A has BETTER discrimination
target_auc_B = 0.70  # Rater B has WORSE discrimination

# Calculate d' from target AUC
d_prime_A = norm.ppf(target_auc_A) * sigma_disc_A * np.sqrt(2)
d_prime_B = norm.ppf(target_auc_B) * sigma_disc_B * np.sqrt(2)

print(f"\nRater A: d' = {d_prime_A:.3f}, target AUC = {target_auc_A:.2f}")
print(f"Rater B: d' = {d_prime_B:.3f}, target AUC = {target_auc_B:.2f}")

def calculate_binormal_roc(sigma_disc, d_prime):
    """Calculate binormal ROC curve."""
    thresholds = np.linspace(-4, 4, 200)
    tpr = norm.cdf((d_prime - thresholds) / sigma_disc)
    fpr = norm.cdf(-thresholds / sigma_disc)

    sort_idx = np.argsort(fpr)
    fpr = fpr[sort_idx]
    tpr = tpr[sort_idx]

    auc = norm.cdf(d_prime / (sigma_disc * np.sqrt(2)))
    return fpr, tpr, auc

# Calculate ROC curves
fpr_A, tpr_A, auc_A = calculate_binormal_roc(sigma_disc_A, d_prime_A)
fpr_B, tpr_B, auc_B = calculate_binormal_roc(sigma_disc_B, d_prime_B)

print(f"\nActual AUCs:")
print(f"Rater A: {auc_A:.3f} (BETTER)")
print(f"Rater B: {auc_B:.3f} (WORSE)")
print(f"AUC GAP: {auc_A - auc_B:.2f}")

# Operating points
print(f"\n{'='*70}")
print("OPERATING POINTS (determined by level noise / bias)")
print("="*70)

# Rater A: Very conservative threshold at FPR = 5%
fpr_A_target = 0.05
spec_A = 1 - fpr_A_target
threshold_A = norm.ppf(spec_A) * sigma_disc_A
tpr_A_op = norm.cdf((d_prime_A - threshold_A) / sigma_disc_A)
acc_A = prevalence * tpr_A_op + (1 - prevalence) * spec_A

print(f"\nRater A (Very Conservative/Biased):")
print(f"  Threshold: {threshold_A:.3f} (very conservative, shifted by bias)")
print(f"  Sensitivity: {tpr_A_op:.3f}")
print(f"  Specificity: {spec_A:.3f}")
print(f"  FPR: {fpr_A_target:.3f}")
print(f"  Accuracy: {acc_A:.3f} ({acc_A*100:.1f}%)")

# Calculate OPTIMAL accuracy for Rater A (what they could achieve)
threshold_A_optimal = d_prime_A / 2
tpr_A_optimal = norm.cdf((d_prime_A - threshold_A_optimal) / sigma_disc_A)
fpr_A_optimal = norm.cdf(-threshold_A_optimal / sigma_disc_A)
spec_A_optimal = 1 - fpr_A_optimal
acc_A_optimal = prevalence * tpr_A_optimal + (1 - prevalence) * spec_A_optimal

print(f"\nRater A at OPTIMAL threshold (what they could achieve):")
print(f"  Threshold: {threshold_A_optimal:.3f}")
print(f"  Sensitivity: {tpr_A_optimal:.3f}")
print(f"  Specificity: {spec_A_optimal:.3f}")
print(f"  FPR: {fpr_A_optimal:.3f}")
print(f"  Accuracy: {acc_A_optimal:.3f} ({acc_A_optimal*100:.1f}%)")
print(f"  → WASTED POTENTIAL: {(acc_A_optimal - acc_A)*100:.1f} percentage points")

# Rater B: Optimal threshold
threshold_B = d_prime_B / 2
tpr_B_op = norm.cdf((d_prime_B - threshold_B) / sigma_disc_B)
fpr_B_op = norm.cdf(-threshold_B / sigma_disc_B)
spec_B = 1 - fpr_B_op
acc_B = prevalence * tpr_B_op + (1 - prevalence) * spec_B

print(f"\nRater B (Unbiased/Optimal):")
print(f"  Threshold: {threshold_B:.3f} (optimal)")
print(f"  Sensitivity: {tpr_B_op:.3f}")
print(f"  Specificity: {spec_B:.3f}")
print(f"  FPR: {fpr_B_op:.3f}")
print(f"  Accuracy: {acc_B:.3f} ({acc_B*100:.1f}%)")

print(f"\n{'='*70}")
print("KEY FINDING:")
print("="*70)
print(f"Rater A has BETTER discrimination (AUC={auc_A:.2f}) but LOWER accuracy ({acc_A*100:.1f}%)")
print(f"due to very conservative threshold choice.")
print(f"Rater B has WORSE discrimination (AUC={auc_B:.2f}) but HIGHER accuracy ({acc_B*100:.1f}%)")
print(f"due to optimal threshold choice.")
print(f"Rater A is wasting {(acc_A_optimal - acc_A)*100:.1f} percentage points of potential accuracy.")
print(f"AUC gap: {auc_A - auc_B:.2f} (larger than v4's 0.05)")
print("="*70)

# Generate simulated responses for heatmaps
def generate_rater_responses(n_cases, n_occasions, sigma_disc, d_prime, threshold, bias_shift):
    """Generate binary responses based on binormal model."""
    # Create case difficulties
    true_logits = np.linspace(-3, 3, n_cases)

    responses = np.zeros((n_cases, n_occasions), dtype=int)

    for t in range(n_occasions):
        # Add pattern noise (same across occasions for a given case)
        if t == 0:
            pattern_noise = np.random.normal(0, sigma_disc * 0.7, n_cases)

        # Add occasion noise (varies across occasions)
        occasion_noise = np.random.normal(0, sigma_disc * 0.3, n_cases)

        # Total logit with noise and bias
        logits = true_logits + bias_shift + pattern_noise + occasion_noise

        # Convert to probabilities and generate responses
        probs = expit(logits)
        responses[:, t] = (np.random.uniform(0, 1, n_cases) < probs).astype(int)

    return responses

# Generate responses with bias to achieve target operating points
bias_A = -1.2  # Very conservative bias (negative shift)
bias_B = 0.0   # No bias

responses_A = generate_rater_responses(n_cases, n_occasions, sigma_disc_A, d_prime_A, threshold_A, bias_A)
responses_B = generate_rater_responses(n_cases, n_occasions, sigma_disc_B, d_prime_B, threshold_B, bias_B)

# Gold standard (based on case difficulty)
gold_standard = np.concatenate([np.zeros(n_cases//2), np.ones(n_cases//2 + n_cases%2)]).astype(int)

# Create figure with 1x3 layout
fig = plt.figure(figsize=(14, 4.5))
gs = fig.add_gridspec(1, 3, wspace=0.0, width_ratios=[0.70, 1.3, 1])

cmap = plt.cm.gray_r  # White=0 (No), Black=1 (Yes)
boundary = n_cases // 2 - 0.5

# Panel A: Combined heatmaps (side by side within one subplot)
ax1 = fig.add_subplot(gs[0, 0])

# Create combined heatmap array with a small gap between A and B
gap_width = 1
combined_responses = np.hstack([responses_A,
                                 np.full((n_cases, gap_width), np.nan),
                                 responses_B])

# Plot combined heatmap with square aspect ratio
im = ax1.imshow(combined_responses, aspect='equal', cmap=cmap, vmin=0, vmax=1,
                interpolation='nearest')

# Add labels
ax1.set_xlabel('Occasion', fontsize=9)
ax1.set_ylabel('Cases (sorted by signal strength)', fontsize=9)

# X-ticks: show occasions for both raters
xtick_positions = list(range(n_occasions)) + [n_occasions + gap_width + i for i in range(n_occasions)]
xtick_labels = [f'{i+1}' for i in range(n_occasions)] + [f'{i+1}' for i in range(n_occasions)]
ax1.set_xticks(xtick_positions)
ax1.set_xticklabels(xtick_labels, fontsize=8)

# Y-ticks: Show signal strength from -5 (easy negative) to +5 (easy positive), with 0 at middle
# Map case indices to signal strength scale
# Case 0 (easiest negative) → -5
# Case n_cases//2 (boundary, most difficult) → 0
# Case n_cases-1 (easiest positive) → +5
ax1.set_yticks([0, n_cases//2, n_cases-1])
ax1.set_yticklabels(['-5', '0', '+5'], fontsize=8)

# Add gridlines to show individual cells
# Horizontal lines between rows
for i in range(n_cases + 1):
    ax1.axhline(y=i - 0.5, color='gray', linestyle='-', linewidth=0.3, alpha=0.5)

# Vertical lines between columns (for both raters)
total_cols = n_occasions * 2 + gap_width
for i in range(total_cols + 1):
    ax1.axvline(x=i - 0.5, color='gray', linestyle='-', linewidth=0.3, alpha=0.5)

# Boundary line (thicker, dotted)
ax1.axhline(y=boundary, color='black', linestyle=':', linewidth=1.2, alpha=0.6)

# Vertical line to separate raters (thicker)
ax1.axvline(x=n_occasions - 0.5, color='black', linestyle='-', linewidth=2)

# Add thick black border around each heatmap
# Rater A borders
ax1.axhline(y=-0.5, color='black', linestyle='-', linewidth=2)  # Top
ax1.axhline(y=n_cases - 0.5, color='black', linestyle='-', linewidth=2)  # Bottom
ax1.axvline(x=-0.5, color='black', linestyle='-', linewidth=2)  # Left
ax1.axvline(x=n_occasions - 0.5, color='black', linestyle='-', linewidth=2)  # Right (shared with separator)

# Rater B borders
ax1.axhline(y=-0.5, color='black', linestyle='-', linewidth=2)  # Top (shared)
ax1.axhline(y=n_cases - 0.5, color='black', linestyle='-', linewidth=2)  # Bottom (shared)
ax1.axvline(x=n_occasions + gap_width - 0.5, color='black', linestyle='-', linewidth=2)  # Left (shared with separator)
ax1.axvline(x=total_cols - 0.5, color='black', linestyle='-', linewidth=2)  # Right

# Add rater labels centered above each heatmap section - positioned just above the heatmaps
# Use blended transform: data coords for x (column position), axes coords for y (above plot)
# Offset the labels more to add more spacing between them
from matplotlib.transforms import blended_transform_factory
trans = blended_transform_factory(ax1.transData, ax1.transAxes)
mid_A = (n_occasions - 1) / 2 - 0.6  # Center of Rater A section, shifted left more
mid_B = n_occasions + gap_width + (n_occasions - 1) / 2 + 0.6  # Center of Rater B section, shifted right more
ax1.text(mid_A, 1.02, 'Rater A', ha='center', va='bottom',
         fontsize=9, fontweight='bold', transform=trans)
ax1.text(mid_B, 1.02, 'Rater B', ha='center', va='bottom',
         fontsize=9, fontweight='bold', transform=trans)

# Title
ax1.text(0.5, 1.08, 'A. Responses',
         transform=ax1.transAxes, ha='center', fontsize=10, fontweight='bold')

# Panel B: ROC curves
ax2 = fig.add_subplot(gs[0, 1])

# Plot ROC curves
ax2.plot(fpr_A, tpr_A, 'k-', linewidth=2.5, alpha=0.8)
ax2.plot(fpr_B, tpr_B, 'k--', linewidth=2.5, alpha=0.8)
ax2.plot([0, 1], [0, 1], 'k:', linewidth=1, alpha=0.4)

# Operating points
ax2.plot(fpr_A_target, tpr_A_op, 'ko', markersize=8, markerfacecolor='white',
         markeredgewidth=2, zorder=10)
ax2.plot(fpr_B_op, tpr_B_op, 'ko', markersize=8, markerfacecolor='black',
         markeredgewidth=2, zorder=10)

# Simple labels on curves
# Rater A (solid line) has higher AUC (0.78), curve is above
# Rater B (dashed line) has lower AUC (0.70), curve is below
# Position labels clearly on their respective curves
ax2.text(0.40, 0.82, 'Rater A',
         fontsize=9, rotation=20, ha='center', style='italic', color='black')
ax2.text(0.55, 0.66, 'Rater B',
         fontsize=9, rotation=15, ha='center', style='italic', color='black')
ax2.text(0.55, 0.48, 'Chance', fontsize=9, rotation=45, alpha=0.6, style='italic')

# Add legend in lower right with AUC and Acc information (no border)
legend_text = f'Rater A: AUC={auc_A:.2f}, Acc={acc_A:.0%}\nRater B: AUC={auc_B:.2f}, Acc={acc_B:.0%}'
ax2.text(0.98, 0.08, legend_text, ha='right', va='bottom',
         fontsize=8.5, bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
         edgecolor='none', alpha=0.95),
         transform=ax2.transAxes)

ax2.set_xlabel('False Positive Rate', fontsize=9)
ax2.set_ylabel('True Positive Rate (Sensitivity)', fontsize=9)
ax2.set_aspect('equal', adjustable='box')
ax2.set_xlim([0, 1])
ax2.set_ylim([0, 1])
ax2.grid(True, alpha=0.2, linewidth=0.5)
ax2.set_axisbelow(True)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

ax2.text(0.5, 1.08, 'B. ROC Curves',
         transform=ax2.transAxes, ha='center', fontsize=10, fontweight='bold')

# Panel C: Variance decomposition
ax3 = fig.add_subplot(gs[0, 2])

# Calculate variance percentages
total_var_A = sigma_c**2 + sigma_l_A**2 + sigma_p_A**2 + sigma_o_A**2
total_var_B = sigma_c**2 + sigma_l_B**2 + sigma_p_B**2 + sigma_o_B**2

pct_c_A = (sigma_c**2 / total_var_A) * 100
pct_l_A = (sigma_l_A**2 / total_var_A) * 100
pct_p_A = (sigma_p_A**2 / total_var_A) * 100
pct_o_A = (sigma_o_A**2 / total_var_A) * 100

pct_c_B = (sigma_c**2 / total_var_B) * 100
pct_l_B = (sigma_l_B**2 / total_var_B) * 100
pct_p_B = (sigma_p_B**2 / total_var_B) * 100
pct_o_B = (sigma_o_B**2 / total_var_B) * 100

x = np.arange(2)
width = 0.7  # Increased from 0.5 to reduce white space

# Stacked bars
ax3.bar(x, [pct_c_A, pct_c_B], width, color='0.95', edgecolor='black', linewidth=0.5)
ax3.bar(x, [pct_l_A, pct_l_B], width, bottom=[pct_c_A, pct_c_B],
       color='0.25', edgecolor='black', linewidth=0.5)
ax3.bar(x, [pct_p_A, pct_p_B], width, bottom=[pct_c_A+pct_l_A, pct_c_B+pct_l_B],
       color='0.50', edgecolor='black', linewidth=0.5)
ax3.bar(x, [pct_o_A, pct_o_B], width, bottom=[pct_c_A+pct_l_A+pct_p_A, pct_c_B+pct_l_B+pct_p_B],
       color='0.75', edgecolor='black', linewidth=0.5)

ax3.set_ylabel('% of Total Variance', fontsize=9)
ax3.set_xticks(x)
ax3.set_xticklabels(['Rater A', 'Rater B'], fontsize=9)
ax3.set_ylim([0, 100])
ax3.grid(True, axis='y', alpha=0.2, linewidth=0.5)
ax3.set_axisbelow(True)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

# Direct labels on bars
for i, (c, l, p, o) in enumerate([(pct_c_A, pct_l_A, pct_p_A, pct_o_A),
                                     (pct_c_B, pct_l_B, pct_p_B, pct_o_B)]):
    if c > 8:
        ax3.text(i, c/2, f'Signal\n{c:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='normal')
    if l > 8:
        ax3.text(i, c + l/2, f'Level\n{l:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='normal', color='white')
    if p > 8:
        ax3.text(i, c + l + p/2, f'Pattern\n{p:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='normal')
    if o > 8:
        ax3.text(i, c + l + p + o/2, f'Occasion\n{o:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='normal')

# Intervention annotations
ax3.text(0, -15, '→ Threshold\ncalibration', ha='center', va='top', fontsize=7.5,
         style='italic', transform=ax3.transData)
ax3.text(1, -15, '→ Training +\ndecision aids', ha='center', va='top', fontsize=7.5,
         style='italic', transform=ax3.transData)

ax3.text(0.5, 1.08, 'C. Variance Decomposition',
         transform=ax3.transAxes, ha='center', fontsize=10, fontweight='bold')

# Manually adjust subplot positions to eliminate white space
# Get current positions and squeeze them together
pos1 = ax1.get_position()
pos2 = ax2.get_position()
pos3 = ax3.get_position()

# Move panel B to start right where panel A ends (with small gap for y-label)
ax2.set_position([pos1.x1 + 0.06, pos2.y0, pos2.width, pos2.height])
# Update pos2 to reflect the new position
pos2 = ax2.get_position()
# Move panel C to start right where panel B ends
ax3.set_position([pos2.x1 + 0.05, pos3.y0, pos3.width, pos3.height])

# Save figure - do NOT use tight_layout() or bbox_inches='tight' as they override wspace
output_dir = "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/Noise_in_Diagnosing_Epilepsy"
output_path = os.path.join(output_dir, "killer_figure.pdf")
plt.savefig(output_path, dpi=300, pad_inches=0.1)
print(f"\nFigure saved to: {output_path}")

output_path_png = output_path.replace('.pdf', '.png')
plt.savefig(output_path_png, dpi=300, pad_inches=0.1)
print(f"PNG version saved to: {output_path_png}")

plt.close()

print("\n" + "="*70)
print("FIGURE GENERATION COMPLETE - VERSION 5")
print("="*70)
print(f"✓ AUC gap increased to {auc_A - auc_B:.2f} (from 0.05)")
print(f"✓ Wasted potential increased to {(acc_A_optimal - acc_A)*100:.1f} points (from 5)")
print(f"✓ FPR = {fpr_A_target:.0%} (still visible, more dramatic)")
print("="*70)
