#!/usr/bin/env python3
"""
Flexible Noise Decomposition Analysis with Model Selection

This script implements the noise decomposition framework with support for
different model specifications:
- 'IRT': Item Response Theory (1PL Rasch model) - Signal + Level Noise only
- 'SSIT': Similar Skill Individual Threshold - Signal + Level Noise + Residual (Pattern + Occasion)
- 'KSS': Full Kahneman-Sibony-Sunstein decomposition - All four components

Usage:
    from noise_decomposition_flexible import run_analysis

    # Full KSS model
    results = run_analysis("data.csv", model_type="KSS")

    # SSIT model (no occasion noise)
    results = run_analysis("data.csv", model_type="SSIT")

    # IRT model (no pattern or occasion noise)
    results = run_analysis("data.csv", model_type="IRT")
"""

import os
import pickle
import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
import pytensor
import warnings

warnings.filterwarnings('ignore')


def run_analysis(data_filename,
                 model_type="KSS",
                 results_filename=None,
                 draws=5000,
                 tune=2000,
                 chains=10,
                 cores=6,
                 target_accept=0.98,
                 random_seed=42):
    """
    Loads data from a CSV file, builds and samples a Bayesian hierarchical model using PyMC,
    computes the variance decomposition for the latent scale parameters, and saves key results.

    Parameters:
    -----------
    data_filename : str
        Name of the CSV file containing the data with columns: id, item, t, Y

    model_type : str, default="KSS"
        Type of model to fit:
        - "IRT": Item Response Theory (1PL Rasch) - σ_p = σ_o = 0
          Only estimates Signal (c_i) and Level Noise (ℓ_j)

        - "SSIT": Similar Skill Individual Threshold - σ_o = 0
          Estimates Signal, Level Noise, and Pattern Noise (or combined residual)
          Pattern and Occasion noise are confounded into residual

        - "KSS": Full Kahneman-Sibony-Sunstein decomposition (default)
          Estimates all four components: Signal, Level, Pattern, and Occasion Noise

    results_filename : str, optional
        Name of the file to save the results. If None, defaults to model_type prefix

    draws : int, default=5000
        Number of MCMC draws per chain after tuning

    tune : int, default=2000
        Number of tuning (warmup) iterations per chain

    chains : int, default=10
        Number of independent MCMC chains

    cores : int, default=6
        Number of CPU cores to use for parallel sampling

    target_accept : float, default=0.98
        Target acceptance rate for NUTS sampler

    random_seed : int, default=42
        Random seed for reproducibility

    Returns:
    --------
    dict : Dictionary containing:
      - "trace": The InferenceData object from MCMC
      - "variance_decomposition": Dict with keys 'total_variance', 'perc_c', 'perc_l', 'perc_p', 'perc_o'
      - "effective_scales": Dict with keys 'S_est', 'LN_est', 'PN_est', 'ON_est'
      - "data": The preprocessed pandas DataFrame
      - "model_type": The model type used
    """

    # Validate model_type
    valid_models = ["IRT", "SSIT", "KSS"]
    if model_type not in valid_models:
        raise ValueError(f"model_type must be one of {valid_models}, got '{model_type}'")

    # Set default results filename if not provided
    if results_filename is None:
        base_name = data_filename.replace(".csv", "")
        results_filename = f"{base_name}_{model_type}_results.pkl"

    # Set PyTensor flags before any PyTensor-related imports
    os.environ["PYTENSOR_DEVICE"] = "cpu"
    os.environ["PYTENSOR_FLOATX"] = "float64"
    os.environ["PYTENSOR_COMPUTE_TEST_VALUE"] = "ignore"

    print(f"{'='*60}")
    print(f"Running {model_type} Model Analysis")
    print(f"{'='*60}")
    print(f"\nLoading data from {data_filename}")
    data = pd.read_csv(data_filename)
    print("Data head:")
    print(data.head())

    # Create integer indices
    data['expert_idx'] = pd.Categorical(data['id']).codes
    data['case_idx'] = pd.Categorical(data['item']).codes
    data['occ_idx'] = pd.Categorical(data['t']).codes

    # Get dimensions
    n_experts = data['expert_idx'].nunique()
    n_cases = data['case_idx'].nunique()
    n_obs = data.shape[0]

    print(f"\nDataset summary:")
    print(f"  Number of experts (M): {n_experts}")
    print(f"  Number of cases (N): {n_cases}")
    print(f"  Number of observations: {n_obs}")

    # Model descriptions
    model_descriptions = {
        "IRT": "Item Response Theory (1PL Rasch): Signal + Level Noise only",
        "SSIT": "Similar Skill Individual Threshold: Signal + Level Noise + Residual",
        "KSS": "Full decomposition: Signal + Level + Pattern + Occasion Noise"
    }
    print(f"\nModel: {model_descriptions[model_type]}")

    # Build and sample from the PyMC model using non-centered parameterizations
    print(f"\nBuilding {model_type} model...")
    with pm.Model() as model:
        # Priors for scale parameters (always include signal and level noise)
        sigma_c = pm.HalfNormal("sigma_c", sigma=1)
        sigma_l = pm.HalfNormal("sigma_l", sigma=1)
        intercept = pm.Normal("intercept", mu=0, sigma=10)

        # Non-centered latent variables for cases and experts
        z_c = pm.Normal("z_c", mu=0, sigma=1, shape=n_cases)
        c = pm.Deterministic("c", z_c * sigma_c)

        z_l = pm.Normal("z_l", mu=0, sigma=1, shape=n_experts)
        l = pm.Deterministic("l", z_l * sigma_l)

        # Start building linear predictor
        z = intercept + c[data['case_idx'].values] + l[data['expert_idx'].values]

        # Model-specific components
        monitor_vars = ['sigma_c', 'sigma_l', 'intercept']

        if model_type == "IRT":
            # IRT model: No pattern or occasion noise
            # z already contains only c_i + ℓ_j + intercept
            pass

        elif model_type == "SSIT":
            # SSIT model: Add residual term (combines pattern + occasion)
            # This is observation-level to capture all remaining variance
            sigma_residual = pm.HalfNormal("sigma_residual", sigma=1)
            z_residual = pm.Normal("z_residual", mu=0, sigma=1, shape=n_obs)
            residual = pm.Deterministic("residual", z_residual * sigma_residual)
            z = z + residual
            monitor_vars.append('sigma_residual')

        elif model_type == "KSS":
            # Full KSS model: Separate pattern and occasion noise
            sigma_p = pm.HalfNormal("sigma_p", sigma=1)
            sigma_o = pm.HalfNormal("sigma_o", sigma=1)

            z_p = pm.Normal("z_p", mu=0, sigma=1, shape=(n_experts, n_cases))
            p = pm.Deterministic("p", z_p * sigma_p)

            z_o = pm.Normal("z_o", mu=0, sigma=1, shape=n_obs)
            o = pm.Deterministic("o", z_o * sigma_o)

            z = z + p[data['expert_idx'].values, data['case_idx'].values] + o
            monitor_vars.extend(['sigma_p', 'sigma_o'])

        # Likelihood
        y_obs = pm.Bernoulli("y_obs", logit_p=z, observed=data['Y'].values)

        print(f"\nSampling with NUTS (NumPyro backend)...")
        print(f"  Chains: {chains}")
        print(f"  Draws per chain: {draws}")
        print(f"  Tuning iterations: {tune}")
        print(f"  Target acceptance: {target_accept}")

        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            cores=cores,
            random_seed=random_seed,
            return_inferencedata=True,
            nuts_sampler='numpyro',
            init='jitter+adapt_diag',
            progressbar=True,
            target_accept=target_accept
        )

    # Post-sampling analysis
    print(f"\n{'='*60}")
    print("Posterior Summary:")
    print(f"{'='*60}")
    summary = az.summary(trace, var_names=monitor_vars)
    print(summary)

    # Extract posterior samples for the scale parameters
    sigma_c_samples = trace.posterior['sigma_c'].values.flatten()
    sigma_l_samples = trace.posterior['sigma_l'].values.flatten()

    # Compute variances
    var_c = np.mean(sigma_c_samples ** 2)
    var_l = np.mean(sigma_l_samples ** 2)

    # Model-specific variance extraction
    if model_type == "IRT":
        # IRT: No pattern or occasion noise
        var_p = 0.0
        var_o = 0.0
        sigma_p_samples = None
        sigma_o_samples = None

    elif model_type == "SSIT":
        # SSIT: Residual combines pattern and occasion
        sigma_residual_samples = trace.posterior['sigma_residual'].values.flatten()
        var_residual = np.mean(sigma_residual_samples ** 2)
        # For reporting, we put residual in the "pattern + occasion" category
        var_p = var_residual
        var_o = 0.0
        sigma_p_samples = sigma_residual_samples
        sigma_o_samples = None

    elif model_type == "KSS":
        # Full KSS: Separate pattern and occasion
        sigma_p_samples = trace.posterior['sigma_p'].values.flatten()
        sigma_o_samples = trace.posterior['sigma_o'].values.flatten()
        var_p = np.mean(sigma_p_samples ** 2)
        var_o = np.mean(sigma_o_samples ** 2)

    # Calculate total variance
    total_variance = var_c + var_l + var_p + var_o

    # Compute percentage contributions
    perc_c = (var_c / total_variance) * 100
    perc_l = (var_l / total_variance) * 100
    perc_p = (var_p / total_variance) * 100
    perc_o = (var_o / total_variance) * 100

    print(f"\n{'='*60}")
    print("Variance Decomposition:")
    print(f"{'='*60}")
    print(f"Total Variance (sum of components): {total_variance:.3f}")
    print("\nPercentage contributions:")
    print(f"  Signal (case) variance:              {perc_c:.2f}%")
    print(f"  Level Noise (expert) variance:       {perc_l:.2f}%")

    if model_type == "IRT":
        print(f"  Pattern Noise:                       N/A (not estimated in IRT)")
        print(f"  Occasion Noise:                      N/A (not estimated in IRT)")
    elif model_type == "SSIT":
        print(f"  Residual (Pattern + Occasion):       {perc_p:.2f}%")
        print(f"  Occasion Noise:                      N/A (confounded with pattern)")
    else:  # KSS
        print(f"  Pattern Noise (interaction):         {perc_p:.2f}%")
        print(f"  Occasion Noise (within-rater):       {perc_o:.2f}%")

    # Compute effective scale estimates
    S_est = np.sqrt(var_c)
    LN_est = np.sqrt(var_l)
    PN_est = np.sqrt(var_p) if var_p > 0 else 0.0
    ON_est = np.sqrt(var_o) if var_o > 0 else 0.0

    print(f"\n{'='*60}")
    print("Effective Scale Estimates:")
    print(f"{'='*60}")
    print(f"  Signal (S):         {S_est:.3f}")
    print(f"  Level Noise (LN):   {LN_est:.3f}")

    if model_type == "IRT":
        print(f"  Pattern Noise (PN): N/A")
        print(f"  Occasion Noise (ON): N/A")
    elif model_type == "SSIT":
        print(f"  Residual:           {PN_est:.3f}")
        print(f"  Occasion Noise (ON): N/A")
    else:
        print(f"  Pattern Noise (PN): {PN_est:.3f}")
        print(f"  Occasion Noise (ON): {ON_est:.3f}")

    # Prepare results dictionary
    results = {
        "model_type": model_type,
        "trace": trace,
        "variance_decomposition": {
            "total_variance": total_variance,
            "perc_c": perc_c,
            "perc_l": perc_l,
            "perc_p": perc_p,
            "perc_o": perc_o
        },
        "effective_scales": {
            "S_est": S_est,
            "LN_est": LN_est,
            "PN_est": PN_est,
            "ON_est": ON_est
        },
        "data": data
    }

    # Extract and save latent effects
    print(f"\n{'='*60}")
    print("Extracting Latent Effects:")
    print(f"{'='*60}")

    c_est = trace.posterior['c'].mean(dim=["chain", "draw"]).values
    l_est = trace.posterior['l'].mean(dim=["chain", "draw"]).values

    df_latents = data[['expert_idx', 'case_idx', 'occ_idx']].copy()
    df_latents['c'] = df_latents['case_idx'].apply(lambda j: c_est[int(j)])
    df_latents['l'] = df_latents['expert_idx'].apply(lambda i: l_est[int(i)])

    if model_type == "IRT":
        # No pattern or occasion effects
        df_latents['p'] = 0.0
        df_latents['o'] = 0.0

    elif model_type == "SSIT":
        # Residual at observation level
        residual_est = trace.posterior['residual'].mean(dim=["chain", "draw"]).values
        df_latents['p'] = 0.0  # Not separately estimated
        df_latents['o'] = residual_est  # Store in 'o' column for consistency

    elif model_type == "KSS":
        # Full decomposition
        p_est = trace.posterior['p'].mean(dim=["chain", "draw"]).values
        o_est = trace.posterior['o'].mean(dim=["chain", "draw"]).values
        df_latents['p'] = df_latents.apply(
            lambda row: p_est[int(row['expert_idx']), int(row['case_idx'])], axis=1
        )
        df_latents['o'] = o_est

    # Rename columns
    df_latents.rename(columns={"expert_idx": "i", "case_idx": "j", "occ_idx": "t"},
                     inplace=True)

    # Save latent effects
    latent_csv_filename = data_filename.replace(".csv", f"_{model_type}_latent_effects.csv")
    df_latents.to_csv(latent_csv_filename, index=False)
    print(f"Estimated latent effects saved to: {latent_csv_filename}")

    # Save full results
    print(f"Full results saved to: {results_filename}")
    with open(results_filename, "wb") as f:
        pickle.dump(results, f)

    print(f"\n{'='*60}")
    print("Analysis Complete!")
    print(f"{'='*60}\n")

    return results


