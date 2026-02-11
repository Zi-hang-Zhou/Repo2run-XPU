"""
XPU 经验知识库 - 对外接口定义
只需要关注这个文件即可。
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple



# 数据结构定义


@dataclass
class XpuHint:
    """单条经验提示"""
    id: str                          # 经验 ID
    similarity: float                # 相似度 (0-1)
    advice: List[str]                # 建议列表（自然语言）
    context: Dict = field(default_factory=dict)   # 上下文信息


@dataclass
class XpuRetrievalResult:
    """检索结果"""
    prompt_block: str                # 可直接注入到 LLM prompt 的文本块
    hints: List[XpuHint]             # 检索到的经验列表

    @property
    def ids(self) -> List[str]:
        """返回所有经验的 ID 列表"""
        return [h.id for h in self.hints]

    @property
    def has_hints(self) -> bool:
        """是否检索到了经验"""
        return len(self.hints) > 0



# 接口定义（抽象类）


class IXpuRetriever(ABC):
    """
    XPU 检索器接口

    只需要实现这个接口，或者直接使用 XpuHandler 类
    """

    @abstractmethod
    def retrieve(self, error_log: str) -> XpuRetrievalResult:
        """
        根据错误日志检索相关经验

        Args:
            error_log: sandbox 输出的错误日志

        Returns:
            XpuRetrievalResult 对象，包含：
            - prompt_block: 直接加到 LLM prompt 的文本
            - hints: 检索到的经验列表
        """
        pass

    @abstractmethod
    def feedback(self, hint_ids: List[str], is_helpful: bool):
        """
        反馈某些经验是否有帮助（用于优化检索质量）

        Args:
            hint_ids: 之前检索到的经验 ID 列表
            is_helpful: 这些经验是否帮助解决了问题
        """
        pass

    @abstractmethod
    def close(self):
        """关闭连接，释放资源"""
        pass



# 配置类

@dataclass
class XpuConfig:
    """XPU 配置"""
    # 数据库连接
    database_url: Optional[str] = None  # 如果为 None，从环境变量读取

    # 检索参数
    total_k: int = 12                   # 总共检索多少条经验（用于分批暴露）
    expose_k: int = 3                   # 每次暴露给 Agent 的经验数量
    min_similarity: float = 0.3         # 最小相似度阈值
    max_log_length: int = 4000          # 日志最大长度（超出会截断）

    # 错误记忆参数（用于分批暴露逻辑）
    error_similarity_threshold: float = 0.9  # 判断"相同错误"的相似度阈值

    # 兼容旧配置
    @property
    def top_k(self) -> int:
        """兼容旧接口，返回 expose_k"""
        return self.expose_k

    # 错误检测关键词
    error_keywords: List[str] = field(default_factory=lambda: [
        "module not found",
        "modulenotfounderror",
        "importerror",
        "no module named",
        "could not find a version",
        "command not found",
        "permission denied",
        "error:",
        "failed",
        "traceback",
        "exception",
    ])



# 使用示例

"""
# 方式 1: 直接使用 XpuHandler（推荐）
from xpu_handler_v2 import XpuHandler

handler = XpuHandler()
result = handler.retrieve(sandbox_output)

if result.has_hints:
    # 注入到 prompt
    prompt += result.prompt_block

    # 记录使用了哪些经验
    used_ids = result.ids

# 任务完成后反馈
handler.feedback(used_ids, is_helpful=True)
handler.close()


# 方式 2: 使用配置
from xpu_handler_v2 import XpuHandler
from xpu_interface import XpuConfig

config = XpuConfig(
    top_k=5,
    min_similarity=0.4,
)
handler = XpuHandler(config=config)
"""
