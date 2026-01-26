#!/usr/bin/env python3
"""
分析XPU消融实验结果
对比带XPU和不带XPU的实验效果
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def analyze_track_json(track_path):
    """分析track.json文件，提取关键指标"""
    try:
        with open(track_path, 'r') as f:
            data = json.load(f)

        # 统计对话轮数（只统计assistant消息）
        assistant_turns = sum(1 for msg in data if msg.get('role') == 'assistant')

        # 检查是否成功（最后是否有"success"标记）
        success = False
        final_message = ""
        if data:
            last_msg = data[-1]
            content = last_msg.get('content', '')
            if 'success' in content.lower() or 'pass' in content.lower():
                success = True
            final_message = content[:200] if content else ""

        return {
            'turns': assistant_turns,
            'success': success,
            'final_message': final_message,
            'total_messages': len(data)
        }
    except Exception as e:
        return {
            'turns': 0,
            'success': False,
            'final_message': f"Error: {e}",
            'total_messages': 0
        }

def collect_results(output_dir, repo_list):
    """收集指定仓库列表的实验结果"""
    results = {}

    for repo in repo_list:
        track_path = output_dir / repo / 'track.json'
        if track_path.exists():
            results[repo] = analyze_track_json(track_path)
        else:
            results[repo] = {
                'turns': 0,
                'success': False,
                'final_message': 'track.json not found',
                'total_messages': 0
            }

    return results

def compare_results(baseline_results, treatment_results):
    """对比baseline和treatment的结果"""

    comparison = []

    for repo in baseline_results.keys():
        baseline = baseline_results[repo]
        treatment = treatment_results.get(repo, {})

        comparison.append({
            'repo': repo,
            'baseline_turns': baseline['turns'],
            'treatment_turns': treatment.get('turns', 0),
            'baseline_success': baseline['success'],
            'treatment_success': treatment.get('success', False),
            'turn_diff': baseline['turns'] - treatment.get('turns', 0)
        })

    return comparison

def print_summary(comparison):
    """打印对比结果摘要"""

    print("=" * 80)
    print("XPU消融实验结果摘要")
    print("=" * 80)

    baseline_success = sum(1 for c in comparison if c['baseline_success'])
    treatment_success = sum(1 for c in comparison if c['treatment_success'])

    baseline_avg_turns = sum(c['baseline_turns'] for c in comparison) / len(comparison) if comparison else 0
    treatment_avg_turns = sum(c['treatment_turns'] for c in comparison) / len(comparison) if comparison else 0

    print(f"\n总体统计:")
    print(f"  实验仓库数量: {len(comparison)}")
    print(f"  Baseline (不带XPU):")
    print(f"    - 成功数量: {baseline_success}")
    print(f"    - 成功率: {baseline_success/len(comparison)*100:.1f}%")
    print(f"    - 平均对话轮数: {baseline_avg_turns:.1f}")
    print(f"  Treatment (带XPU):")
    print(f"    - 成功数量: {treatment_success}")
    print(f"    - 成功率: {treatment_success/len(comparison)*100:.1f}%")
    print(f"    - 平均对话轮数: {treatment_avg_turns:.1f}")

    print(f"\n对比:")
    print(f"  成功率提升: {(treatment_success - baseline_success) / len(comparison) * 100:.1f}%")
    print(f"  平均轮数减少: {baseline_avg_turns - treatment_avg_turns:.1f}")

    # XPU带来改进的案例
    improved = [c for c in comparison if c['treatment_success'] and not c['baseline_success']]
    if improved:
        print(f"\nXPU带来改进的案例 ({len(improved)}个):")
        for c in improved[:5]:  # 只显示前5个
            print(f"  - {c['repo']}")

    # XPU导致退化的案例
    degraded = [c for c in comparison if not c['treatment_success'] and c['baseline_success']]
    if degraded:
        print(f"\nXPU导致退化的案例 ({len(degraded)}个):")
        for c in degraded[:5]:  # 只显示前5个
            print(f"  - {c['repo']}")

    print("=" * 80)

def save_detailed_results(comparison, output_file):
    """保存详细的对比结果到CSV文件"""

    with open(output_file, 'w') as f:
        # 写入表头
        f.write("repo,baseline_turns,treatment_turns,turn_diff,baseline_success,treatment_success\n")

        # 写入每个仓库的结果
        for c in comparison:
            f.write(f"{c['repo']},{c['baseline_turns']},{c['treatment_turns']},{c['turn_diff']},{c['baseline_success']},{c['treatment_success']}\n")

    print(f"\n详细结果已保存到: {output_file}")

def main():
    # 读取任务列表
    with open('python329.jsonl', 'r') as f:
        repos = [json.loads(line)['repository'] for line in f.readlines()[:50]]

    output_dir = Path('output')

    print("正在收集实验结果...")

    # 假设我们会在不同的output目录中运行实验
    # 为了简化，我们先检查当前output目录

    # 这里需要用户告诉我们baseline和treatment的output目录位置
    # 暂时假设：
    # - output_baseline: baseline实验结果
    # - output_treatment: treatment实验结果

    print("\n注意: 请确保已经运行了两组实验，并且结果分别保存在:")
    print("  - output_baseline/: 不带XPU的baseline实验")
    print("  - output_treatment/: 带XPU的treatment实验")
    print()

    baseline_dir = Path('output_baseline')
    treatment_dir = Path('output_treatment')

    if not baseline_dir.exists() or not treatment_dir.exists():
        print("警告: 实验结果目录不存在！")
        print("请先运行实验:")
        print("  1. 运行baseline: python build_agent/multi_main.py tasks_without_xpu.txt")
        print("     然后将output/重命名为output_baseline/")
        print("  2. 运行treatment: python build_agent/multi_main.py tasks_with_xpu.txt")
        print("     然后将output/重命名为output_treatment/")
        return

    baseline_results = collect_results(baseline_dir, repos)
    treatment_results = collect_results(treatment_dir, repos)

    comparison = compare_results(baseline_results, treatment_results)

    print_summary(comparison)
    save_detailed_results(comparison, 'ablation_results.csv')

if __name__ == '__main__':
    main()