def compare_models(data_filename, models=["IRT", "SSIT", "KSS"], **kwargs):
    """
    Fit multiple models to the same dataset and compare results.

    Parameters:
    -----------
    data_filename : str
        Path to the CSV data file

    models : list of str, default=["IRT", "SSIT", "KSS"]
        List of model types to fit

    **kwargs : dict
        Additional arguments passed to run_analysis()

    Returns:
    --------
    dict : Dictionary mapping model_type to results
    """
    results = {}
    for model_type in models:
        print(f"\n\n{'#'*70}")
        print(f"# Fitting {model_type} model")
        print(f"{'#'*70}\n")
        results[model_type] = run_analysis(data_filename, model_type=model_type, **kwargs)

    # Print comparison table
    print(f"\n{'='*70}")
    print("MODEL COMPARISON")
    print(f"{'='*70}")
    print(f"{'Model':<10} {'Signal %':<12} {'Level %':<12} {'Pattern %':<12} {'Occasion %':<12}")
    print(f"{'-'*70}")

    for model_type in models:
        vd = results[model_type]['variance_decomposition']
        print(f"{model_type:<10} {vd['perc_c']:>10.2f}%  {vd['perc_l']:>10.2f}%  "
              f"{vd['perc_p']:>10.2f}%  {vd['perc_o']:>10.2f}%")

    print(f"{'='*70}\n")

    return results


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Usage: python noise_decomposition_flexible.py <data_file.csv> [model_type]")
        print("  model_type: IRT, SSIT, or KSS (default: KSS)")
        print("\nExample:")
        print("  python noise_decomposition_flexible.py dataQ1.csv KSS")
        print("  python noise_decomposition_flexible.py dataQ1.csv SSIT")
        print("\nOr to compare all models:")
        print("  python -c \"from noise_decomposition_flexible import compare_models; compare_models('dataQ1.csv')\"")
        sys.exit(1)

    data_file = sys.argv[1]
    model_type = sys.argv[2] if len(sys.argv) > 2 else "KSS"

    results = run_analysis(data_file, model_type=model_type)

    print(f"\nResults object contains:")
    print(f"  - trace: MCMC samples (InferenceData)")
    print(f"  - variance_decomposition: percentage contributions")
    print(f"  - effective_scales: σ estimates for each component")
    print(f"  - data: preprocessed DataFrame")
    print(f"  - model_type: '{model_type}'")
