# Repo2Run Output - 50 Repos Batch Run (No XPU Baseline)

## Run Configuration

| Item | Value |
|---|---|
| LLM | `qwen3.5-plus` (via dmxapi) |
| XPU | Disabled (baseline mode) |
| Concurrency | 3 processes |
| Agent step limit | 100 steps |
| Agent time limit | 1 hour |
| Base image | `python:3.10` |

## Results Summary

| Metric | Count |
|---|---|
| Total repos | 50 |
| Success (pytest collect passed) | **43** |
| Agent completed but pytest failed | 1 |
| Agent timeout (1h limit, killed) | 6 |
| **Success rate** | **86%** |

## Output Structure

Each repo directory contains:

| File | Description |
|---|---|
| `Dockerfile` | Generated Dockerfile for reproducing the environment |
| `track.json` | Agent conversation trajectory (full LLM interaction log) |
| `track.txt` | Final status (`Generate success!` or error message) |
| `test.txt` | Collected pytest test cases (`pytest --collect-only` output) |
| `inner_commands.json` | Commands executed inside the Docker container |
| `outer_commands.json` | Commands/diffs executed outside the container |
| `pipdeptree.json` | Dependency tree (JSON format) |
| `pipdeptree.txt` | Dependency tree (text format) |
| `pip_list.json` | Installed pip packages |
| `sha.txt` | Git commit SHA used |
| `patch/` | Code patches applied (if any) |

## Detailed Results

### Successful Repos (43)

| # | Repository | Commit SHA | Tests Collected |
|---|---|---|---|
| 1 | adbar/trafilatura | `ee1865b` | 98 |
| 2 | alteryx/featuretools | `938a0f6` | 1,812 |
| 3 | amperser/proselint | `79b33e7` | 338 |
| 4 | ansible/molecule | `21ec29b` | 780 |
| 5 | beeware/briefcase | `5ccb0e5` | 3,695 |
| 6 | cantools/cantools | `8947f8e` | 442 |
| 7 | castagnait/plugin.video.netflix | `7accc24` | 0 * |
| 8 | dj-stripe/dj-stripe | `e9ee6b7` | 695 |
| 9 | dtmilano/androidviewclient | `c75c684` | 43 |
| 10 | embeddings-benchmark/mteb | `363a27e` | 5,713 |
| 11 | ethereum/py-evm | `ffce74f` | 152,247 |
| 12 | getsentry/sentry-python | `11d68ee` | 3,083 |
| 13 | giampaolo/pyftpdlib | `7e9988e` | 897 |
| 14 | guardrails-ai/guardrails | `a5c81e9` | 680 |
| 15 | has2k1/plotnine | `0368b66` | 531 |
| 16 | hips/autograd | `ac5c3ea` | 557 |
| 17 | huggingface/datasets | `224b4e6` | 3,107 |
| 18 | jacebrowning/memegen | `c11a423` | 288 |
| 19 | jazzband/pip-tools | `8b2d6ed` | 1,000 |
| 20 | jazzband/tablib | `7d6c58a` | 215 |
| 21 | kedro-org/kedro | `37ec20e` | 1,821 |
| 22 | lark-parser/lark | `f79772c` | 0 * |
| 23 | Lightning-AI/litgpt | `c04150` | 2,097 |
| 24 | lmcinnes/umap | `ef71aed` | 208 |
| 25 | mampfes/hacs_waste_collection_schedule | `90c534e` | 7 |
| 26 | mopidy/mopidy | `b3ac21c` | 1,158 |
| 27 | nixtla/neuralforecast | `cf89402` | 360 |
| 28 | nonebot/nonebot2 | `0554e4a` | 589 |
| 29 | online-ml/river | `0531d47` | 3,954 |
| 30 | piccolo-orm/piccolo | `1945476` | 893 |
| 31 | piskvorky/smart_open | `8a487ff` | 432 |
| 32 | platformio/platformio-core | `a7b3ded` | 241 |
| 33 | posit-dev/great-tables | `829d829` | 90 |
| 34 | pypa/pip | `b78d808` | 2,861 |
| 35 | pypa/twine | `63a0aaf` | 232 |
| 36 | python-control/python-control | `4242976` | 4,380 |
| 37 | python-poetry/poetry | `a84cd0f` | 2,917 |
| 38 | roboflow/supervision | `6af1ab3` | 1,106 |
| 39 | spec-first/connexion | `df9960b` | 803 |
| 40 | tmux-python/tmuxp | `79f82f5` | 1,023 |
| 41 | tortoise/tortoise-orm | `a1e42df` | 1,610 |
| 42 | uriyyo/fastapi-pagination | `94bfcb6` | 2,044 |
| 43 | vacanza/python-holidays | `da10b28` | 6,872 |

\* These repos have no standard pytest tests; `pytest --collect-only` returned exit code 5 ("no tests found"), which counts as a pass.

### Failed Repos (7)

#### Agent Timeout - 6 repos

These repos hit the 1-hour time limit. The agent process was force-killed (`os._exit(1)`), so no Dockerfile or test results were generated. Only intermediate files (`inner_commands.json`, `pipdeptree.json`, etc.) remain from in-progress agent work.

| # | Repository | Commit SHA | Failure Reason |
|---|---|---|---|
| 1 | cookiecutter/cookiecutter | `b63db3a` | Agent timeout (1h) |
| 2 | giskard-ai/giskard | `c92584e` | Agent timeout (1h) |
| 3 | google-deepmind/acme | `e210507` | Agent timeout (1h) |
| 4 | google/trax | `31022d6` | Agent timeout (1h) |
| 5 | skrub-data/skrub | `b6914e8` | Agent timeout (1h) |
| 6 | spotify/luigi | `eda8d65` | Agent timeout (1h) |

#### Agent Step Limit Reached - 1 repo

This repo completed the agent loop (100 steps) but `pytest --collect-only` never passed. A Dockerfile was generated via `integrate_dockerfile`, but the environment is not correctly configured.

| # | Repository | Commit SHA | Failure Reason |
|---|---|---|---|
| 7 | yourlabs/django-autocomplete-light | `d829891` | 100 steps exhausted, pytest failed |
