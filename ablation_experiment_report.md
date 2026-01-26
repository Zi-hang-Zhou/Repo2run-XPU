# XPU消融实验分析报告

## 1. 实验概述

本实验旨在评估XPU（经验知识库）对自动化环境配置任务的影响。通过对比使用XPU和不使用XPU两种条件下的实验结果，分析XPU对任务完成效率和成功率的贡献。

### 实验设置

| 项目 | 说明 |
|------|------|
| 实验仓库数量 | 50个 |
| Baseline组 | 不使用XPU经验知识库 |
| Treatment组 | 使用XPU经验知识库 |
| 最大对话轮数限制 | 100轮 |
| 成功标准 | 生成有效的Dockerfile |

## 2. 总体结果对比

| 指标 | Baseline (无XPU) | Treatment (有XPU) | 变化 |
|------|------------------|-------------------|------|
| 成功数 | 47 | 47 | +0 |
| 成功率 | 94.0% | 94.0% | +0.0% |
| 总对话轮数 | 2912 | 2680 | **-232 (-8.0%)** |
| 平均对话轮数 | 58.2 | 53.6 | **-4.6** |

## 3. 成功情况详细分析

### 3.1 完整对比 (50个仓库)

| 情况 | 数量 | 占比 | 说明 |
|------|------|------|------|
| 两者都成功 | 45 | 90.0% | 基础任务，两组都能完成 |
| 仅Baseline成功 | 2 | 4.0% | Treatment实验未完整运行 |
| 仅Treatment成功 | 2 | 4.0% | Baseline实验未完整运行 |
| 两者都失败 | 1 | 2.0% | 两组实验都未完整运行 |

### 3.2 实验完成情况说明

**注意**: 以下仓库的实验未完整运行（只有依赖分析数据，没有对话记录和Dockerfile）：

| 仓库 | Baseline状态 | Treatment状态 |
|------|--------------|---------------|
| neptune-ai/neptune-client | ✓ 完成 | ✗ 未完成 |
| plotly/dash-bio | ✓ 完成 | ✗ 未完成 |
| idaholab/civet | ✗ 未完成 | ✓ 完成 |
| quantumjot/btrack | ✗ 未完成 | ✓ 完成 |
| google/trax | ✗ 未完成 | ✗ 未完成 |

### 3.3 有效对比范围

剔除未完整运行的仓库后，**45个仓库**可用于有效对比分析。

## 4. 轮数变化分析 (45个共同成功仓库)

### 4.1 轮数差异显著的仓库 (差异>20轮)

| 仓库 | Baseline轮数 | Treatment轮数 | 轮数差 | 效果 |
|------|--------------|---------------|--------|------|
| artesiawater/hydropandas | 100 | 10 | **+90** | XPU大幅节省 |
| valory-xyz/trader | 100 | 10 | **+90** | XPU大幅节省 |
| qiboteam/qibo | 100 | 15 | **+85** | XPU大幅节省 |
| posit-dev/great-tables | 100 | 16 | **+84** | XPU大幅节省 |
| m-o-a-t/moat-mqtt | 100 | 35 | **+65** | XPU大幅节省 |
| flairNLP/fundus | 100 | 42 | **+58** | XPU大幅节省 |
| andreidrang/python-rucaptcha | 10 | 100 | -90 | XPU增加轮数 |
| gymrek-lab/TRTools | 21 | 100 | -79 | XPU增加轮数 |
| tortoise/tortoise-orm | 30 | 100 | -70 | XPU增加轮数 |

### 4.2 轮数变化汇总

| 类别 | 数量 | 详情 |
|------|------|------|
| XPU大幅节省轮数 (>50轮) | 6 | 平均节省 78.7 轮 |
| XPU增加轮数 (>50轮) | 3 | 平均增加 79.7 轮 |
| **净效果** | - | **节省 232 轮 (8.0%)** |

## 5. 关键指标总结

### 5.1 效率提升

```
总轮数减少: 2912 → 2680 = 节省 232 轮 (8.0%)
平均轮数减少: 58.2 → 53.6 = 节省 4.6 轮/仓库
```

### 5.2 XPU表现亮点

XPU在以下场景表现优异，将原本需要100轮（达到上限）的任务缩短到10-42轮：

| 仓库 | 节省轮数 | 节省比例 |
|------|----------|----------|
| artesiawater/hydropandas | 90轮 | 90% |
| valory-xyz/trader | 90轮 | 90% |
| qiboteam/qibo | 85轮 | 85% |
| posit-dev/great-tables | 84轮 | 84% |
| m-o-a-t/moat-mqtt | 65轮 | 65% |
| flairNLP/fundus | 58轮 | 58% |

### 5.3 XPU导致负效果的深入分析

