# Note: Mostly works also on newer Python versions, but bonesis enumeration
# has a bug that can cause it to race condition.
FROM python:3.12.13-trixie
EXPOSE 8888

# Graphviz is used by one of the notebooks to show graphs
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gringo \
        graphviz && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /workspace
WORKDIR /workspace

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# The example notebooks
COPY 01-boolean-networks-introduction.ipynb .
COPY 02-boolean-network-inference.ipynb .
COPY anterior-posterior.png .

# Verify that the notebooks run
RUN jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  01-boolean-networks-introduction.ipynb

RUN jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=python3 \
  02-boolean-network-inference.ipynb

CMD ["python3", "-m", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token=''", "--ServerApp.password=''", "--allow-root"]