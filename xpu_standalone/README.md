# XPU 经验知识库模块

独立的 XPU (Experience Unit) 经验知识库模块，可对接到任意 Agent 系统。

## 文件结构

```
xpu_standalone/
├── xpu_interface.py        # ⭐ 接口定义（数据结构 + 抽象类）
├── xpu_handler_v2.py       # ⭐ 推荐使用的新版实现
├── xpu_handler.py          # 旧版实现（兼容）
├── xpu_v1.jsonl            # 知识库数据（103 条经验）
├── xpu/                    # 核心模块
│   ├── xpu_adapter.py      # 数据结构定义
│   ├── xpu_vector_store.py # 向量数据库操作
│   └── ...
└── scripts/                # 管道脚本
    └── ...
```

## 环境依赖

```bash
pip install psycopg2-binary pgvector openai numpy
```

环境变量：
```bash
export dns="postgresql://user:pass@host:5433/db"  # 向量数据库连接
export OPENAI_API_KEY="sk-..."                    # 用于生成 embedding
```

---

## 对接方式（推荐 v2 接口）

### 1. 基本使用

```python
from xpu_handler_v2 import XpuHandler

# 初始化
handler = XpuHandler()

# 检索经验
result = handler.retrieve(sandbox_error_output)

if result.has_hints:
    # 直接将建议注入到 LLM prompt
    prompt += result.prompt_block

    # 获取检索到的经验 ID
    print(f"使用了 {len(result.hints)} 条经验: {result.ids}")

# 反馈（可选，用于优化检索质量）
handler.feedback(result.ids, is_helpful=True)

# 关闭连接
handler.close()
```

### 2. 自定义配置

```python
from xpu_handler_v2 import XpuHandler
from xpu_interface import XpuConfig

config = XpuConfig(
    database_url="postgresql://user:pass@host:5433/db",
    top_k=5,                    # 返回前 5 条
    min_similarity=0.4,         # 最小相似度 0.4
    max_log_length=6000,        # 日志最大长度
)

handler = XpuHandler(config=config)
```

### 3. 完整 Agent 集成示例

```python
from xpu_handler_v2 import XpuHandler

class MyAgent:
    def __init__(self):
        self.xpu = XpuHandler()
        self.last_xpu_ids = []

    def run_step(self, sandbox_output: str):
        # 1. 检索经验
        result = self.xpu.retrieve(sandbox_output)

        # 2. 构建 prompt
        prompt = self.build_base_prompt()
        if result.has_hints:
            prompt += "\n\n" + result.prompt_block
            self.last_xpu_ids = result.ids

        # 3. 调用 LLM
        response = self.call_llm(prompt)
        return response

    def on_task_complete(self, success: bool):
        # 反馈本次任务使用的经验是否有效
        if self.last_xpu_ids:
            self.xpu.feedback(self.last_xpu_ids, is_helpful=success)
        self.xpu.close()
```

---

## 核心接口

### XpuRetrievalResult（检索结果）

```python
@dataclass
class XpuRetrievalResult:
    prompt_block: str       # 可直接注入 prompt 的文本
    hints: List[XpuHint]    # 检索到的经验列表

    @property
    def ids(self) -> List[str]     # 所有经验 ID
    @property
    def has_hints(self) -> bool    # 是否有结果
```

### XpuHint（单条经验）

```python
@dataclass
class XpuHint:
    id: str                 # 经验 ID
    similarity: float       # 相似度 (0-1)
    advice: List[str]       # 建议列表
    context: Dict           # 上下文
```

### XpuHandler（主类）

```python
class XpuHandler:
    def __init__(config: XpuConfig = None)
    def retrieve(error_log: str) -> XpuRetrievalResult
    def feedback(hint_ids: List[str], is_helpful: bool)
    def close()
```

---

## 兼容旧接口

如果你之前使用的是旧版接口，仍然可以使用：

```python
from xpu_handler_v2 import XpuHandler

handler = XpuHandler()

# 旧接口（兼容）
hint_block, xpu_ids, candidates_info = handler.retrieve_hints(sandbox_output)
handler.finalize_session(is_task_success=True)
```

---

## 数据格式 (xpu_v1.jsonl)

每行是一条经验记录：

```json
{
  "id": "xpu_xxx",
  "context": {
    "lang": "python",
    "os": ["linux"],
    "python": ["3.10"],
    "tools": ["pytest", "pip"]
  },
  "signals": {
    "regex": ["ModuleNotFoundError: No module named 'xxx'"],
    "keywords": ["ImportError", "pip install"]
  },
  "advice_nl": [
    "安装缺失的模块: pip install xxx",
    "检查依赖版本是否兼容"
  ],
  "atoms": [
    {"name": "pip_install", "args": {"package": "xxx"}}
  ]
}
```

---

## 管道脚本

| 脚本 | 作用 |
|------|------|
| `scripts/run_xpu_pipeline.py` | 完整管道：轨迹 → 提取 → 索引 |
| `scripts/index_xpu_to_vector_db_enhanced.py` | 向量索引入库 |
| `scripts/test_xpu_db_connection.py` | 测试数据库连接 |
| `scripts/view_xpu.py` | 查看数据库中的经验 |
