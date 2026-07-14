# 1. Install UV

Full instructions: https://docs.astral.sh/uv/getting-started/installation/

Linux:

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:

```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Ok if you already have `pip`:

```
pip install uv
```

# 2. Create virtual environment

```
uv venv venv-grn --python=3.10
source ./venv-grn/bin/activate
uv pip install -r requirements.txt
```

# 3. Run Jupyter

```
python3 -m jupyter notebook
```