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
COPY 01-dataset-overview.ipynb .
COPY 02-arboreto-grn.ipynb .
COPY pseudotime.png .

# Verify that the notebooks run
RUN jupyter nbconvert --to notebook --execute --inplace --debug \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  01-dataset-overview.ipynb

  RUN jupyter nbconvert --to notebook --execute --inplace --debug \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  02-arboreto-grn.ipynb

CMD ["python3", "-m", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=''", "--ServerApp.password=''", "--allow-root"]