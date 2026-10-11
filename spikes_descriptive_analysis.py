#!/usr/bin/env python3
"""
Spikes Dataset - Descriptive Analysis
(Does not require PyMC - can run standalone)

This script performs descriptive statistics and data preparation for the spikes dataset.
The prepared data can then be analyzed using the SSIT model in a Jupyter environment.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

print("="*70)
print("SPIKES DATASET - DESCRIPTIVE ANALYSIS")
print("="*70)

# =============================================================================
# 1. LOAD DATA
# =============================================================================

print("\n### 1. Loading Data ###\n")

data_dir = "/Users/bwestove/cdac Dropbox/brandon westover/0_People/temp_people/fabio/KILT_technical/spikes"

# Load the three files (no header in these CSVs)
expertise_df = pd.read_csv(f"{data_dir}/expertise_spikes.csv", header=None)
y_answers_df = pd.read_csv(f"{data_dir}/y_answers_spikes.csv", header=None)
y_prob_df = pd.read_csv(f"{data_dir}/y_prob_spikes.csv", header=None)

print(f"Data dimensions:")
print(f"  Expertise:            {expertise_df.shape}")
print(f"  True answers:         {y_answers_df.shape}")
print(f"  Participant responses: {y_prob_df.shape}")

# Extract arrays
expertise = expertise_df.values.flatten()
y_answers = y_answers_df.values
y_prob = y_prob_df.values

# Handle y_answers dimensions
if y_answers.ndim == 2:
    if y_answers.shape[1] == 1:
        y_true = y_answers.flatten()
    else:
        y_true = y_answers.mean(axis=1)  # Average if multiple columns
else:
    y_true = y_answers

# Convert to binary (threshold at 0.5)
threshold = 0.5
y_true_binary = (y_true >= threshold).astype(int)
y_pred_binary = (y_prob >= threshold).astype(int)

n_items, n_raters = y_prob.shape

print(f"\nProcessed dimensions:")
print(f"  Items (questions):    {n_items}")
print(f"  Raters (participants): {n_raters}")
print(f"  Expertise levels:      {np.unique(expertise)}")

# Map expertise levels to labels (0-indexed: 0=Experts, 1=Experienced, 2=Novices)
expertise_labels = {0: 'Experts', 1: 'Experienced', 2: 'Novices'}
print(f"\nExpertise distribution:")
for level in sorted(np.unique(expertise)):
    count = (expertise == level).sum()
    print(f"  {expertise_labels[level]:12s}: {count} participants")

# =============================================================================
# 2. DESCRIPTIVE STATISTICS BY EXPERTISE GROUP
# =============================================================================

print("\n" + "="*70)
print("### 2. Descriptive Statistics by Expertise Group ###")
print("="*70 + "\n")

# Compute accuracy for each participant
accuracies = np.zeros(n_raters)
for i in range(n_raters):
    accuracies[i] = (y_pred_binary[:, i] == y_true_binary).mean()

# Group by expertise
stats_list = []
for level in sorted(np.unique(expertise)):
    mask = expertise == level
    group_acc = accuracies[mask]

    stats_list.append({
        'Expertise': expertise_labels[level],
        'N': mask.sum(),
        'Median Accuracy': np.median(group_acc),
        'Range Min': np.min(group_acc),
        'Range Max': np.max(group_acc),
        'Mean Accuracy': np.mean(group_acc),
        'Std Accuracy': np.std(group_acc)
    })

stats_df = pd.DataFrame(stats_list)
print("Accuracy by Expertise Level:")
print(stats_df.to_string(index=False))

# =============================================================================
# 3. ROC OPERATING POINTS
# =============================================================================

print("\n" + "="*70)
print("### 3. ROC Operating Points ###")
print("="*70 + "\n")

# Compute operating point for each participant
roc_list = []
for i in range(n_raters):
    y_pred = y_pred_binary[:, i]

    # Confusion matrix
    tn, fp, fn, tp = confusion_matrix(y_true_binary, y_pred).ravel()

    # Compute rates
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # Sensitivity
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # 1 - Specificity
    tnr = tn / (tn + fp) if (tn + fp) > 0 else 0  # Specificity
    fnr = fn / (fn + tp) if (fn + tp) > 0 else 0  # 1 - Sensitivity
    acc = (tp + tn) / (tp + tn + fp + fn)

    roc_list.append({
        'Rater ID': i + 1,
        'Expertise': expertise_labels[expertise[i]],
        'Expertise Level': expertise[i],
        'Sensitivity (TPR)': tpr,
        'FPR': fpr,
        'Specificity (TNR)': tnr,
        'FNR': fnr,
        'Accuracy': acc
    })

roc_df = pd.DataFrame(roc_list)

print("First 10 participants:")
print(roc_df.head(10)[['Rater ID', 'Expertise', 'Sensitivity (TPR)', 'FPR', 'Accuracy']].to_string(index=False))

# Summary by expertise
print("\nROC Summary by Expertise:")
roc_summary = roc_df.groupby('Expertise').agg({
    'Sensitivity (TPR)': ['mean', 'std'],
    'FPR': ['mean', 'std'],
    'Accuracy': ['mean', 'std']
})
print(roc_summary)

# =============================================================================
# 4. PREPARE DATA FOR NOISE ANALYSIS
# =============================================================================

print("\n" + "="*70)
print("### 4. Preparing Data for SSIT Model ###")
print("="*70 + "\n")

# Convert to long format
data_list = []
for rater_idx in range(n_raters):
    for item_idx in range(n_items):
        data_list.append({
            'id': rater_idx + 1,
            'item': item_idx + 1,
            't': 1,  # Single occasion
            'Y': int(y_pred_binary[item_idx, rater_idx]),
            'expertise': expertise[rater_idx],
            'true_answer': y_true_binary[item_idx]
        })

analysis_df = pd.DataFrame(data_list)

print(f"Prepared data for analysis:")
print(f"  Shape: {analysis_df.shape}")
print(f"  Participants: {analysis_df['id'].nunique()}")
print(f"  Items: {analysis_df['item'].nunique()}")
print(f"  Total observations: {len(analysis_df)}")
print(f"  Proportion Y=1: {analysis_df['Y'].mean():.3f}")

print("\nFirst 10 rows:")
print(analysis_df.head(10).to_string(index=False))

# Save for analysis
os.makedirs("spikes_analysis_output", exist_ok=True)
analysis_df[['id', 'item', 't', 'Y']].to_csv(
    "spikes_analysis_output/spikes_data_for_analysis.csv",
    index=False
)
print("\nData saved to: spikes_analysis_output/spikes_data_for_analysis.csv")

# =============================================================================
# 5. VISUALIZATIONS
# =============================================================================

print("\n" + "="*70)
print("### 5. Creating Visualizations ###")
print("="*70 + "\n")

# Create output directory
os.makedirs("spikes_analysis_output", exist_ok=True)

# Plot 1: Accuracy by Expertise
print("Creating accuracy boxplot...")
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Prepare data for plotting
plot_data = pd.DataFrame({
    'Expertise': [expertise_labels[e] for e in expertise],
    'Accuracy': accuracies
})

sns.boxplot(data=plot_data, x='Expertise', y='Accuracy',
           order=['Experts', 'Experienced', 'Novices'], ax=ax1)
sns.swarmplot(data=plot_data, x='Expertise', y='Accuracy',
             order=['Experts', 'Experienced', 'Novices'],
             color='black', alpha=0.5, ax=ax1)

ax1.set_xlabel('Expertise Level', fontsize=14)
ax1.set_ylabel('Accuracy', fontsize=14)
ax1.set_title('Accuracy Distribution by Expertise Level', fontsize=16, fontweight='bold')
ax1.grid(alpha=0.3, axis='y')
plt.tight_layout()
fig1.savefig("spikes_analysis_output/accuracy_by_expertise.png", dpi=300, bbox_inches='tight')
plt.close(fig1)

# Plot 2: ROC Operating Points
print("Creating ROC operating points plot...")
fig2, ax2 = plt.subplots(figsize=(10, 8))

colors = {'Experts': '#2E86AB', 'Experienced': '#F18F01', 'Novices': '#C73E1D'}

for expertise_group in ['Experts', 'Experienced', 'Novices']:
    group_data = roc_df[roc_df['Expertise'] == expertise_group]

    # Plot individual points
    ax2.scatter(group_data['FPR'], group_data['Sensitivity (TPR)'],
               alpha=0.6, color=colors[expertise_group], s=100,
               label=f'{expertise_group} (n={len(group_data)})')

    # Plot group mean as star
    mean_fpr = group_data['FPR'].mean()
    mean_tpr = group_data['Sensitivity (TPR)'].mean()
    ax2.scatter(mean_fpr, mean_tpr,
               color=colors[expertise_group], s=400, marker='*',
               edgecolors='black', linewidths=2, zorder=10)

# Diagonal reference line
ax2.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.3, label='Chance')

ax2.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=14)
ax2.set_ylabel('True Positive Rate (Sensitivity)', fontsize=14)
ax2.set_title('ROC Operating Points by Expertise Level', fontsize=16, fontweight='bold')
ax2.set_xlim([-0.05, 1.05])
ax2.set_ylim([-0.05, 1.05])
ax2.legend(loc='lower right', fontsize=12)
ax2.grid(alpha=0.3)
ax2.set_aspect('equal')
plt.tight_layout()
fig2.savefig("spikes_analysis_output/roc_operating_points.png", dpi=300, bbox_inches='tight')
plt.close(fig2)

# Plot 3: Sensitivity vs Specificity
print("Creating sensitivity vs specificity plot...")
fig3, ax3 = plt.subplots(figsize=(10, 8))

for expertise_group in ['Experts', 'Experienced', 'Novices']:
    group_data = roc_df[roc_df['Expertise'] == expertise_group]

    ax3.scatter(group_data['Specificity (TNR)'], group_data['Sensitivity (TPR)'],
               alpha=0.6, color=colors[expertise_group], s=100,
               label=f'{expertise_group}')

    # Mean
    mean_spec = group_data['Specificity (TNR)'].mean()
    mean_sens = group_data['Sensitivity (TPR)'].mean()
    ax3.scatter(mean_spec, mean_sens,
               color=colors[expertise_group], s=400, marker='*',
               edgecolors='black', linewidths=2, zorder=10)

ax3.set_xlabel('Specificity', fontsize=14)
ax3.set_ylabel('Sensitivity', fontsize=14)
ax3.set_title('Sensitivity vs Specificity by Expertise', fontsize=16, fontweight='bold')
ax3.set_xlim([0, 1.05])
ax3.set_ylim([0, 1.05])
ax3.legend(loc='lower left', fontsize=12)
ax3.grid(alpha=0.3)
ax3.set_aspect('equal')
plt.tight_layout()
fig3.savefig("spikes_analysis_output/sensitivity_vs_specificity.png", dpi=300, bbox_inches='tight')
plt.close(fig3)

print("\nPlots saved to spikes_analysis_output/")

# =============================================================================
# 6. SAVE RESULTS
# =============================================================================

print("\n" + "="*70)
print("### 6. Saving Results ###")
print("="*70 + "\n")

# Save to Excel
with pd.ExcelWriter("spikes_analysis_output/spikes_descriptive_stats.xlsx") as writer:
    stats_df.to_excel(writer, sheet_name='Accuracy_by_Expertise', index=False)
    roc_df.to_excel(writer, sheet_name='ROC_Points', index=False)
    roc_summary.to_excel(writer, sheet_name='ROC_Summary')

print("Results saved to: spikes_analysis_output/spikes_descriptive_stats.xlsx")

# Save individual CSVs
stats_df.to_csv("spikes_analysis_output/accuracy_stats.csv", index=False)
roc_df.to_csv("spikes_analysis_output/roc_points.csv", index=False)

print("Individual CSV files also saved.")

# =============================================================================
# 7. SUMMARY
# =============================================================================

print("\n" + "="*70)
print("SUMMARY")
print("="*70 + "\n")

print("### Dataset Overview ###")
print(f"  Items:        {n_items}")
print(f"  Participants: {n_raters}")
print(f"  Observations: {n_items * n_raters}")

print("\n### Accuracy by Expertise ###")
for _, row in stats_df.iterrows():
    print(f"  {row['Expertise']:12s}: {row['Median Accuracy']:.3f} [{row['Range Min']:.3f}, {row['Range Max']:.3f}]")

print("\n### ROC Metrics by Expertise ###")
for expertise_group in ['Experts', 'Experienced', 'Novices']:
    group = roc_df[roc_df['Expertise'] == expertise_group]
    print(f"\n{expertise_group}:")
    print(f"  Sensitivity: {group['Sensitivity (TPR)'].mean():.3f} ± {group['Sensitivity (TPR)'].std():.3f}")
    print(f"  Specificity: {group['Specificity (TNR)'].mean():.3f} ± {group['Specificity (TNR)'].std():.3f}")
    print(f"  FPR:         {group['FPR'].mean():.3f} ± {group['FPR'].std():.3f}")

print("\n" + "="*70)
print("NEXT STEPS")
print("="*70)
print("\nTo complete the analysis with SSIT model:")
print("1. Use the prepared data: spikes_analysis_output/spikes_data_for_analysis.csv")
print("2. Run in Jupyter notebook with PyMC installed:")
print("\n```python")
print("from noise_decomposition_flexible import run_analysis")
print("")
print("results = run_analysis(")
print("    'spikes_analysis_output/spikes_data_for_analysis.csv',")
print("    model_type='SSIT',")
print("    draws=5000, tune=2000, chains=10")
print(")")
print("```")
print("\n" + "="*70 + "\n")
