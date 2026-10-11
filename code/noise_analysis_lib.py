#!/usr/bin/env python3
"""
Noise Analysis Library - Core Functions

This module provides reusable functions for noise decomposition analysis.
Import this in Jupyter notebooks for case studies.

Usage:
    from noise_analysis_lib import (
        prepare_data_for_analysis,
        run_noise_analysis,
        compute_descriptive_stats,
        compute_roc_points,
        plot_variance_decomposition,
        plot_roc_curves
    )
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, auc
from noise_decomposition_flexible import run_analysis


def prepare_data_for_analysis(y_prob, y_answers, expertise=None,
                              occasion=1, threshold=0.5):
    """
    Convert response probability matrix to the format needed for noise analysis.

    Parameters:
    -----------
    y_prob : ndarray or DataFrame, shape (n_items, n_raters)
        Probability or continuous responses from raters

    y_answers : ndarray or DataFrame, shape (n_items,) or (n_items, n_raters)
        True answers (gold standard) as probabilities or binary
        If 2D, uses first column or mean across columns

    expertise : array-like, optional
        Expertise level for each rater (for grouping)

    occasion : int, default=1
        Occasion number (use 1 for single-occasion data)

    threshold : float, default=0.5
        Threshold for converting probabilities to binary responses

    Returns:
    --------
    DataFrame with columns: id, item, t, Y, expertise (if provided)
    """

    # Convert to numpy arrays if needed
    if isinstance(y_prob, pd.DataFrame):
        y_prob = y_prob.values
    if isinstance(y_answers, pd.DataFrame):
        y_answers = y_answers.values

    # Handle y_answers dimension
    if y_answers.ndim == 2:
        # If 2D, use first column or mean
        if y_answers.shape[1] == 1:
            y_answers = y_answers.flatten()
        else:
            y_answers = y_answers.mean(axis=1)

    n_items, n_raters = y_prob.shape

    # Create long-format dataframe
    data_list = []

    for rater_idx in range(n_raters):
        for item_idx in range(n_items):
            # Binary response (threshold probabilities)
            response = 1 if y_prob[item_idx, rater_idx] >= threshold else 0

            row = {
                'id': rater_idx + 1,  # 1-indexed rater ID
                'item': item_idx + 1,  # 1-indexed item ID
                't': occasion,
                'Y': response
            }

            if expertise is not None:
                row['expertise'] = expertise[rater_idx]

            data_list.append(row)

    df = pd.DataFrame(data_list)

    # Convert true answers to binary
    y_binary = (y_answers >= threshold).astype(int)
    df['true_answer'] = df['item'].map(lambda x: y_binary[x-1])

    return df


def run_noise_analysis(df, model_type="SSIT", save_prefix="analysis",
                      draws=5000, tune=2000, chains=10, cores=6,
                      target_accept=0.98, random_seed=42):
    """
    Run noise decomposition analysis on prepared data.

    Parameters:
    -----------
    df : DataFrame
        Data in long format with columns: id, item, t, Y

    model_type : str, default="SSIT"
        Model type: "IRT", "SSIT", or "KSS"

    save_prefix : str, default="analysis"
        Prefix for output files

    Other parameters: passed to run_analysis()

    Returns:
    --------
    results : dict
        Results dictionary from run_analysis()
    """

    # Save to temporary CSV
    temp_file = f"{save_prefix}_temp.csv"
    df[['id', 'item', 't', 'Y']].to_csv(temp_file, index=False)

    # Run analysis
    results = run_analysis(
        temp_file,
        model_type=model_type,
        results_filename=f"{save_prefix}_{model_type}_results.pkl",
        draws=draws,
        tune=tune,
        chains=chains,
        cores=cores,
        target_accept=target_accept,
        random_seed=random_seed
    )

    # Clean up temp file
    import os
    os.remove(temp_file)

    return results


def compute_descriptive_stats(y_prob, y_answers, expertise, threshold=0.5):
    """
    Compute descriptive statistics by expertise group.

    Parameters:
    -----------
    y_prob : ndarray, shape (n_items, n_raters)
        Responses from raters

    y_answers : ndarray, shape (n_items,)
        True answers

    expertise : array-like
        Expertise level for each rater

    threshold : float, default=0.5
        Threshold for binary classification

    Returns:
    --------
    DataFrame with columns: expertise_level, n_raters, median_accuracy,
                           accuracy_range_min, accuracy_range_max
    """

    # Convert to binary
    if isinstance(y_prob, pd.DataFrame):
        y_prob = y_prob.values
    if isinstance(y_answers, pd.DataFrame):
        y_answers = y_answers.values
    if y_answers.ndim == 2:
        y_answers = y_answers.mean(axis=1)

    y_binary = (y_prob >= threshold).astype(int)
    y_true = (y_answers >= threshold).astype(int)

    # Compute accuracy for each rater
    n_items, n_raters = y_binary.shape
    accuracies = np.zeros(n_raters)

    for i in range(n_raters):
        accuracies[i] = (y_binary[:, i] == y_true).mean()

    # Group by expertise
    expertise_array = np.array(expertise)
    unique_levels = sorted(np.unique(expertise_array))

    stats_list = []
    for level in unique_levels:
        mask = expertise_array == level
        group_acc = accuracies[mask]

        stats_list.append({
            'expertise_level': level,
            'n_raters': mask.sum(),
            'median_accuracy': np.median(group_acc),
            'accuracy_range_min': np.min(group_acc),
            'accuracy_range_max': np.max(group_acc),
            'mean_accuracy': np.mean(group_acc),
            'std_accuracy': np.std(group_acc)
        })

    return pd.DataFrame(stats_list)


def compute_roc_points(y_prob, y_answers, expertise=None, threshold=0.5):
    """
    Compute ROC operating points (TPR, FPR) for each rater.

    Parameters:
    -----------
    y_prob : ndarray, shape (n_items, n_raters)
        Responses from raters

    y_answers : ndarray, shape (n_items,)
        True answers

    expertise : array-like, optional
        Expertise level for each rater

    threshold : float, default=0.5
        Threshold for binary classification

    Returns:
    --------
    DataFrame with columns: rater_id, expertise, tpr, fpr, tnr, fnr, accuracy
    """

    # Convert to binary
    if isinstance(y_prob, pd.DataFrame):
        y_prob = y_prob.values
    if isinstance(y_answers, pd.DataFrame):
        y_answers = y_answers.values
    if y_answers.ndim == 2:
        y_answers = y_answers.mean(axis=1)

    y_binary = (y_prob >= threshold).astype(int)
    y_true = (y_answers >= threshold).astype(int)

    n_items, n_raters = y_binary.shape

    roc_list = []
    for i in range(n_raters):
        y_pred = y_binary[:, i]

        # Compute confusion matrix elements
        tp = ((y_pred == 1) & (y_true == 1)).sum()
        fp = ((y_pred == 1) & (y_true == 0)).sum()
        tn = ((y_pred == 0) & (y_true == 0)).sum()
        fn = ((y_pred == 0) & (y_true == 1)).sum()

        # Compute rates
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0  # Sensitivity
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0  # 1 - Specificity
        tnr = tn / (tn + fp) if (tn + fp) > 0 else 0  # Specificity
        fnr = fn / (fn + tp) if (fn + tp) > 0 else 0  # 1 - Sensitivity
        acc = (tp + tn) / (tp + tn + fp + fn)

        row = {
            'rater_id': i + 1,
            'tpr': tpr,
            'fpr': fpr,
            'tnr': tnr,
            'fnr': fnr,
            'accuracy': acc,
            'sensitivity': tpr,
            'specificity': tnr
        }

        if expertise is not None:
            row['expertise'] = expertise[i]

        roc_list.append(row)

    return pd.DataFrame(roc_list)


def extract_participant_estimates(results, df):
    """
    Extract individual participant estimates from model results.

    Parameters:
    -----------
    results : dict
        Results from run_noise_analysis()

    df : DataFrame
        Original data with expertise info

    Returns:
    --------
    DataFrame with columns: rater_id, level_noise, skill, expertise
    """

    trace = results['trace']

    # Extract level noise (bias) for each rater
    l_samples = trace.posterior['l'].values  # shape: (chains, draws, n_raters)
    l_mean = l_samples.mean(axis=(0, 1))  # Posterior mean
    l_std = l_samples.std(axis=(0, 1))    # Posterior SD

    # For SSIT: Extract residual variance as "inverse skill"
    # Skill = 1/σ where σ is the noise level
    if results['model_type'] == 'SSIT':
        sigma_residual = results['effective_scales']['PN_est']  # Stored in PN slot for SSIT
        # This is population-level; for individual skill we'd need more
        skill = 1.0 / sigma_residual if sigma_residual > 0 else np.inf
        skill_array = np.full(len(l_mean), skill)  # Same for all (SSIT assumption)
    else:
        # For other models, could extract from pattern noise or set to NaN
        skill_array = np.full(len(l_mean), np.nan)

    # Get expertise mapping
    expertise_map = df.groupby('id')['expertise'].first() if 'expertise' in df.columns else None

    participant_data = []
    for i in range(len(l_mean)):
        rater_id = i + 1
        row = {
            'rater_id': rater_id,
            'level_noise': l_mean[i],
            'level_noise_sd': l_std[i],
            'skill': skill_array[i]
        }

        if expertise_map is not None and rater_id in expertise_map.index:
            row['expertise'] = expertise_map[rater_id]

        participant_data.append(row)

    return pd.DataFrame(participant_data)


def extract_item_difficulties(results):
    """
    Extract item (question) difficulty estimates.

    Parameters:
    -----------
    results : dict
        Results from run_noise_analysis()

    Returns:
    --------
    DataFrame with columns: item_id, difficulty, difficulty_sd
    """

    trace = results['trace']

    # Extract case effects (signal strength / difficulty)
    c_samples = trace.posterior['c'].values  # shape: (chains, draws, n_cases)
    c_mean = c_samples.mean(axis=(0, 1))
    c_std = c_samples.std(axis=(0, 1))

    item_data = []
    for i in range(len(c_mean)):
        item_data.append({
            'item_id': i + 1,
            'difficulty': c_mean[i],
            'difficulty_sd': c_std[i]
        })

    return pd.DataFrame(item_data)


def plot_variance_decomposition(results, title="Variance Decomposition"):
    """
    Plot variance decomposition as a stacked bar chart.

    Parameters:
    -----------
    results : dict
        Results from run_noise_analysis()

    title : str
        Plot title

    Returns:
    --------
    fig, ax
    """

    vd = results['variance_decomposition']
    model_type = results['model_type']

    fig, ax = plt.subplots(figsize=(8, 6))

    # Prepare data based on model type
    if model_type == "IRT":
        components = ['Signal', 'Level Noise']
        percentages = [vd['perc_c'], vd['perc_l']]
        colors = ['#2E86AB', '#A23B72']
    elif model_type == "SSIT":
        components = ['Signal', 'Level Noise', 'Residual']
        percentages = [vd['perc_c'], vd['perc_l'], vd['perc_p']]
        colors = ['#2E86AB', '#A23B72', '#F18F01']
    else:  # KSS
        components = ['Signal', 'Level Noise', 'Pattern Noise', 'Occasion Noise']
        percentages = [vd['perc_c'], vd['perc_l'], vd['perc_p'], vd['perc_o']]
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

    # Create stacked bar
    bottom = 0
    for comp, pct, color in zip(components, percentages, colors):
        ax.bar(0, pct, bottom=bottom, color=color, label=comp, width=0.5)
        # Add percentage label
        if pct > 3:  # Only label if segment is large enough
            ax.text(0, bottom + pct/2, f'{pct:.1f}%',
                   ha='center', va='center', color='white', fontweight='bold')
        bottom += pct

    ax.set_ylim([0, 100])
    ax.set_ylabel('Percentage of Total Variance', fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig, ax


def plot_roc_curves(roc_df, group_by='expertise', figsize=(10, 8)):
    """
    Plot ROC curves grouped by a variable (e.g., expertise).

    Parameters:
    -----------
    roc_df : DataFrame
        ROC operating points from compute_roc_points()

    group_by : str, default='expertise'
        Column to group by

    figsize : tuple
        Figure size

    Returns:
    --------
    fig, ax
    """

    fig, ax = plt.subplots(figsize=figsize)

    if group_by in roc_df.columns:
        groups = sorted(roc_df[group_by].unique())
        colors = sns.color_palette("husl", len(groups))

        for group, color in zip(groups, colors):
            group_data = roc_df[roc_df[group_by] == group]

            # Plot individual points
            ax.scatter(group_data['fpr'], group_data['tpr'],
                      alpha=0.6, color=color, s=100,
                      label=f'{group_by}={group} (n={len(group_data)})')

            # Plot group mean
            mean_fpr = group_data['fpr'].mean()
            mean_tpr = group_data['tpr'].mean()
            ax.scatter(mean_fpr, mean_tpr,
                      color=color, s=300, marker='*',
                      edgecolors='black', linewidths=2,
                      zorder=10)
    else:
        # No grouping, plot all points
        ax.scatter(roc_df['fpr'], roc_df['tpr'], alpha=0.6, s=100)

    # Diagonal reference line (chance performance)
    ax.plot([0, 1], [0, 1], 'k--', linewidth=2, alpha=0.3, label='Chance')

    ax.set_xlabel('False Positive Rate (1 - Specificity)', fontsize=12)
    ax.set_ylabel('True Positive Rate (Sensitivity)', fontsize=12)
    ax.set_title('ROC Operating Points', fontsize=14, fontweight='bold')
    ax.set_xlim([-0.05, 1.05])
    ax.set_ylim([-0.05, 1.05])
    ax.legend(loc='lower right')
    ax.grid(alpha=0.3)
    ax.set_aspect('equal')

    plt.tight_layout()
    return fig, ax


def save_results_summary(results, participant_df, item_df, stats_df, roc_df,
                        output_file="analysis_summary.xlsx"):
    """
    Save all analysis results to an Excel file with multiple sheets.

    Parameters:
    -----------
    results : dict
        Results from run_noise_analysis()
    participant_df : DataFrame
        Participant-level estimates
    item_df : DataFrame
        Item difficulty estimates
    stats_df : DataFrame
        Descriptive statistics
    roc_df : DataFrame
        ROC operating points
    output_file : str
        Output filename
    """

    with pd.ExcelWriter(output_file) as writer:
        # Variance decomposition
        vd = results['variance_decomposition']
        vd_df = pd.DataFrame([{
            'Model': results['model_type'],
            'Total Variance': vd['total_variance'],
            'Signal %': vd['perc_c'],
            'Level Noise %': vd['perc_l'],
            'Pattern/Residual %': vd['perc_p'],
            'Occasion Noise %': vd['perc_o']
        }])
        vd_df.to_excel(writer, sheet_name='Variance_Decomposition', index=False)

        # Effective scales
        scales = results['effective_scales']
        scales_df = pd.DataFrame([scales])
        scales_df.to_excel(writer, sheet_name='Effective_Scales', index=False)

        # Participant estimates
        participant_df.to_excel(writer, sheet_name='Participant_Estimates', index=False)

        # Item difficulties
        item_df.to_excel(writer, sheet_name='Item_Difficulties', index=False)

        # Descriptive stats
        stats_df.to_excel(writer, sheet_name='Descriptive_Stats', index=False)

        # ROC points
        roc_df.to_excel(writer, sheet_name='ROC_Points', index=False)

    print(f"Results saved to: {output_file}")
