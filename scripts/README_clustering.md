# Repo2Run 聚类分析使用指南

本文档说明如何使用聚类分析工具对 XPU 经验单元和仓库执行轨迹进行聚类分析。

## 功能概览

提供两种聚类分析视角：

1. **XPU 视角** - 对经验单元（XPU）进行聚类
   - 基于: `advice_nl` + `keywords` + `tools` 的组合文本
   - 目的: 发现相似的问题解决模式
   - 输出: XPU 聚类结果和特征分析

2. **仓库视角** - 对仓库执行轨迹进行聚类
   - 基于: 执行轨迹中的 `thoughts` 和 `observations`
   - 目的: 发现相似的配置流程模式
   - 输出: 仓库聚类结果和交互特征

## 快速开始

### 安装依赖

```bash
pip install pandas scikit-learn matplotlib numpy
```

### 运行聚类分析

#### 1. XPU 视角聚类

```bash
# 基础用法（10个聚类）
python scripts/analyze_clusters_enhanced.py --perspective xpu

# 自定义聚类数量
python scripts/analyze_clusters_enhanced.py --perspective xpu --n_clusters 15

# 指定输出目录
python scripts/analyze_clusters_enhanced.py --perspective xpu --output_dir ./my_results
```

#### 2. 仓库视角聚类

```bash
# 基础用法（10个聚类）
python scripts/analyze_clusters_enhanced.py --perspective repository

# 自定义聚类数量
python scripts/analyze_clusters_enhanced.py --perspective repository --n_clusters 8
```

#### 3. 同时进行两种聚类

```bash
# 一次性完成两种聚类分析
python scripts/analyze_clusters_enhanced.py --perspective both --n_clusters 10
```

##  输出文件说明

所有结果默认保存在 `clustering_results/` 目录下：

### XPU 视角输出

1. **xpu_clusters.csv** - 详细聚类结果
   - 列: `xpu_id`, `repo`, `cluster_id`, `tools`, `keywords`, `advice`
   - 每行代表一个 XPU 及其聚类分配

2. **xpu_cluster_stats.csv** - 聚类统计
   - 列: `cluster_id`, `size`, `top_repos`, `top_tools`
   - 每行代表一个聚类的汇总信息

3. **xpu_clusters_visualization.png** - 可视化图
   - PCA 降维到 2D 的聚类可视化
   - 不同颜色代表不同聚类

### 仓库视角输出

1. **repository_clusters.csv** - 详细聚类结果
   - 列: `repo_name`, `cluster_id`, `num_turns`, `num_commands`, `thoughts_text`
   - 每行代表一个仓库及其聚类分配

2. **repository_cluster_stats.csv** - 聚类统计
   - 列: `cluster_id`, `size`, `avg_turns`, `avg_commands`, `repos`
   - 每行代表一个聚类的汇总信息

3. **repository_clusters_visualization.png** - 可视化图
   - PCA 降维到 2D 的聚类可视化

## 分析结果解读

### XPU 聚类特征

每个 XPU 聚类可能代表：
- **相似的错误类型** - 例如：版本冲突、依赖缺失、测试失败
- **相似的解决方案** - 例如：安装特定包、修改配置、代码编辑
- **特定工具/框架** - 例如：Django、pytest、poetry 相关问题

### 仓库聚类特征

每个仓库聚类可能代表：
- **配置复杂度** - 交互轮数多的 vs 简单的
- **依赖管理方式** - Poetry vs pip vs conda
- **常见问题模式** - 测试失败、导入错误、版本不兼容

##  高级用法

### 调整聚类数量

根据数据规模选择合适的聚类数量：
- XPU 数据（61条）: 建议 5-15 个聚类
- 仓库数据（36个）: 建议 4-10 个聚类

```bash
# XPU 较少聚类（更粗粒度）
python scripts/analyze_clusters_enhanced.py --perspective xpu --n_clusters 5

# XPU 较多聚类（更细粒度）
python scripts/analyze_clusters_enhanced.py --perspective xpu --n_clusters 15
```

### 自定义输出目录

```bash
python scripts/analyze_clusters_enhanced.py \
  --perspective both \
  --n_clusters 10 \
  --output_dir ./analysis_results_2025
```

## 命令行参数说明

```
usage: analyze_clusters_enhanced.py [-h] [--perspective {xpu,repository,both}]
                                   [--n_clusters N_CLUSTERS]
                                   [--output_dir OUTPUT_DIR]

参数:
  -h, --help            显示帮助信息
  --perspective {xpu,repository,both}
                        聚类视角 (默认: both)
                        - xpu: 仅 XPU 聚类
                        - repository: 仅仓库聚类
                        - both: 两者都做
  --n_clusters N_CLUSTERS
                        聚类数量 (默认: 10)
  --output_dir OUTPUT_DIR
                        输出目录 (默认: ./clustering_results)
```

##  数据格式要求

### XPU 数据格式 (xpu_v1.jsonl)

每行一个 JSON 对象，必需字段：
```json
{
  "id": "xpu_xxx",
  "source": {"repo": "user/repo"},
  "signals": {"keywords": [...], "regex": [...]},
  "advice_nl": [...],
  "context": {"tools": [...]}
}
```

### 仓库轨迹数据格式 (output/user/repo/track.json)

JSON 数组，每个元素是一条消息：
```json
[
  {
    "role": "assistant",
    "content": "### Thought: ...\n### Action:\n```bash\n...\n```"
  },
  {
    "role": "system",
    "content": "### Observation:\n..."
  }
]


