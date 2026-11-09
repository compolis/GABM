# User Guide


## Table of Contents
- [Getting Started](#getting-started)
- [Run the Main Program](#run-the-main-program)
- [Trait State Modeling](#trait-state-modeling)
- [Managing Logs and Caches](#managing-logs-and-caches)
- [Using LLM Modules](#using-llm-modules)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)


## Getting Started

### Prerequisites

 You will either need a local installation of [Conda](https://conda.org/), or [Python](https://www.python.org/) at or above version 3.12. To check your default Python version run:

```bash
python3 --version
```

### Initial set up

#### Using Conda
If you use [Conda](https://conda.org/) which is distributed with [Anaconda](https://www.anaconda.com/), [Miniconda](https://docs.conda.io/en/latest/miniconda.html), or [Miniforge](https://github.com/conda-forge/miniforge), you can set up GABM in a new environment as follows:

```bash
conda create -n gabm
conda activate gabm
conda install python=3.12
pip install gabm==0.5.0
```

You can then check all installed dependencies and create your own requirements file with:

```bash
conda list -e > requirements.txt
```


#### Using Python >=3.14

Install from [PyPI](https://pypi.org/) using [Pip](https://pypi.org/project/pip/) as follows:

```bash
python3 -m venv gabm-venv
source gabm-venv/bin/activate  # On Windows: gabm-venv\\Scripts\\activate
pip install --upgrade pip
pip install gabm==0.5.0
```

Once installed you can check installed dependencies and create a requirements file:

```bash
pip freeze > requirements.txt
```


#### Optional: Local LLM Support

By default, GABM installs only the dependencies needed for hosted LLM providers (OpenAI, Google, DeepSeek, etc.).
If you want to run LLMs locally (e.g., downloaded from Hugging Face), you need additional dependencies:

- torch
- transformers

These are listed in requirements-local-llm.txt in the project root.

To install with local LLM support, use:

```bash
pip install gabm[llm-local]
```

Or, manually install from requirements-local-llm.txt:

```bash
pip install -r requirements-local-llm.txt
```

This keeps the core installation lightweight for users who only use hosted LLMs.


### Set Up API Keys

Create `data/api_key.csv` with your API keys. For all supported LLM providers (including PublicAI/Apertus), see [API_KEYS.md](API_KEYS.md) for up-to-date details and instructions.



#### Using Local Apertus LLM Models

For instructions on downloading, authenticating, and using local Apertus LLM models (and other Hugging Face models), see [HUGGING_FACE.md](HUGGING_FACE.md).


## Run the Main Program


### Running GABM: Example and Survey Modes

You can run GABM in different modes using a command-line argument. The default mode is now `auto`, which runs the chat example when LLM credentials are configured and otherwise falls back to the original Agent-Based Model (ABM) simulation (`example` mode). A `survey` mode is also available as a placeholder.

#### Run from the command line

- To run in auto mode (default):
    ```bash
    python3 -m gabm
    # or explicitly
    python3 -m gabm --mode auto
    ```
- To force the classic example simulation:
    ```bash
    python3 -m gabm --mode example
    ```
- To force the simple chat example:
    ```bash
    python3 -m gabm --mode chat
    ```
- To run the survey example:
    ```bash
    python3 -m gabm --mode survey
    ```

#### Run using the Makefile

The Makefile provides a `run-local` target for convenience. You can pass arguments to the program using the `ARGS` variable:

- To run in auto mode (default):
    ```bash
    make run-local
    # or explicitly
    make run-local ARGS="--mode auto"
    ```
- To force the classic example simulation:
    ```bash
    make run-local ARGS="--mode example"
    ```
- To force the simple chat example:
    ```bash
    make run-local ARGS="--mode chat"
    ```
- To run the survey example:
    ```bash
    make run-local ARGS="--mode survey"
    ```

To run the dedicated chat example simulation with ONS-backed names:

```bash
make run-example-chat
```

### Running the Chat Example and Interpreting Results

The chat example creates a small set of people and has them exchange LLM-generated messages in rounds. It is useful for testing:

- LLM provider wiring and model selection
- reproducibility behavior (same seed, with and without cache replay)
- output artifact generation for comparison across runs

Run with defaults:

```bash
make run-example-chat
```

Run with an explicit seed, provider, model, and run ID:

```bash
make run-example-chat SEED=42 LLM_SERVICE=openai LLM_MODEL=gpt-4o-mini RUN_ID=seed42_openai_a
```

Use an OpenAI request seed (best-effort deterministic sampling):

```bash
make run-example-chat SEED=42 LLM_SEED=42 RUN_ID=seed42_openai_seeded_a
```

Force live prompting (disable cache replay):

```bash
make run-example-chat SEED=42 NO_CACHE=1 RUN_ID=seed42_live_a
```

Each run writes outputs to:

- `data/output/examples/chat/<run-directory>/conversation_transcript.txt`
- `data/output/examples/chat/<run-directory>/console_output.txt`
- `data/output/examples/chat/<run-directory>/run_metadata.json`
- `data/output/examples/chat/<run-directory>/prompt_response_cache_delta.jsonl`

The `run_metadata.json` file records key run settings such as seed, provider, model, and whether cache was enabled.
For OpenAI-backed runs, it also records `llm_seed` and any observed `openai_system_fingerprints` values.

Compare two runs:

```bash
make compare-example-chat RUN_A=seed42_openai_a RUN_B=seed42_openai_b
```

Expected behavior:

- With cache replay enabled (default), repeating the same prompts typically yields identical transcripts.
- With `NO_CACHE=1`, prompts are sent live each time, so two same-seed runs may differ.
- For OpenAI live runs, using the same `LLM_SEED` and identical request settings improves reproducibility, but does not guarantee perfect determinism.
- If `openai_system_fingerprints` differs between runs, backend changes may explain output differences.
- Metadata comparison ignores volatile fields such as timestamp and run directory path.

What to expect from a normal run:

- The example creates two `Person` agents and prints their summaries (age, gender, name, interests, values).
- It prints `Participants: <name1> and <name2>` and then runs a 4-round alternating conversation (`Round 1` to `Round 4`).
- With default settings (`openai` + `gpt-4o-mini`), the dialogue is short and natural, focused on finding shared interests.
- You will usually see LLM cache/log lines in console output (for example cache updates and JSONL append confirmations).
- Run artifacts are written under `data/output/examples/chat/<run-directory>/` by default.

If you set `OUTPUT_ROOT=...`, run artifacts are written under the path you provide.

### Running Simple Chat Ensembles

For multi-run analysis of the simple chat simulation, run a seed-window sweep:

```bash
make run-example-chat-ensemble
```

Run a smaller exploratory sweep:

```bash
make run-example-chat-ensemble START_SEED=42 N_RUNS=5 RUN_ID=chat_small_01
```

Run a deliberately awkward, high-dissimilarity sweep:

```bash
make run-example-chat-ensemble START_SEED=42 N_RUNS=5 RUN_ID=chat_awkward_small CONVERSATION_MODE=awkward PAIRING_STRATEGY=max_dissimilarity CANDIDATE_POOL_SIZE=12
```

Default outputs are written under `data/output/examples/chat/ensembles/<sweep-directory>/`:

- `similarity_sweep_results.csv` (one row per run)
- `similarity_bin_summary.json` (aggregated metrics by shared-interest bin)
- `similarity_vs_transcript_size.png` (scatter plot)
- `sweep_metadata.json` (sweep configuration)
- `runs/` (full per-run artifacts from underlying chat runs)

Awkward-mode controls:

- `CONVERSATION_MODE=awkward` reduces explicit "find common ground quickly" behavior in prompts.
- `PAIRING_STRATEGY=max_dissimilarity` selects the most dissimilar pair from a generated candidate pool.
- `CANDIDATE_POOL_SIZE` controls how many candidates are generated before selecting the pair (must be `>= 2`; larger values increase chance of sharper contrast).

Useful columns in `similarity_sweep_results.csv` for awkward runs:

- `pair_dissimilarity_score`
- `first_shared_interest_round` (`-1` means no explicit shared-interest marker detected)
- `awkward_marker_count`
- `disagreement_marker_count`

### Running the Chat + Opinion Example

The chat+opinion example extends the simple chat by tracking each person's opinion of the other over multiple rounds.

Run with defaults:

```bash
make run-example-chat-opinion
```

Run with more rounds:

```bash
make run-example-chat-opinion ROUNDS=12
```

Run a deliberately awkward, high-dissimilarity variant:

```bash
make run-example-chat-opinion ROUNDS=12 CONVERSATION_MODE=awkward PAIRING_STRATEGY=max_dissimilarity CANDIDATE_POOL_SIZE=12
```

Outputs are written under `data/output/examples/chat_opinion/<run-directory>/` by default:

- `conversation_transcript.txt`
- `console_output.txt`
- `run_metadata.json`
- `opinion_history.json`
- `opinion_change.png`

What to expect:

- Two agents alternate turns for the configured number of rounds.
- A per-round opinion update is computed from conversation signals (for example engagement/affect cues and shared interests).
- Opinion trajectories for `A -> B` and `B -> A` are saved and plotted in `opinion_change.png`.

You can override the seed, year, and ONS file paths if needed:

```bash
make run-example-chat SEED=42 YEAR=2026 ONS_MALE=data/input/abm/names_england_wales_ons_male.csv ONS_FEMALE=data/input/abm/names_england_wales_ons_female.csv
```

### Running Chat + Opinion Ensembles

For multi-run analysis, the ensemble sweep runs many chat+opinion simulations across a seed window and aggregates similarity/outcome metrics.

Run with defaults:

```bash
make run-example-chat-opinion-ensemble
```

Run with explicit sweep settings:

```bash
make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=50 ROUNDS=10 RUN_ID=sim_sweep_01
```

Run an awkward, dissimilar pairing sweep:

```bash
make run-example-chat-opinion-ensemble START_SEED=100 N_RUNS=20 ROUNDS=10 RUN_ID=sim_sweep_awkward CONVERSATION_MODE=awkward PAIRING_STRATEGY=max_dissimilarity CANDIDATE_POOL_SIZE=12
```

Default outputs are written under `data/output/examples/chat_opinion/ensembles/<sweep-directory>/`:

- `similarity_sweep_results.csv` (one row per run)
- `similarity_bin_summary.json` (aggregated metrics by similarity bin)
- `similarity_vs_final_opinion.png` (scatter plot)
- `sweep_metadata.json` (sweep configuration)
- `runs/` (full per-run artifacts from underlying chat+opinion runs)

Notes:

- `pair_similarity_score` blends age similarity, gender similarity, and shared-interest overlap.
- The sweep is deterministic for fixed seeds when cache behavior and model backend remain stable.
- Use `NO_CACHE=1` when you specifically want to observe live-provider variability.
- `CONVERSATION_MODE=awkward` and `PAIRING_STRATEGY=max_dissimilarity` can produce slower rapport formation and more uneven dialogue.
- Additional per-run columns include `pair_dissimilarity_score`, `first_shared_interest_round`, `awkward_marker_count`, and `disagreement_marker_count`.

### Cost and HPC Guidance for Ensembles

Ensemble runs can consume API credits quickly when using hosted LLM services.

Why this happens:

- Each run creates multiple prompts, and total prompt count scales approximately with `N_RUNS x ROUNDS`.
- Conversation histories diverge quickly across seeds, so cache hits are often limited in ensemble workloads.
- Running with `NO_CACHE=1` sends every prompt live to the provider.

Recommended practice:

- Start with very small pilots (for example `N_RUNS=3` to `N_RUNS=10`) before scaling.
- Prefer local LLM execution for larger sweeps where possible.
- If you have access to HPC resources, use them for local-model ensembles and reserve hosted APIs for targeted validation runs.
- Keep hosted and local comparison runs aligned on configuration (seed windows, rounds, model settings, cache mode).

Suggested staged workflow:

1. Run a small hosted baseline for `chat` and `chat_opinion` ensembles.
2. Run matching local/HPC ensembles with the same seed window.
3. Compare aggregate outputs (`similarity_sweep_results.csv`, bin summaries, plots) across environments.
4. Scale up only after confirming the signal you care about is stable.

### Compare Hosted vs HPC Ensembles

Use the comparison utility to quantify differences between two sweep directories (for example hosted API vs local/HPC model runs):

```bash
make compare-ensemble-sweeps \
    SWEEP_A=data/output/examples/chat/ensembles/chat_small_01 \
    SWEEP_B=data/output/examples/chat/ensembles/chat_hpc_01 \
    LABEL_A=hosted \
    LABEL_B=hpc \
    RUN_ID=chat_compare_01
```

You can also compare chat_opinion sweeps the same way by pointing `SWEEP_A` and `SWEEP_B` to chat_opinion ensemble directories.

Outputs are written under `data/output/examples/ensembles/compare/<comparison-directory>/`:

- `comparison_report.json` (machine-readable deltas and per-bin comparisons)
- `comparison_summary.txt` (quick human-readable summary)

Interpretation tip:

- Treat exact transcript equality as non-goal across hosted vs local/HPC models.
- Focus on aggregate deltas in shared metrics (for example means and variability) and similarity-bin behavior.

### Compare Individual HPC Chat Runs

When comparing two individual HPC chat run directories (for example same seed across different server initializations), use:

```bash
make compare-hpc-chat-runs RUN_A=run_511621 RUN_B=run_511679
```

You can also pass full paths:

```bash
make compare-hpc-chat-runs RUN_A=/path/to/run_511621 RUN_B=/path/to/run_511679
```

If needed, override working directory resolution used for job IDs and `run_<id>` values:

```bash
make compare-hpc-chat-runs RUN_A=511621 RUN_B=511679 WORKING_DIR=/flash-calder/users/<user>/gabm
```

To generate markdown rows for reproducibility stress/concurrency summaries:

```bash
make summarize-hpc-concurrency INPUTS='--header --job-id 511621 --job-id 511679'
```

To generate a single markdown report that includes run manifest details, pairwise comparison summaries, and concurrency rows:

```bash
make report-hpc-chat-runs \
  INPUTS='--run /path/to/run_835891 --run /path/to/run_836062 --run /path/to/run_836067 --run /path/to/run_839326 --run /path/to/run_839328 --run /path/to/run_839329 --title Calder_HPC_reproducibility_report_Qwen3-14B' \
  OUTPUT=data/output/examples/chat/hpc/Calder/repro_report.md
```

In the chat example, participant names are now part of `Person` state:
- If a name is explicitly provided when creating a person, that name is used.
- If no name is provided, `Person` auto-assigns a name from the ONS files (using year of birth and gender).
- The chat simulation reads names directly from each person instance.

### Person Age and Date of Birth Modes

`Person` supports multiple ways to represent age information:

- exact year of birth via `year_of_birth`
- exact age in years via `age`
- age range in years via `age_min` and `age_max`
- full date of birth via `date_of_birth` (Python `datetime.date`)

Only one mode should be provided at initialization time.

When an age range is used, the model stores both bounds and computes a midpoint age for derived fields that require a single value.

Convenience methods:

- `get_age_range()` returns `(age_min, age_max)`
- `has_exact_age()` returns whether exact age is known
- `get_birthday_month_day()` returns `(month, day)` when a full date of birth is known
- `is_birthday(month, day)` checks whether a simulation date matches the person's birthday

### Temporal Precision and Uncertainty

For sub-year simulations (daily or weekly steps), temporal precision matters:

- `date_of_birth` gives highest precision: exact birthday detection is possible.
- `year_of_birth` gives annual precision only: age is known by year, but exact birthday within the year is unknown.
- `age` and `age_min`/`age_max` are coarser snapshots and should be treated as approximations over time.

This is important for high-detail digital-twin use cases (for example homes, workplaces, or neighborhoods) where some residents have exact birth dates and others have only approximate age data.

To support day-level stepping, `Environment` now maintains `current_date` and provides:

- `advance_day(days=..., birthday_callback=...)` to advance simulation calendar time
- `get_birthdays_on(date)` to query birthday matches among active people

Recommended practice for mixed-quality data:

- Use `date_of_birth` when known.
- Use `year_of_birth` when only year is known, and treat birthday timing as uncertain.
- Use `age_min`/`age_max` when only ranges are available and avoid event logic that depends on exact birthday timing.
- For random population generation, trait and interest generation use independent deterministic seeds so each can remain reproducible without introducing accidental coupling.


When you run GABM (e.g., with `python3 -m gabm`), the default behavior is to execute an Agent-Based Model (ABM) simulation. Here’s what happens:

### Agent Groups and Opinions

- The simulation creates three groups of agents: Negative, Positive, and Neutral.
- You can configure the number of agents in each group by editing variables at the top of the main script.
- Negative agents start with an opinion of -1.0, Positive agents with 1.0, and Neutral agents with 0.0.

### Communication Rounds

- The simulation runs for several rounds (configurable).
- In each round, agents from the Negative and Positive groups communicate with randomly selected Neutral agents.
- When a Neutral agent communicates, both the Neutral agent and the other agent update their opinions to the average of their current opinions. This models opinion mixing and convergence.


### Output and Visualization

- The simulation logs the state of the environment and the average opinion after each round to `data/logs/run_main.log`.
- After the simulation, a separate boxplot is generated for each opinion topic (negative, neutral, positive), showing the distribution of agent opinions at each round. These plots are saved as `opinions_negative.png`, `opinions_neutral.png`, and `opinions_positive.png` in `data/output`.
- The boxplots help visualize how opinions change and converge over time for each topic. You should see positive and negative opinions mix and converge, while neutral opinions may behave differently depending on the communication rules.
- The `data/logs` directory should contain `run_main.log`.

### Customization

- You can change the number of agents in each group, the number of rounds, and other parameters by editing the main script.
- The random seed is set for reproducibility, so results are consistent across runs unless you change the seed.

This ABM demonstration is a starting point, it does not show how LLMs can be used in an ABM yet!


## Trait State Modeling

`Person` now supports layered trait state designed for richer cognitive/social simulations:

- `initial_trait_values`: immutable canonical starting values (includes the Big Five by default).
- `base_traits`: mutable trait values that can evolve during simulation.
- `trait_beliefs`: structured beliefs for:
    - self-trait opinions;
    - first-order opinions about others' traits;
    - higher-order opinions (e.g., another person's opinion of traits).

### Reflection updates

Use `reflect_on_traits()` to move mutable base traits toward self-perceived trait values:

```python
person.set_self_trait_opinion(TraitTopicID(0), 2.0)
person.reflect_on_traits(learning_rate=0.25, seed=123)
```

This keeps initial canonical values unchanged while allowing state evolution in simulation.

### Reproducible trait snapshots

For checkpointing and replay, use:

```python
state = person.export_trait_state()
person.import_trait_state(state)
```

The exported state includes canonical initial values, mutable base traits, and structured trait beliefs.


## Managing Logs and Caches

GABM creates logs and caches (such as prompt/response caches for LLM services and logs for ABM runs) that can grow large over time. Logs for LLM modules are written to `data/logs/llm/`, and logs for ABM runs are written to `data/logs/run_main.log`.

Check these log files for troubleshooting API issues, prompt/response errors, or cache problems. User-friendly ways to tidy up logs and caches and compile data into reproducible research objects are being developed for a future release. More details will be provided as these features are implemented.


## Using LLM Modules

GABM provides unified interfaces for sending prompts to various LLMs and listing available models. Each LLM module exposes a service class with the following functions:
```python
def send(self, api_key, message, model=None):
    """
    Send a prompt to the LLM and return the response object.
    Args:
        api_key (str): The API key for the LLM service.
        message (str): The message to send.
        model (str, optional): The model to use for the request.
    Returns:
        The response object from the LLM.
    """

def list_available_models(self, api_key):
    """
    List available models for the LLM service.
    Args:
        api_key (str): The API key for the LLM service.
    Returns:
        A list of available models.
    """
```

Caching and Logging:
- Responses are cached for reproducibility; repeated prompts return cached results.
- All send/responses are logged for audit and debugging.

Example Usage (where ```<User_API_Key>``` should be replaced with the user's API key for the OpenAI Service):
```python
from gabm.io.llm.openai import OpenAIService
service = OpenAIService()
response = service.send(api_key="<User_API_Key>", message="Hello!", model="gpt-3.5-turbo")
service.list_available_models(api_key="<User_API_Key>")
```

The `data/logs/llm` directory is for log files for each LLM service used.

The `data/llm` directory is for caches of prompts and responses for each LLM service used.


## Troubleshooting

If you encounter errors, check your Python version and that all dependencies are installed. If all versions match the documentation, please peruse [reported issues](https://github.com/compolis/GABM/issues), comment on a relevant open issue or [open an issue](https://github.com/compolis/GABM/issues/new/choose) to request support.


## Additional Resources

- [README.md](README.md)
- [Reported Issues](https://github.com/compolis/GABM/issues)
- [Running on HPC systems](Running_On_HPC_Systems.md)
