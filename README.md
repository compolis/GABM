
# gabm
Generative Agent Based Model

## Getting Started

### 1. Clone the Repository
First, fork the upstream repository on GitHub to your own account. Then, clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/gabm.git
cd gabm
```

### 2. Set Up Your Environment
Install Python 3.9+ and pip if you haven't already. Then install dependencies:

```bash
pip install -r requirements.txt
```

### 3. API Keys
You need a `data/api_key.csv` file with your API keys. This file is not included in the repository for security reasons.

- Ask the project maintainer for a template or example.
- Or, create it yourself with the following format (CSV with header):

```
api,key
openai,sk-...
deepseek,sk-...
llama,YOUR_GROQ_KEY
claude,YOUR_ANTHROPIC_KEY
genai,YOUR_GOOGLE_KEY
```

Place this file in the `data/` directory.

### 4. Running the Code
From the project root, run:

```bash
python3 run.py
```


## Contributing Workflow

**Note:** The `main` branch is protected. All changes must be made through Pull Requests, which require at least one review and approval before merging. Direct pushes to `main` are not allowed. This ensures code quality and collaborative review.

1. **Fork** the upstream repository to your own GitHub account.
2. **Clone** your fork locally.
3. **Create a new branch** for your feature or fix:
	```bash
	git checkout -b my-feature
	```
4. **Make your changes** and commit them:
	```bash
	git add .
	git commit -m "Describe your change"
	```
5. **Push** your branch to your fork:
	```bash
	git push origin my-feature
	```
6. **Open a Pull Request** from your branch to the main branch of the upstream repository on GitHub.
7. Wait for review and feedback. Update your branch as needed.


### Tips
- Keep your fork up to date with the upstream repository:
  ```bash
  git remote add upstream https://github.com/UPSTREAM_USERNAME/gabm.git
  git fetch upstream
  git merge upstream/main
  ```
- For easier authentication, set up SSH keys with GitHub:
  1. Generate an SSH key (if you don’t have one):
	  ```bash
	  ssh-keygen -t ed25519 -C "your_email@example.com"
	  ```
  2. Add your public key to GitHub (Settings > SSH and GPG keys).
  3. Change your remotes to use SSH:
	  ```bash
	  git remote set-url origin git@github.com:YOUR_USERNAME/gabm.git
	  git remote set-url upstream git@github.com:compolis/gabm.git
	  ```
  4. Test with:
	  ```bash
	  ssh -T git@github.com
	  ```