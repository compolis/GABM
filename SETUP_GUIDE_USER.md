# User Setup Guide
This guide is for end users who want to use GABM with minimal setup. You will either need [Conda](https://conda.org/) or to use an installation of [Python](https://www.python.org/) at version 3.12. Check your Python version:

```bash
python3 --version
```

## 1. Quickstart for Conda Users
If you use [Conda](https://conda.org/) which is distributed with[Anaconda](https://www.anaconda.com/)/[Miniconda](https://docs.conda.io/en/latest/miniconda.html) and [Miniforge](https://github.com/conda-forge/miniforge) you can set up GABM in a new environment as follows:

```bash
conda create -n gabm
conda activate gabm
conda install python=3.12
pip install gabm==0.1.1
```

You can then check all installed dependencies and create your own requirements file with:

```bash
conda list -e > requirements.txt
```


## 2. Quickstart for Python 3.12 users
Install from [PyPI](https://pypi.org/) using [Pip](https://pypi.org/project/pip/) as follows:

```bash
python3 -m venv gabm-venv
source gabm-venv/bin/activate  # On Windows: gabm-venv\\Scripts\\activate
pip install --upgrade pip
pip install gabm==0.1.1
```

You can then check installed dependencies with:

```bash
pip freeze > requirements.txt
```


## 3. Set Up API Keys (Optional)
If you want to use LLM features, create `data/api_key.csv` with your API keys. See [API_KEYS.md](API_KEYS.md) for details and instructions.


## 4. Run the Main Program
From the project root:

```bash
python3 -m gabm
```


## 6. Troubleshooting

- If you encounter errors, check your Python version and that all dependencies are installed.
- For more help, see the [README](README.md).
- If you need support, you can [open an issue on GitHub](https://github.com/compolis/GABM/issues/new/choose).
