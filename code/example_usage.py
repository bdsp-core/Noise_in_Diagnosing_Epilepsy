#!/usr/bin/env python3
"""
Example usage of the flexible noise decomposition framework

This script demonstrates how to:
1. Fit a single model (IRT, SSIT, or KSS)
2. Compare multiple models
3. Extract and interpret results
"""

from noise_decomposition_flexible import run_analysis, compare_models
import matplotlib.pyplot as plt
import numpy as np

# =============================================================================
# Example 1: Fit a single model
# =============================================================================

print("\n" + "="*70)
print("EXAMPLE 1: Fit a single KSS model")
print("="*70)

# Fit the full KSS model
results_kss = run_analysis(
    "dataQ1.csv",
    model_type="KSS",
    draws=2000,        # Fewer draws for faster example
    tune=1000,
    chains=4,          # Fewer chains for faster example
    cores=4
)

# Access variance decomposition
vd = results_kss['variance_decomposition']
print("\nVariance Decomposition:")
print(f"  Signal:        {vd['perc_c']:.1f}%")
print(f"  Level Noise:   {vd['perc_l']:.1f}%")
print(f"  Pattern Noise: {vd['perc_p']:.1f}%")
print(f"  Occasion Noise: {vd['perc_o']:.1f}%")

# Access effective scales
scales = results_kss['effective_scales']
print("\nEffective Scales (σ estimates):")
print(f"  Signal:        {scales['S_est']:.3f}")
print(f"  Level Noise:   {scales['LN_est']:.3f}")
print(f"  Pattern Noise: {scales['PN_est']:.3f}")
print(f"  Occasion Noise: {scales['ON_est']:.3f}")


# =============================================================================
# Example 2: Compare all three models
# =============================================================================

print("\n" + "="*70)
print("EXAMPLE 2: Compare IRT, SSIT, and KSS models")
print("="*70)

# Fit all three models and compare
all_results = compare_models(
    "dataQ1.csv",
    models=["IRT", "SSIT", "KSS"],
    draws=2000,
    tune=1000,
    chains=4,
    cores=4
)

# The compare_models function automatically prints a comparison table
# You can also access individual results:
print("\nDetailed comparison:")
for model_type, results in all_results.items():
    vd = results['variance_decomposition']
    print(f"\n{model_type} Model:")
    print(f"  Total variance: {vd['total_variance']:.3f}")
    print(f"  Signal/Noise ratio: {vd['perc_c']/(100-vd['perc_c']):.2f}")


# =============================================================================
# Example 3: Fit SSIT model for T=1 data
# =============================================================================

print("\n" + "="*70)
print("EXAMPLE 3: Fit SSIT model (recommended for T=1)")
print("="*70)

# When you only have one occasion (T=1), use SSIT
# It combines pattern and occasion noise into a single residual
results_ssit = run_analysis(
    "dataQ1.csv",
    model_type="SSIT",
    draws=2000,
    tune=1000,
    chains=4,
    cores=4
)

print("\nWith T=1 data, SSIT avoids trying to separate")
print("pattern noise from occasion noise (which are confounded).")


# =============================================================================
# Example 4: Create a simple visualization
# =============================================================================

print("\n" + "="*70)
print("EXAMPLE 4: Visualize variance decomposition")
print("="*70)

# Create a bar plot comparing the three models
fig, ax = plt.subplots(1, 1, figsize=(10, 6))

models = ["IRT", "SSIT", "KSS"]
x = np.arange(len(models))
width = 0.2

# Extract percentages for each component
signal_pcts = [all_results[m]['variance_decomposition']['perc_c'] for m in models]
level_pcts = [all_results[m]['variance_decomposition']['perc_l'] for m in models]
pattern_pcts = [all_results[m]['variance_decomposition']['perc_p'] for m in models]
occasion_pcts = [all_results[m]['variance_decomposition']['perc_o'] for m in models]

# Create stacked bars
ax.bar(x, signal_pcts, width*3, label='Signal', color='#2E86AB')
ax.bar(x, level_pcts, width*3, bottom=signal_pcts, label='Level Noise', color='#A23B72')
ax.bar(x, pattern_pcts, width*3, bottom=np.array(signal_pcts)+np.array(level_pcts),
       label='Pattern Noise', color='#F18F01')
ax.bar(x, occasion_pcts, width*3,
       bottom=np.array(signal_pcts)+np.array(level_pcts)+np.array(pattern_pcts),
       label='Occasion Noise', color='#C73E1D')

ax.set_ylabel('Percentage of Total Variance', fontsize=12)
ax.set_title('Variance Decomposition Across Models', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=12)
ax.legend(loc='upper right')
ax.set_ylim([0, 100])
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig("model_comparison_example.png", dpi=300, bbox_inches='tight')
print("\nSaved comparison plot to: model_comparison_example.png")
plt.show()


# =============================================================================
# Example 5: Post-hoc combination for T=1 data
# =============================================================================

print("\n" + "="*70)
print("EXAMPLE 5: Combine pattern + occasion for T=1 data")
print("="*70)

# If you ran the full KSS model but have T=1 data,
# you can combine pattern and occasion noise post-hoc
import numpy as np

trace = results_kss['trace']
sigma_p_samples = trace.posterior['sigma_p'].values.flatten()
sigma_o_samples = trace.posterior['sigma_o'].values.flatten()

# Combine variances
var_p = np.mean(sigma_p_samples ** 2)
var_o = np.mean(sigma_o_samples ** 2)
var_other = var_p + var_o
other_noise = np.sqrt(var_other)

# Recompute percentages
var_c = results_kss['effective_scales']['S_est'] ** 2
var_l = results_kss['effective_scales']['LN_est'] ** 2
total_var = var_c + var_l + var_other

print("\nCombined variance decomposition:")
print(f"  Signal:               {(var_c/total_var)*100:.1f}%")
print(f"  Level Noise:          {(var_l/total_var)*100:.1f}%")
print(f"  Other Noise (PN+ON):  {(var_other/total_var)*100:.1f}%")
print(f"\nOther Noise scale: {other_noise:.3f}")


print("\n" + "="*70)
print("Examples complete! Check the generated files:")
print("  - model_comparison_example.png")
print("  - *_latent_effects.csv files")
print("  - *.pkl results files")
print("="*70 + "\n")
