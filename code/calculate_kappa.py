#!/usr/bin/env python3
"""
Calculate Cohen's kappa for inter-rater agreement
for the epilepsy diagnosis data (Q1 and Q2).
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from itertools import combinations
from statsmodels.stats.inter_rater import fleiss_kappa

def calculate_kappa_for_dataset(data_file):
    """
    Calculate pairwise Cohen's kappa between all raters and return mean kappa.

    Args:
        data_file: Path to CSV file with columns: id, item, t, Y

    Returns:
        mean_kappa: Average Cohen's kappa across all rater pairs
        std_kappa: Standard deviation of kappa values
        all_kappas: List of all pairwise kappa values
    """
    # Load data
    df = pd.read_csv(data_file)

    # Get unique raters and items
    raters = sorted(df['id'].unique())
    items = sorted(df['item'].unique())

    print(f"Dataset: {data_file}")
    print(f"  Raters: {len(raters)}")
    print(f"  Items: {len(items)}")
    print(f"  Occasions: {len(df['t'].unique())}")

    # For each rater, get their responses across all items (averaging over occasions)
    # We'll use the first occasion (t=1) for simplicity, or average if needed
    rater_responses = {}
    for rater in raters:
        # Get responses for this rater, averaging over occasions
        rater_df = df[df['id'] == rater].groupby('item')['Y'].mean().reset_index()
        # Round to get binary (in case of ties, though unlikely with 2 occasions)
        rater_responses[rater] = rater_df.set_index('item')['Y'].round().astype(int)

    # Calculate pairwise Cohen's kappa for all rater pairs
    kappa_values = []
    for r1, r2 in combinations(raters, 2):
        y1 = rater_responses[r1].values
        y2 = rater_responses[r2].values
        # Use labels parameter to handle cases where one rater has all 0s or all 1s
        try:
            kappa = cohen_kappa_score(y1, y2, labels=[0, 1])
            # Only include valid kappa values (not NaN)
            if not np.isnan(kappa):
                kappa_values.append(kappa)
        except:
            # Skip this pair if kappa can't be calculated
            pass

    mean_kappa = np.mean(kappa_values)
    std_kappa = np.std(kappa_values)

    print(f"  Pairwise kappa values:")
    print(f"    Valid pairs: {len(kappa_values)}/{len(raters)*(len(raters)-1)//2}")
    print(f"    Mean: {mean_kappa:.3f}")
    print(f"    Std:  {std_kappa:.3f}")
    print(f"    Min:  {np.min(kappa_values):.3f}")
    print(f"    Max:  {np.max(kappa_values):.3f}")
    print()

    return mean_kappa, std_kappa, kappa_values

def calculate_fleiss_kappa(data_file):
    """
    Calculate Fleiss' kappa for multiple raters.
    """
    df = pd.read_csv(data_file)

    # Average over occasions for each rater-item pair
    df_avg = df.groupby(['id', 'item'])['Y'].mean().reset_index()
    df_avg['Y'] = df_avg['Y'].round().astype(int)

    # Create contingency table: rows = items, columns = categories (0, 1)
    # Each cell contains count of raters who chose that category for that item
    items = sorted(df_avg['item'].unique())
    n_raters = len(df_avg['id'].unique())

    # Build the table
    table = []
    for item in items:
        item_data = df_avg[df_avg['item'] == item]['Y']
        n_0 = (item_data == 0).sum()
        n_1 = (item_data == 1).sum()
        table.append([n_0, n_1])

    table = np.array(table)
    kappa = fleiss_kappa(table, method='fleiss')

    return kappa

if __name__ == "__main__":
    # Calculate kappa for Stage 1 (Q1 - History only)
    print("=" * 60)
    print("Stage 1 (History only)")
    print("=" * 60)
    kappa1_mean, kappa1_std, kappa1_values = calculate_kappa_for_dataset('dataQ1.csv')
    fleiss1 = calculate_fleiss_kappa('dataQ1.csv')
    print(f"  Fleiss' kappa: {fleiss1:.3f}")
    print()

    # Calculate kappa for Stage 2 (Q2 - History + EEG/Imaging)
    print("=" * 60)
    print("Stage 2 (History + EEG/Imaging)")
    print("=" * 60)
    kappa2_mean, kappa2_std, kappa2_values = calculate_kappa_for_dataset('dataQ2.csv')
    fleiss2 = calculate_fleiss_kappa('dataQ2.csv')
    print(f"  Fleiss' kappa: {fleiss2:.3f}")
    print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Stage 1 (History):")
    print(f"  Mean pairwise Cohen's kappa: {kappa1_mean:.2f}")
    print(f"  Fleiss' kappa:               {fleiss1:.2f}")
    print()
    print(f"Stage 2 (History + EEG/Img):")
    print(f"  Mean pairwise Cohen's kappa: {kappa2_mean:.2f}")
    print(f"  Fleiss' kappa:               {fleiss2:.2f}")
    print()
    print("Paper claims:")
    print("  Stage 1: kappa ≈ 0.6")
    print("  Stage 2: kappa ≈ 0.7")
    print()
    print("Verification (using Fleiss' kappa):")
    print(f"  Stage 1: {'✓ MATCHES' if abs(fleiss1 - 0.6) < 0.05 else '✗ DOES NOT MATCH'} (diff = {fleiss1 - 0.6:.2f})")
    print(f"  Stage 2: {'✓ MATCHES' if abs(fleiss2 - 0.7) < 0.05 else '✗ DOES NOT MATCH'} (diff = {fleiss2 - 0.7:.2f})")
