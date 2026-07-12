#!/usr/bin/env python3
"""
run_grn_inference.py

This script performs parallelized Gene Regulatory Network (GRN) inference 
using GRNBoost2 on a single-cell RNA-seq dataset (h5ad file). 
It selects Highly Variable Genes (HVGs) as target genes (or all genes if not specified),
uses a list of known transcription factors as predictors (or all genes if not specified),
and parallelizes the workload using a local Dask cluster.
"""

import argparse
import sys
import os
import scanpy as sc
import pandas as pd
from arboreto.algo import grnboost2
from distributed import Client, LocalCluster

def main():
    parser = argparse.ArgumentParser(description="Infer GRN using GRNBoost2 on a local Dask cluster.")
    parser.add_argument("--input", type=str, default="preprocessed_adata.h5ad", 
                        help="Path to preprocessed scanpy .h5ad file.")
    parser.add_argument("--n_hvg", type=int, default=None,
                        help="Number of highly variable genes to select. If not provided, all genes are used.")
    parser.add_argument("--tf_list", type=str, default=None,
                        help="Path to the transcription factor list (TXT). If not provided, all genes are used as TFs.")
    parser.add_argument("--output", type=str, default="full_grn_results.tsv", 
                        help="Path to save the output TSV file.")
    parser.add_argument("--cores", type=int, default=24, 
                        help="Number of CPU cores/workers to use (default: 24).")
    parser.add_argument("--memory_limit", type=str, default="4GB", 
                        help="Memory limit per worker (e.g., '4GB'). Adjust based on system RAM.")
    
    args = parser.parse_args()

    # 1. Validation checks
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    
    if args.tf_list and not os.path.exists(args.tf_list):
        print(f"Error: TF list file '{args.tf_list}' not found.")
        sys.exit(1)

    print("--- Step 1: Loading single-cell dataset ---")
    adata = sc.read_h5ad(args.input)
    print(f"Loaded dataset with shape: {adata.shape}")

    print("--- Step 2: Selecting Highly Variable Genes ---")
    # Normalize total counts per cell to a target sum (e.g., 10,000)
    sc.pp.normalize_total(adata, target_sum=1e4)

    # Logarithmize the data (X = log(X + 1))
    sc.pp.log1p(adata)

    # Identify highly variable genes
    if args.n_hvg is not None:
        sc.pp.highly_variable_genes(adata, n_top_genes=args.n_hvg, flavor="seurat")
        hvg_list = adata.var_names[adata.var.highly_variable].tolist()
        print(f"Identified {len(hvg_list)} target HVGs.")
    else:
        hvg_list = adata.var_names.tolist()
        print(f"Using all {len(hvg_list)} genes as targets.")

    print("--- Step 3: Loading Transcription Factors ---")
    if args.tf_list:
        with open(args.tf_list, "r") as f:
            tf_list = [line.strip() for line in f if line.strip()]
    else:
        tf_list = adata.var_names.tolist()
        print(f"No TF list provided, using all {len(tf_list)} genes as candidate TFs.")
    
    # Keep only TFs that are actually present in our expression dataset
    available_tfs = list(set(tf_list).intersection(adata.var_names))
    print(f"Found {len(available_tfs)} candidate TFs in the dataset.")

    print("--- Step 4: Creating optimized expression matrix subset ---")
    # We subset to the union of HVGs and available TFs.
    # This prevents loading unused genes, saving RAM
    genes_to_keep = list(set(hvg_list).union(available_tfs))
    adata_subset = adata[:, genes_to_keep].copy()
    
    # Convert expression data to pandas DataFrame (cells x genes)
    expression_df = pd.DataFrame(
        adata_subset.X.toarray() if hasattr(adata_subset.X, "toarray") else adata_subset.X,
        index=adata_subset.obs_names,
        columns=adata_subset.var_names
    )
    print(f"Expression matrix prepared with shape: {expression_df.shape}")

    print(f"--- Step 5: Setting up Dask Parallel Cluster ({args.cores} cores) ---")
    # Create a local multiprocessing cluster for Arboreto
    # n_workers = 24 with 1 thread each is recommended for CPU-bound tasks in Arboreto
    cluster = LocalCluster(
        n_workers=args.cores, 
        threads_per_worker=1, 
        memory_limit=args.memory_limit
    )
    client = Client(cluster)
    print(f"Dask dashboard is available at: {client.dashboard_link}")

    try:
        print("--- Step 6: Inferring Gene Regulatory Network ---")
        # Run GRNBoost2
        # Target genes = hvg_list
        # Candidate regulators = available_tfs
        network = grnboost2(
            expression_data=expression_df,
            gene_names=hvg_list,
            tf_names=available_tfs,
            client_or_address=client,
            verbose=True
        )
        
        # Format columns and sort
        network.columns = ['TF', 'Target', 'Importance']
        network = network.sort_values(by="Importance", ascending=False).reset_index(drop=True)

        print("--- Step 7: Saving network to disk ---")
        network.to_csv(args.output, sep="\t", index=False)
        print(f"Success! GRN saved to '{args.output}'")
        print(f"Total interactions inferred: {len(network)}")

    finally:
        # Ensure the Dask cluster is closed even if the execution fails midway
        print("Shutting down Dask cluster...")
        client.close()
        cluster.close()

if __name__ == "__main__":
    main()