以下3个仓库使用XPU后轮数反而大幅增加，深入分析发现了具体问题：

#### 案例1: andreidrang/python-rucaptcha (10轮 → 100轮)

**Baseline成功方案** (10轮):
```
pip install requests aiohttp msgspec tenacity → 设置环境变量 → runtest成功
```

**Treatment失败原因**:
- XPU推荐了**不相关的建议**：
  - `xpu_1829374650`: "检测到poetry.lock，需要安装Poetry" (但此项目不需要Poetry)
  - `xpu_2210000042`: "Ansible的pyproject.toml基于setuptools" (这不是Ansible项目!)
- Agent被误导，陷入使用`conflictlist`命令的死循环
- **错误执行61次**: "conflictlist command usage error"
- **重复下载23次**: 无效的download命令

**问题诊断**: XPU匹配了错误的项目类型，推荐了完全不适用的经验

---

#### 案例2: gymrek-lab/TRTools (21轮 → 100轮)

**Baseline成功方案** (21轮):
```
尝试多个numpy版本 → 安装最新numpy → 安装系统依赖(tabix, bcftools) → 成功
```

**Treatment失败原因**:
- XPU**重复推荐同一建议10+次**:
  - `xpu_2210000030`: "Cython 3.0引入破坏性变更，尝试pip install 'Cython<3'"
- Agent按建议尝试安装旧版numpy，但**陷入死循环**:
  - `pip install -q numpy==1.17.3` 执行了**96次**!
  - 错误: `NameError: name 'CCompiler' is not defined`
- 实际问题是numpy 1.17与Python 3.10不兼容，但XPU建议指向了Cython

**问题诊断**: XPU建议部分相关但不是根因，Agent被误导走入错误方向且无法自拔

---

#### 案例3: tortoise/tortoise-orm (30轮 → 100轮)

**Baseline成功方案** (30轮):
```
poetry install → 逐个安装缺失模块(asyncpg, pyodbc等) → 设置PYTHONPATH → 成功
```

**Treatment失败原因**:
- XPU推荐Poetry相关建议，Agent正确执行了`poetry install`
- 但之后陷入**asyncpg模块找不到**的死循环:
  - `ModuleNotFoundError: No module named 'asyncpg'` 出现**100次**
  - `pip install asyncpg` 执行了**45次**
  - `poetryruntest` 执行了**50次**
- Agent安装了模块但Poetry虚拟环境隔离导致运行时找不到

**问题诊断**: XPU建议正确但Agent执行后陷入环境问题，缺乏问题升级机制

---

### 5.4 XPU负效果根因分析

| 问题类型 | 出现次数 | 说明 |
|----------|----------|------|
| **推荐不相关经验** | 1个 | python-rucaptcha被匹配为Ansible项目 |
| **重复推荐无效建议** | 2个 | 同一XPU建议被推送10-20次 |
| **导致Agent死循环** | 3个 | 单一命令被重复执行45-96次 |
| **缺乏退出机制** | 3个 | 建议无效时无法自动放弃 |

### 5.5 改进建议(详细)

1. **提高匹配准确度**: 避免将python-rucaptcha匹配为Ansible项目
2. **去重机制**: 同一XPU建议最多推送3次，之后自动降权
3. **循环检测**: 当同一命令执行>5次失败时，触发策略切换
4. **对比学习**: 分析Baseline成功路径，学习正确的解决思路

## 6. 结论

### 6.1 核心结论

1. **总体效率提升8%**: 使用XPU后，总对话轮数从2912轮减少到2680轮，节省232轮

2. **成功率持平**: 两组实验成功率均为94%（在可比较的范围内）

3. **显著优势案例**: 6个仓库实现了50轮以上的节省，XPU帮助避免达到最大轮数限制

4. **需要优化的案例**: 3个仓库使用XPU后轮数反而增加，说明XPU匹配算法需要改进

### 6.2 XPU价值评估

| 评估维度 | 结论 | 评分 |
|----------|------|------|
| 效率提升 | 节省8%对话轮数 | ⭐⭐⭐⭐ |
| 成功率影响 | 持平 | ⭐⭐⭐ |
| 稳定性 | 有少数负面案例 | ⭐⭐⭐ |
| **综合评价** | **正向价值，有优化空间** | ⭐⭐⭐⭐ |

### 6.3 改进建议

1. **分析负面案例**: 深入研究andreidrang/python-rucaptcha等3个轮数增加的案例
2. **优化匹配算法**: 提高XPU经验与目标仓库的相关性匹配准确度
3. **动态控制策略**: 当检测到XPU建议无效时，自动降低其权重

---

*报告生成时间: 2025年1月24日*
*数据来源: /data/zihang/Repo2Run/output (Baseline) 和 /data/zihang/Repo2Run/output_treatment/output (Treatment)*
