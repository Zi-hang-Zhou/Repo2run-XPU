#!/usr/bin/env python3
"""
从 XPU 视角和仓库视角进行聚类分析
"""

import argparse
import json
import pandas as pd
from pathlib import Path
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# 定义路径
ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / 'data'
OUTPUT_DIR = ROOT_DIR / 'output'
XPU_FILE = ROOT_DIR / 'xpu_v1.jsonl'
RESULTS_DIR = ROOT_DIR / 'clustering_results'


def load_xpu_data():
    """从 xpu_v1.jsonl 加载数据"""
    records = []
    with open(XPU_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            xpu = json.loads(line)

            # 提取关键信息
            record = {
                'xpu_id': xpu.get('id', ''),
                'repo': xpu.get('source', {}).get('repo', 'unknown'),
                'dataset': xpu.get('source', {}).get('dataset', ''),
                'instance_id': xpu.get('source', {}).get('instance_id', ''),

                # 上下文信息
                'lang': ','.join(xpu.get('context', {}).get('lang', [])) if isinstance(xpu.get('context', {}).get('lang', []), list) else xpu.get('context', {}).get('lang', ''),
                'os': ','.join(xpu.get('context', {}).get('os', [])),
                'python_versions': ','.join(xpu.get('context', {}).get('python', [])),
                'tools': ','.join(xpu.get('context', {}).get('tools', [])),

                # 信号信息
                'keywords': ' '.join(xpu.get('signals', {}).get('keywords', [])),
                'regex_patterns': ' '.join(xpu.get('signals', {}).get('regex', [])),

                # 建议信息
                'advice': ' '.join(xpu.get('advice_nl', [])),

                # 组合文本（用于聚类）
                'text_for_clustering': '',

                'status': xpu.get('status', ''),
                'hits': xpu.get('telemetry', {}).get('hits', 0),
            }

            # 组合用于聚类的文本
            text_parts = [
                record['keywords'],
                record['advice'],
                record['tools'],
            ]
            record['text_for_clustering'] = ' '.join(filter(None, text_parts))

            records.append(record)

    return pd.DataFrame(records)


def load_repo_trajectories():
    """从各个仓库的 track.json 加载执行轨迹"""
    repo_data = []

    # 遍历 output 目录下的所有仓库
    for repo_dir in OUTPUT_DIR.iterdir():
        if not repo_dir.is_dir():
            continue

        for subrepo_dir in repo_dir.iterdir():
            if not subrepo_dir.is_dir():
                continue

            track_file = subrepo_dir / 'track.json'
            if not track_file.exists():
                continue

            try:
                with open(track_file, 'r', encoding='utf-8') as f:
                    trajectory = json.load(f)

                # 提取有用信息
                repo_name = f"{repo_dir.name}/{subrepo_dir.name}"

                # 收集所有 assistant 的思考和命令
                thoughts = []
                commands = []
                observations = []

                for msg in trajectory:
                    role = msg.get('role', '')
                    content = msg.get('content', '')

                    if role == 'assistant':
                        # 提取思考部分
                        if '### Thought:' in content:
                            thought = content.split('### Thought:')[1].split('###')[0].strip()
                            thoughts.append(thought)

                        # 提取命令部分
                        if '```bash' in content or '```diff' in content:
                            commands.append(content)

                    elif role == 'system':
                        # 提取观察结果
                        if '### Observation:' in content:
                            obs = content.split('### Observation:')[1].split('[Current directory]')[0].strip()
                            observations.append(obs[:500])  # 限制长度

                record = {
                    'repo_name': repo_name,
                    'num_turns': len(trajectory),
                    'num_thoughts': len(thoughts),
                    'num_commands': len(commands),
                    'thoughts_text': ' '.join(thoughts),
                    'commands_text': ' '.join(commands),
                    'observations_text': ' '.join(observations),
                    'text_for_clustering': ' '.join(thoughts + observations[:10]),  # 限制观察数量
                }

                repo_data.append(record)

            except Exception as e:
                print(f"Warning: Failed to load {track_file}: {e}")
                continue

    return pd.DataFrame(repo_data)


def cluster_by_xpu(df, n_clusters=10, save_dir=None):
    """
    以 XPU 视角进行聚类
    基于 advice_nl + keywords + tools 的组合文本
    """
    print(f"\n{'='*60}")
    print("XPU 视角聚类分析")
    print(f"{'='*60}")
    print(f"总 XPU 数量: {len(df)}")

    # 确保有文本数据
    df['text_for_clustering'] = df['text_for_clustering'].fillna('')

    # 过滤空文本
    df_filtered = df[df['text_for_clustering'].str.len() > 10].copy()
    print(f"有效 XPU 数量（文本长度 > 10）: {len(df_filtered)}")

    if len(df_filtered) < n_clusters:
        n_clusters = max(2, len(df_filtered) // 2)
        print(f"调整聚类数量为: {n_clusters}")

    # TF-IDF 向量化
    vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=2,
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(df_filtered['text_for_clustering'])
    print(f"向量维度: {vectors.shape}")

    # K-Means 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_filtered['cluster_id'] = kmeans.fit_predict(vectors)

    # 统计每个聚类
    print(f"\n聚类分布:")
    cluster_counts = df_filtered['cluster_id'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} 个 XPU")

    # 分析每个聚类的特征
    print(f"\n聚类特征分析:")
    for cluster_id in range(n_clusters):
        cluster_df = df_filtered[df_filtered['cluster_id'] == cluster_id]
        print(f"\n--- Cluster {cluster_id} ({len(cluster_df)} XPUs) ---")

        # 最常见的仓库
        top_repos = cluster_df['repo'].value_counts().head(3)
        print(f"  主要仓库: {', '.join([f'{repo}({cnt})' for repo, cnt in top_repos.items()])}")

        # 最常见的工具
        all_tools = ' '.join(cluster_df['tools'].dropna()).split(',')
        if all_tools and all_tools != ['']:
            tool_counts = Counter([t.strip() for t in all_tools if t.strip()])
            top_tools = tool_counts.most_common(3)
            print(f"  主要工具: {', '.join([f'{tool}({cnt})' for tool, cnt in top_tools])}")

        # 示例建议
        sample_advice = cluster_df['advice'].iloc[0][:200] if len(cluster_df) > 0 else ''
        print(f"  示例建议: {sample_advice}...")

    # 保存结果
    if save_dir:
        save_dir.mkdir(exist_ok=True, parents=True)

        # 保存详细结果
        result_df = df_filtered[[
            'xpu_id', 'repo', 'cluster_id', 'tools', 'keywords', 'advice'
        ]]
        csv_path = save_dir / 'xpu_clusters.csv'
        result_df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n✓ 详细结果已保存到: {csv_path}")

        # 保存聚类统计
        stats = []
        for cluster_id in range(n_clusters):
            cluster_df = df_filtered[df_filtered['cluster_id'] == cluster_id]
            stats.append({
                'cluster_id': cluster_id,
                'size': len(cluster_df),
                'top_repos': ', '.join(cluster_df['repo'].value_counts().head(3).index.tolist()),
                'top_tools': ', '.join([t for t, _ in Counter(' '.join(cluster_df['tools']).split(',')).most_common(3)]),
            })

        stats_df = pd.DataFrame(stats)
        stats_path = save_dir / 'xpu_cluster_stats.csv'
        stats_df.to_csv(stats_path, index=False, encoding='utf-8')
        print(f"✓ 聚类统计已保存到: {stats_path}")

        # 可视化（如果可能）
        try:
            visualize_clusters(vectors.toarray(), df_filtered['cluster_id'].values,
                             save_dir / 'xpu_clusters_visualization.png',
                             title='XPU Clustering Visualization')
        except Exception as e:
            print(f"Warning: 可视化失败: {e}")

    return df_filtered


def cluster_by_repository(df, n_clusters=10, save_dir=None):
    """
    以仓库视角进行聚类
    基于仓库执行轨迹中的 thoughts 和 observations
    """
    print(f"\n{'='*60}")
    print("仓库视角聚类分析")
    print(f"{'='*60}")
    print(f"总仓库数量: {len(df)}")

    # 确保有文本数据
    df['text_for_clustering'] = df['text_for_clustering'].fillna('')

    # 过滤空文本
    df_filtered = df[df['text_for_clustering'].str.len() > 10].copy()
    print(f"有效仓库数量（文本长度 > 10）: {len(df_filtered)}")

    if len(df_filtered) < n_clusters:
        n_clusters = max(2, len(df_filtered) // 2)
        print(f"调整聚类数量为: {n_clusters}")

    # TF-IDF 向量化
    vectorizer = TfidfVectorizer(
        max_df=0.8,
        min_df=1,
        max_features=1000,
        stop_words='english',
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(df_filtered['text_for_clustering'])
    print(f"向量维度: {vectors.shape}")

    # K-Means 聚类
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df_filtered['cluster_id'] = kmeans.fit_predict(vectors)

    # 统计每个聚类
    print(f"\n聚类分布:")
    cluster_counts = df_filtered['cluster_id'].value_counts().sort_index()
    for cluster_id, count in cluster_counts.items():
        print(f"  Cluster {cluster_id}: {count} 个仓库")

    # 分析每个聚类的特征
    print(f"\n聚类特征分析:")
    for cluster_id in range(n_clusters):
        cluster_df = df_filtered[df_filtered['cluster_id'] == cluster_id]
        print(f"\n--- Cluster {cluster_id} ({len(cluster_df)} 仓库) ---")

        # 仓库列表
        repos = cluster_df['repo_name'].tolist()[:5]
        print(f"  仓库示例: {', '.join(repos)}")

        # 平均轮数
        avg_turns = cluster_df['num_turns'].mean()
        avg_commands = cluster_df['num_commands'].mean()
        print(f"  平均交互轮数: {avg_turns:.1f}")
        print(f"  平均命令数: {avg_commands:.1f}")

        # 示例思考
        sample_thought = cluster_df['thoughts_text'].iloc[0][:200] if len(cluster_df) > 0 else ''
        print(f"  示例思考: {sample_thought}...")

    # 保存结果
    if save_dir:
        save_dir.mkdir(exist_ok=True, parents=True)

        # 保存详细结果
        result_df = df_filtered[[
            'repo_name', 'cluster_id', 'num_turns', 'num_commands', 'thoughts_text'
        ]]
        csv_path = save_dir / 'repository_clusters.csv'
        result_df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"\n✓ 详细结果已保存到: {csv_path}")

        # 保存聚类统计
        stats = []
        for cluster_id in range(n_clusters):
            cluster_df = df_filtered[df_filtered['cluster_id'] == cluster_id]
            stats.append({
                'cluster_id': cluster_id,
                'size': len(cluster_df),
                'avg_turns': cluster_df['num_turns'].mean(),
                'avg_commands': cluster_df['num_commands'].mean(),
                'repos': ', '.join(cluster_df['repo_name'].tolist()[:3]),
            })

        stats_df = pd.DataFrame(stats)
        stats_path = save_dir / 'repository_cluster_stats.csv'
        stats_df.to_csv(stats_path, index=False, encoding='utf-8')
        print(f"✓ 聚类统计已保存到: {stats_path}")

        # 可视化
        try:
            visualize_clusters(vectors.toarray(), df_filtered['cluster_id'].values,
                             save_dir / 'repository_clusters_visualization.png',
                             title='Repository Clustering Visualization')
        except Exception as e:
            print(f"Warning: 可视化失败: {e}")

    return df_filtered


def visualize_clusters(vectors, labels, save_path, title='Clustering Visualization'):
    """使用 PCA 降维并可视化聚类结果"""
    # PCA 降维到 2D
    pca = PCA(n_components=2, random_state=42)
    vectors_2d = pca.fit_transform(vectors)

    # 绘图
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1],
                         c=labels, cmap='tab10', alpha=0.6, s=50)
    plt.colorbar(scatter, label='Cluster ID')
    plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
    plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    print(f"✓ 可视化图已保存到: {save_path}")
    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="Repo2Run 聚类分析工具 - 支持 XPU 和仓库两种视角",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # XPU 视角聚类（10个簇）
  python scripts/analyze_clusters_enhanced.py --perspective xpu --n_clusters 10

  # 仓库视角聚类（8个簇）
  python scripts/analyze_clusters_enhanced.py --perspective repository --n_clusters 8

  # 同时进行两种聚类
  python scripts/analyze_clusters_enhanced.py --perspective both --n_clusters 10
        """
    )

    parser.add_argument(
        '--perspective',
        type=str,
        choices=['xpu', 'repository', 'both'],
        default='both',
        help="聚类视角: 'xpu' (经验单元), 'repository' (仓库), 'both' (两者都做)"
    )

    parser.add_argument(
        '--n_clusters',
        type=int,
        default=10,
        help="聚类数量（默认: 10）"
    )

    parser.add_argument(
        '--output_dir',
        type=str,
        default=None,
        help="输出目录（默认: ./clustering_results）"
    )

    args = parser.parse_args()

    # 确定输出目录
    if args.output_dir:
        save_dir = Path(args.output_dir)
    else:
        save_dir = RESULTS_DIR

    save_dir.mkdir(exist_ok=True, parents=True)

    print(f"\n{'='*60}")
    print("Repo2Run 聚类分析工具")
    print(f"{'='*60}")
    print(f"聚类视角: {args.perspective}")
    print(f"聚类数量: {args.n_clusters}")
    print(f"输出目录: {save_dir}")

    # 执行聚类
    if args.perspective in ['xpu', 'both']:
        print(f"\n加载 XPU 数据...")
        xpu_df = load_xpu_data()
        cluster_by_xpu(xpu_df, n_clusters=args.n_clusters, save_dir=save_dir)

    if args.perspective in ['repository', 'both']:
        print(f"\n加载仓库轨迹数据...")
        repo_df = load_repo_trajectories()
        if len(repo_df) > 0:
            cluster_by_repository(repo_df, n_clusters=args.n_clusters, save_dir=save_dir)
        else:
            print("警告: 未找到任何仓库轨迹数据")

    print(f"\n{'='*60}")
    print("聚类分析完成！")
    print(f"所有结果已保存到: {save_dir}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
