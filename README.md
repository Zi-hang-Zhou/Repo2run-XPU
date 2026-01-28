从 python329.jsonl 开始运行 Repo2Run
1. 环境准备

安装依赖
pip install -r requirements.txt

设置必需的环境变量
export OPENAI_API_KEY="sk-..."           
export OPENAI_BASE_URL="..."             

可选：启用 XPU 知识库
export dns=postgresql://zihang:123456@localhost:5433/xpu_db

2. 运行方式
方式 A：处理单个仓库

python build_agent/main.py \
  --full_name "wireless-innovation-forum/spectrum-access-system" \
  --sha "928c3150adf7b31e53a96b695bf1fbdd3284ecb2" \
  --root_path . \
  --llm "gpt-4o-2024-05-13"
方式 B：批量处理所有仓库

步骤 1: 生成任务列表
python generate_tasks.py
生成 tasks.txt

步骤 2: 多进程并行运行
python build_agent/multi_main.py tasks.txt

3. python329.jsonl 数据格式
每行是一个 JSON 对象：
{"repository": "author/repo-name", "revision": "commit_sha_40_chars"}

4. 输出位置
处理完成后，结果保存在 output/{author}/{repo}/：

文件	说明
Dockerfile	生成的可运行 Docker 配置
track.json	完整的 LLM 对话历史
inner_commands.json	容器内执行的命令
outer_commands.json	容器外执行的命令
pipdeptree.json	依赖树
test.txt	pytest 输出
5. 完整流程图

python329.jsonl → generate_tasks.py → tasks.txt
                                          ↓
                               multi_main.py (并行)
                                          ↓
                    [每个仓库] git clone → Docker 容器 → LLM 循环配置
                                          ↓
                               output/{author}/{repo}/Dockerfile
6. 可选参数

--enable_xpu    启用知识库检索（需配置数据库）
--online_xpu    启用在线经验提取
--max_turn 100  最大 LLM 交互轮次
