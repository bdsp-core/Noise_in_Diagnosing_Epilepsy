#!/usr/bin/env python3
"""
Case Study: Spikes Dataset Analysis

This script analyzes the spikes dataset to estimate:
- Level noise for each participant
- Skill level for each participant
- Question difficulties

Uses SSIT model (appropriate for single-occasion data).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add parent directory to path to import our library
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from noise_analysis_lib import (
    prepare_data_for_analysis,
    run_noise_analysis,
    compute_descriptive_stats,
    compute_roc_points,
    extract_participant_estimates,
    extract_item_difficulties,
    plot_variance_decomposition,
    plot_roc_curves,
    save_results_summary
)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*70)
print("SPIKES DATASET ANALYSIS")
print("="*70)

# =============================================================================
# 1. LOAD DATA
# =============================================================================

print("\n1. Loading data...")

data_dir = "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/spikes"

# Load the three files
expertise_df = pd.read_csv(f"{data_dir}/expertise_spikes.csv")
y_answers_df = pd.read_csv(f"{data_dir}/y_answers_spikes.csv")
y_prob_df = pd.read_csv(f"{data_dir}/y_prob_spikes.csv")

print(f"\nData dimensions:")
print(f"  Expertise: {expertise_df.shape}")
print(f"  True answers: {y_answers_df.shape}")
print(f"  Participant responses: {y_prob_df.shape}")

# Extract arrays
expertise = expertise_df.values.flatten()
y_answers = y_answers_df.values  # (1000, 37) or (1000,)
y_prob = y_prob_df.values  # (1000, 37)

print(f"\nExpertise levels: {np.unique(expertise)}")
print(f"Expertise counts: {np.bincount(expertise.astype(int))}")

# =============================================================================
# 2. DESCRIPTIVE STATISTICS
# =============================================================================

print("\n" + "="*70)
print("2. DESCRIPTIVE STATISTICS")
print("="*70)

stats_df = compute_descriptive_stats(
    y_prob=y_prob,
    y_answers=y_answers,
    expertise=expertise,
    threshold=0.5
)

print("\nAccuracy by Expertise Level:")
print(stats_df.to_string(index=False))

# =============================================================================
# 3. ROC OPERATING POINTS
# =============================================================================

print("\n" + "="*70)
print("3. ROC OPERATING POINTS")
print("="*70)

roc_df = compute_roc_points(
    y_prob=y_prob,
    y_answers=y_answers,
    expertise=expertise,
    threshold=0.5
)

print("\nROC Points by Expertise (showing first 10):")
print(roc_df.head(10).to_string(index=False))

# Summary by group
print("\nROC Summary by Expertise:")
roc_summary = roc_df.groupby('expertise').agg({
    'tpr': ['mean', 'std', 'min', 'max'],
    'fpr': ['mean', 'std', 'min', 'max'],
    'accuracy': ['mean', 'std', 'min', 'max']
})
print(roc_summary)

# =============================================================================
# 4. PREPARE DATA FOR NOISE ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("4. PREPARING DATA FOR NOISE ANALYSIS")
print("="*70)

# Convert to long format for analysis
df = prepare_data_for_analysis(
    y_prob=y_prob,
    y_answers=y_answers,
    expertise=expertise,
    occasion=1,
    threshold=0.5
)

print(f"\nPrepared data shape: {df.shape}")
print("\nFirst few rows:")
print(df.head(10))

print(f"\nData summary:")
print(f"  Number of participants: {df['id'].nunique()}")
print(f"  Number of items: {df['item'].nunique()}")
print(f"  Number of observations: {len(df)}")
print(f"  Proportion of Y=1: {df['Y'].mean():.3f}")

# =============================================================================
# 5. RUN SSIT MODEL ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("5. RUNNING SSIT MODEL ANALYSIS")
print("="*70)

print("\nThis will take several minutes...")
print("Using SSIT model (appropriate for single-occasion data)")

results = run_noise_analysis(
    df=df,
    model_type="SSIT",
    save_prefix="spikes",
    draws=5000,
    tune=2000,
    chains=10,
    cores=6,
    target_accept=0.98,
    random_seed=42
)

print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)

# =============================================================================
# 6. EXTRACT PARTICIPANT-LEVEL ESTIMATES
# =============================================================================

print("\n" + "="*70)
print("6. PARTICIPANT-LEVEL ESTIMATES")
print("="*70)

participant_df = extract_participant_estimates(results, df)

print("\nParticipant estimates (first 10):")
print(participant_df.head(10).to_string(index=False))

# Summary by expertise
print("\nLevel Noise by Expertise:")
ln_summary = participant_df.groupby('expertise')['level_noise'].agg([
    'count', 'mean', 'std', 'min', 'max'
])
print(ln_summary)

# =============================================================================
# 7. EXTRACT ITEM DIFFICULTIES
# =============================================================================

print("\n" + "="*70)
print("7. ITEM DIFFICULTY ESTIMATES")
print("="*70)

item_df = extract_item_difficulties(results)

print(f"\nExtracted difficulties for {len(item_df)} items")
print("\nDifficulty distribution:")
print(item_df['difficulty'].describe())

print("\nEasiest items (most negative difficulty):")
print(item_df.nsmallest(5, 'difficulty')[['item_id', 'difficulty']].to_string(index=False))

print("\nHardest items (most positive difficulty):")
print(item_df.nlargest(5, 'difficulty')[['item_id', 'difficulty']].to_string(index=False))

# =============================================================================
# 8. VISUALIZATIONS
# =============================================================================

print("\n" + "="*70)
print("8. CREATING VISUALIZATIONS")
print("="*70)

# Create output directory for plots
os.makedirs("spikes_analysis_output", exist_ok=True)

# Plot 1: Variance Decomposition
print("\nCreating variance decomposition plot...")
fig1, ax1 = plot_variance_decomposition(
    results,
    title="Spikes Dataset: Variance Decomposition (SSIT Model)"
)
fig1.savefig("spikes_analysis_output/variance_decomposition.png", dpi=300, bbox_inches='tight')
plt.close(fig1)

# Plot 2: ROC Curves by Expertise
print("Creating ROC curves...")
fig2, ax2 = plot_roc_curves(roc_df, group_by='expertise', figsize=(10, 8))
fig2.savefig("spikes_analysis_output/roc_curves.png", dpi=300, bbox_inches='tight')
plt.close(fig2)

# Plot 3: Level Noise by Expertise
print("Creating level noise boxplot...")
fig3, ax3 = plt.subplots(figsize=(10, 6))
expertise_labels = {1: 'Experts', 2: 'Experienced', 3: 'Novices'}
participant_df['expertise_label'] = participant_df['expertise'].map(expertise_labels)

sns.boxplot(data=participant_df, x='expertise_label', y='level_noise',
           order=['Experts', 'Experienced', 'Novices'], ax=ax3)
sns.swarmplot(data=participant_df, x='expertise_label', y='level_noise',
             order=['Experts', 'Experienced', 'Novices'],
             color='black', alpha=0.5, ax=ax3)

ax3.set_xlabel('Expertise Level', fontsize=12)
ax3.set_ylabel('Level Noise (Bias)', fontsize=12)
ax3.set_title('Level Noise Distribution by Expertise', fontsize=14, fontweight='bold')
ax3.axhline(0, color='red', linestyle='--', alpha=0.5, label='No bias')
ax3.legend()
ax3.grid(alpha=0.3)
plt.tight_layout()
fig3.savefig("spikes_analysis_output/level_noise_by_expertise.png", dpi=300, bbox_inches='tight')
plt.close(fig3)

# Plot 4: Item Difficulty Distribution
print("Creating item difficulty histogram...")
fig4, ax4 = plt.subplots(figsize=(10, 6))
ax4.hist(item_df['difficulty'], bins=50, alpha=0.7, edgecolor='black')
ax4.axvline(0, color='red', linestyle='--', linewidth=2, label='Neutral difficulty')
ax4.set_xlabel('Item Difficulty (Signal Strength)', fontsize=12)
ax4.set_ylabel('Count', fontsize=12)
ax4.set_title('Distribution of Item Difficulties', fontsize=14, fontweight='bold')
ax4.legend()
ax4.grid(alpha=0.3)
plt.tight_layout()
fig4.savefig("spikes_analysis_output/item_difficulty_distribution.png", dpi=300, bbox_inches='tight')
plt.close(fig4)

# Plot 5: Accuracy vs Level Noise
print("Creating accuracy vs level noise scatter plot...")
# Merge ROC data with participant estimates
merged_df = participant_df.merge(
    roc_df[['rater_id', 'accuracy', 'tpr', 'fpr']],
    on='rater_id',
    how='left'
)

fig5, ax5 = plt.subplots(figsize=(10, 6))
for expertise_level in sorted(merged_df['expertise'].unique()):
    group_data = merged_df[merged_df['expertise'] == expertise_level]
    ax5.scatter(group_data['level_noise'], group_data['accuracy'],
               alpha=0.7, s=100, label=f'{expertise_labels[expertise_level]}')

ax5.set_xlabel('Level Noise (Bias)', fontsize=12)
ax5.set_ylabel('Accuracy', fontsize=12)
ax5.set_title('Accuracy vs Level Noise by Expertise', fontsize=14, fontweight='bold')
ax5.axvline(0, color='red', linestyle='--', alpha=0.3, label='No bias')
ax5.legend()
ax5.grid(alpha=0.3)
plt.tight_layout()
fig5.savefig("spikes_analysis_output/accuracy_vs_level_noise.png", dpi=300, bbox_inches='tight')
plt.close(fig5)

print("\nAll plots saved to: spikes_analysis_output/")

# =============================================================================
# 9. SAVE RESULTS
# =============================================================================

print("\n" + "="*70)
print("9. SAVING RESULTS")
print("="*70)

# Save comprehensive summary
save_results_summary(
    results=results,
    participant_df=participant_df,
    item_df=item_df,
    stats_df=stats_df,
    roc_df=roc_df,
    output_file="spikes_analysis_output/spikes_analysis_summary.xlsx"
)

# Also save individual CSVs
participant_df.to_csv("spikes_analysis_output/participant_estimates.csv", index=False)
item_df.to_csv("spikes_analysis_output/item_difficulties.csv", index=False)
stats_df.to_csv("spikes_analysis_output/descriptive_stats.csv", index=False)
roc_df.to_csv("spikes_analysis_output/roc_points.csv", index=False)

print("\nIndividual CSV files also saved.")

# =============================================================================
# 10. SUMMARY REPORT
# =============================================================================

print("\n" + "="*70)
print("SUMMARY REPORT")
print("="*70)

print("\n### Variance Decomposition ###")
vd = results['variance_decomposition']
print(f"Signal (item difficulty):  {vd['perc_c']:.1f}%")
print(f"Level Noise (bias):        {vd['perc_l']:.1f}%")
print(f"Residual (other noise):    {vd['perc_p']:.1f}%")

print("\n### Effective Scales ###")
scales = results['effective_scales']
print(f"Signal:        σ_c = {scales['S_est']:.3f}")
print(f"Level Noise:   σ_l = {scales['LN_est']:.3f}")
print(f"Residual:      σ_r = {scales['PN_est']:.3f}")
print(f"Population Skill: s = {1/scales['PN_est']:.3f}")

print("\n### Accuracy by Expertise ###")
for _, row in stats_df.iterrows():
    level = expertise_labels[int(row['expertise_level'])]
    print(f"{level:12s}: {row['median_accuracy']:.3f} [{row['accuracy_range_min']:.3f}, {row['accuracy_range_max']:.3f}]")

print("\n### Level Noise by Expertise ###")
for expertise_level in sorted(participant_df['expertise'].unique()):
    group_data = participant_df[participant_df['expertise'] == expertise_level]
    level = expertise_labels[expertise_level]
    mean_ln = group_data['level_noise'].mean()
    std_ln = group_data['level_noise'].std()
    print(f"{level:12s}: {mean_ln:+.3f} ± {std_ln:.3f}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("="*70)
print("\nOutput files:")
print("  - spikes_analysis_output/spikes_analysis_summary.xlsx")
print("  - spikes_analysis_output/participant_estimates.csv")
print("  - spikes_analysis_output/item_difficulties.csv")
print("  - spikes_analysis_output/variance_decomposition.png")
print("  - spikes_analysis_output/roc_curves.png")
print("  - spikes_analysis_output/level_noise_by_expertise.png")
print("  - spikes_analysis_output/item_difficulty_distribution.png")
print("  - spikes_analysis_output/accuracy_vs_level_noise.png")
print("="*70 + "\n")
