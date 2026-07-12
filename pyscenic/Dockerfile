# Note: Requires older version of Dask, which does not work well
# on newer Python versions, so 3.10 it is for now...
FROM python:3.10.20-trixie
EXPOSE 8888


# Graphviz is used by one of the notebooks to show graphs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace
WORKDIR /workspace

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# The example notebooks
COPY 03-pyscenic-grn.ipynb .

RUN mkdir -p data

# Full GRN and dataset, in case we want to run complete analysis instead of "simplified"
COPY ./data/full_grn_results.tsv ./data/full_grn_results.tsv

RUN mkdir -p data/filtered_counts
COPY ./data/filtered_counts/barcodes.tsv.gz ./data/filtered_counts/barcodes.tsv.gz
COPY ./data/filtered_counts/genes.tsv.gz ./data/filtered_counts/genes.tsv.gz
COPY ./data/filtered_counts/matrix.mtx.gz ./data/filtered_counts/matrix.mtx.gz

# HVG dataset for the demo

RUN mkdir -p data/filtered_counts_300_hvg
COPY ./data/filtered_counts_300_hvg/barcodes.tsv.gz ./data/filtered_counts_300_hvg/barcodes.tsv.gz
COPY ./data/filtered_counts_300_hvg/genes.tsv.gz ./data/filtered_counts_300_hvg/genes.tsv.gz
COPY ./data/filtered_counts_300_hvg/matrix.mtx.gz ./data/filtered_counts_300_hvg/matrix.mtx.gz


# Verify that the notebooks run
RUN jupyter nbconvert --to notebook --execute --inplace --debug \
  --ExecutePreprocessor.timeout=3600 \
  --ExecutePreprocessor.kernel_name=python3 \
  03-pyscenic-grn.ipynb

CMD ["python3", "-m", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=''", "--ServerApp.password=''", "--allow-root"]