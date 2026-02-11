#!/usr/bin/env python3
"""
将 human-in-the-loop 的顽固 bad case 注入到 XPU 数据库中。

使用方法:
    python scripts/inject_badcases_to_db.py --input human_in_loop_badcases.json

环境变量:
    dns: PostgreSQL 连接字符串 (默认使用 5433 端口的 v18 数据库)
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / ".env")

# 设置默认使用 v18 数据库 (端口 5433)
DEFAULT_DNS = "postgresql://zihang:123456@localhost:5433/xpu_db"

def get_dns():
    """获取数据库连接字符串，优先使用 v18 (5433 端口)"""
    dns = os.environ.get("dns")
    if dns and "5433" in dns:
        return dns
    # 如果环境变量没有设置 5433，使用默认值
    return DEFAULT_DNS


def inject_badcases(input_file: str, dry_run: bool = False):
    """将 bad case 注入数据库"""

    # 加载 bad case 文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    badcases = data.get('badcases', [])
    print(f"📂 加载了 {len(badcases)} 个 bad case")

    if dry_run:
        print("\n🔍 Dry Run 模式 - 仅显示将要注入的条目:")
        for bc in badcases:
            print(f"  - {bc['id']}: {bc['type']}")
        return

    # 连接数据库
    dns = get_dns()
    print(f"🔗 连接数据库: {dns.replace(dns.split(':')[2].split('@')[0], '***')}")

    try:
        from xpu.xpu_vector_store import XpuVectorStore, text_to_embedding, build_xpu_text
        from xpu.xpu_adapter import XpuEntry, XpuAtom
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保在项目根目录运行此脚本")
        sys.exit(1)

    # 临时设置 dns 环境变量
    os.environ["dns"] = dns

    try:
        store = XpuVectorStore(connection_string=dns)
        print("✅ 数据库连接成功")
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        sys.exit(1)

    # 注入每个 bad case
    success_count = 0
    for bc in badcases:
        try:
            # 构建 XpuEntry
            atoms = [XpuAtom(name=a["name"], args=a["args"]) for a in bc.get("atoms", [])]

            entry = XpuEntry(
                id=bc["id"],
                context=bc["context"],
                signals=bc["signals"],
                advice_nl=bc["advice_nl"],
                atoms=atoms
            )

            # 生成 embedding 文本
            text = build_xpu_text(entry)
            print(f"\n📝 处理: {bc['id']}")
            print(f"   类型: {bc['type']}")
            print(f"   文本长度: {len(text)} 字符")

            # 生成 embedding
            embedding = text_to_embedding(text)
            print(f"   Embedding 维度: {len(embedding)}")

            # 插入数据库
            store.upsert_entry(entry, embedding)
            print(f"   ✅ 成功插入")
            success_count += 1

        except Exception as e:
            print(f"   ❌ 插入失败: {e}")

    store.close()
    print(f"\n{'='*50}")
    print(f"📊 注入完成: {success_count}/{len(badcases)} 成功")
    print(f"{'='*50}")


def main():
    parser = argparse.ArgumentParser(description="将顽固 bad case 注入 XPU 数据库")
    parser.add_argument("--input", "-i", type=str, default="human_in_loop_badcases.json",
                        help="Bad case JSON 文件路径")
    parser.add_argument("--dry-run", "-n", action="store_true",
                        help="仅显示将要注入的条目，不实际执行")
    parser.add_argument("--dns", type=str, default=None,
                        help="数据库连接字符串 (覆盖环境变量)")

    args = parser.parse_args()

    if args.dns:
        os.environ["dns"] = args.dns

    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = ROOT_DIR / input_path

    if not input_path.exists():
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    inject_badcases(str(input_path), dry_run=args.dry_run)


if __name__ == "__main__":
    main()
