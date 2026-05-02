# R2R Benchmark100_v2 评测报告

## 概览

- 使用 Repo2Run（原版，不含 XPU）对 100 个开源 Python 仓库执行自动化环境部署
- 部署产物（Dockerfile）经 Phase2 Verifier（Prosecutor + Judge）进行质量验证
- LLM：qwen3.5-plus | Embedding：text-embedding-3-small
- R2R 超时：3600s

## 数据来源

| 来源 | 数量 | 说明 |
|------|------|------|
| benchmark100_v1 旧结果 | 80 | 与 v1 重叠的仓库，直接复用旧 Phase2 结果 |
| benchmark100_v2 新增 | 20 | v2 新增仓库，使用新跑的 R2R + Phase2 结果 |

## 总体结果

| 阶段 | 状态 | 数量 |
|------|------|------|
| R2R 部署 | 成功生成 Dockerfile | 91 |
| | 超时失败 (>3600s) | 9 |
| Phase2 验证 | not_guilty（环境正确） | 45 |
| | guilty（环境有缺陷） | 19 |
| | Docker 构建失败 | 27 |
| | 无 Dockerfile（R2R 超时跳过） | 9 |

## 关键指标

- R2R 部署成功率：91/100 = **91.0%**（按 R2R 声称的标准）
- Dockerfile 可构建率（供 verifier 构建的）：64/91 = **70.3%**
- 端到端成功率（not_guilty / 总数）：45/100 = **45.0%**

## 修正说明

kedro、py-evm、twine 三个仓库原判 Docker 构建失败，原因是构建上下文中缺少 R2R 生成的 `search_patch` 辅助文件（`COPY failed: file not found`），属于验证流程的问题而非 R2R 本身的 Dockerfile 质量缺陷。修复构建上下文后重新验证，Phase2 均判定为 not_guilty。

## not_guilty 仓库（45 个）

- reagento/adaptix (74s)
- tishka17/aiogram_dialog (70s)
- dtmilano/androidviewclient (100s)
- openml/automlbenchmark (271s)
- cherrypy/cheroot (93s)
- idaholab/civet (251s)
- columnflow/columnflow (156s)
- spec-first/connexion (89s)
- cookiecutter/cookiecutter (152s)
- materialsproject/custodian (215s) ★
- datamol-io/datamol (248s)
- fabric/fabric (105s)
- flav-io/flavio (293s)
- python/importlib_metadata (172s)
- kedro-org/kedro (1069s) ※
- kerneltuner/kernel_tuner (155s)
- jaraco/keyring (76s)
- tommadness/KH2Randomizer
- lark-parser/lark (73s)
- HazyResearch/meerkat (570s)
- ansible/molecule (421s)
- embeddings-benchmark/mteb (2262s)
- piccolo-orm/piccolo (930s)
- jazzband/pip-tools (322s)
- has2k1/plotnine (298s)
- python-poetry/poetry (147s)
- ethereum/py-evm (1985s) ※
- giampaolo/pyftpdlib (72s)
- pypose/pypose (328s)
- pytest-dev/pytest-xdist (98s)
- python-control/python-control (238s)
- vacanza/python-holidays (272s)
- juju/python-libjuju (153s) ★
- hhursev/recipe-scrapers (291s)
- robotframework/robotframework (136s)
- theislab/scvelo (663s)
- piskvorky/smart_open (172s)
- sphinx-gallery/sphinx-gallery (185s)
- jazzband/tablib (74s)
- pypa/twine (123s) ※
- lmcinnes/umap (455s)
- yt-project/unyt (113s)
- jazzband/wagtailmenus (113s)
- xknx/xknx (121s)
- google/yapf (51s)

> ★ 标记为 v2 新增仓库
> ※ 原判 Docker 构建失败（缺 search_patch），修复后重验为 not_guilty

## guilty 仓库（19 个）

主要问题为核心依赖缺失或版本不兼容：

### 核心依赖缺失（19 个）

- ajenti/ajenti
- castagnait/plugin.video.netflix
- conda-forge/staged-recipes
- dj-stripe/dj-stripe
- dnarayanan/powderday
- facebookresearch/nevergrad
- fixator10/fixator10-cogs
- flask-middleware/flask-security
- guardrails-ai/guardrails
- lichess4545/heltour
- mampfes/hacs_waste_collection_schedule
- materialsvirtuallab/monty
- ourresearch/oadoi
- pureqml/qmlcore
- pypa/pip
- roboflow/supervision
- tmux-python/tmuxp
- ubernostrum/django-registration ★
- uploadcare/pyuploadcare

## Docker 构建失败分析（27 个）

### Shell 转义问题（2 个）

- neurogym/neurogym
- openqasm/openqasm

### git clone 失败（2 个）

- nixtla/neuralforecast
- terrapower/armi

### pip install 失败（9 个）

- google/trax
- jageo/lobsterpy
- mopidy/mopidy
- online-ml/river
- posit-dev/great-tables
- pretalx/pretalx
- spotify/luigi
- sublimelinter/sublimelinter
- torchgeo/torchgeo

### poetry install 失败（4 个）

- fhempy/fhempy
- gazzolalab/miv-os
- nonebot/nonebot2
- yubico/yubikey-manager

### 其他（8 个）

- emi-group/evox
- huggingface/datasets
- jacebrowning/memegen
- langchain-ai/langgraph
- platformio/platformio-core
- tortoise/tortoise-orm
- uriyyo/fastapi-pagination
- yourlabs/django-autocomplete-light

### 引用不存在的命令/工具（2 个）

- facebookresearch/hydra
- google-deepmind/acme

## R2R 超时失败（9 个）

- theislab/cellrank
- diefenbach/django-lfs
- giskard-ai/giskard
- iree-org/iree-llvm-sandbox ★
- llm-random/llm-random ★
- Modalities/modalities ★
- naomiproject/naomi ★
- netbox-community/netbox
- qiita-spots/qiita ★

## 结论

1. R2R 部署成功率较高（91/100 = 91.0%），9 个失败均为超时
2. 主要瓶颈在 Dockerfile 质量：27 个（占部署成功的 29.7%）构建失败
3. 在构建成功的 64 个仓库中，Phase2 验证通过率 45/64 = 70.3%，19 个 guilty 主要因核心依赖缺失
4. 最终成功率 45/100 = 45.0%
