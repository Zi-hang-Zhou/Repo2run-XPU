"""
XPU Handler v2 - 优化后的经验知识库接口

使用方法:
    from xpu_handler_v2 import XpuHandler

    handler = XpuHandler()
    result = handler.retrieve(error_log)

    if result.has_hints:
        prompt += result.prompt_block
"""

import os
import logging
import hashlib
import numpy as np
from typing import List, Optional, Dict, Any, Tuple
from dataclasses import dataclass, field

from xpu_interface import (
    IXpuRetriever,
    XpuConfig,
    XpuHint,
    XpuRetrievalResult,
)

# 导入 XPU 核心模块（相对导入，适配 standalone 结构）
try:
    from xpu.xpu_adapter import (
        XpuAtom,
        XpuContext,
        XpuEntry,
        render_candidates_block,
    )
    from xpu.xpu_vector_store import XpuVectorStore, text_to_embedding
except ImportError as e:
    logging.error(f"[XPU] Import Error: {e}")
    XpuVectorStore = None
    text_to_embedding = None

logger = logging.getLogger(__name__)


# 错误记忆条目数据结构
@dataclass
class ErrorMemoryEntry:
    """记录已遇到的错误及其候选经验"""
    error_hash: str                          # 错误日志的 MD5 哈希（用于快速完全匹配）
    error_embedding: List[float]             # 错误日志的 embedding（用于相似度匹配）
    all_candidates: List[Dict[str, Any]]     # top-N 的所有候选经验（原始结果）
    exposed_batch: int = 0                   # 已经暴露过的批次数（0, 1, 2, ...）

    def get_next_batch(self, batch_size: int = 3) -> Tuple[List[Dict[str, Any]], bool]:
        """
        获取下一批候选经验

        Returns:
            (candidates, has_more) - 候选列表和是否还有更多批次
        """
        start_idx = self.exposed_batch * batch_size
        end_idx = start_idx + batch_size

        if start_idx >= len(self.all_candidates):
            # 所有经验都已用完
            return [], False

        batch = self.all_candidates[start_idx:end_idx]
        has_more = end_idx < len(self.all_candidates)

        return batch, has_more


class XpuHandler(IXpuRetriever):
    """
    XPU 经验知识库处理器

    这是对外暴露的主要接口类。
    """

    def __init__(self, config: Optional[XpuConfig] = None, max_error_memory: int = 20):
        """
        初始化 XPU Handler

        Args:
            config: XPU 配置，如果为 None 则使用默认配置
            max_error_memory: 最大记忆的错误数量（防止内存过大）
        """
        self.config = config or XpuConfig()
        self.vector_store: Optional[XpuVectorStore] = None
        self._last_query: Optional[str] = None
        self._session_ids: set = set()

        # [新增] 错误记忆管理
        self.max_error_memory = max_error_memory
        self._error_memory_by_hash: Dict[str, ErrorMemoryEntry] = {}  # 按哈希索引（快速完全匹配）
        self._error_memory_list: List[ErrorMemoryEntry] = []  # 按时间顺序存储（用于相似度搜索和 FIFO）

        self._init_vector_store()

    def _init_vector_store(self):
        """初始化向量数据库连接"""
        if XpuVectorStore is None:
            logger.warning("[XPU] XpuVectorStore not available")
            return

        # 获取数据库连接字符串
        dns = self.config.database_url
        if not dns:
            dns = os.environ.get("dns") or os.environ.get("DATABASE_URL")

        if not dns:
            logger.error("[XPU] Missing database connection string. "
                        "Set 'dns' environment variable or pass in XpuConfig.")
            return

        try:
            self.vector_store = XpuVectorStore(connection_string=dns)
            logger.info("[XPU] Vector store initialized successfully")
        except Exception as e:
            logger.error(f"[XPU] Failed to initialize vector store: {e}")
            self.vector_store = None

    def _has_error_keywords(self, text: str) -> bool:
        """检查文本中是否包含错误关键词"""
        if not text:
            return False
        lowered = text.lower()
        return any(kw in lowered for kw in self.config.error_keywords)

    def _truncate_log(self, log: str) -> str:
        """截断过长的日志"""
        max_len = self.config.max_log_length
        if len(log) <= max_len:
            return log
        half = max_len // 2
        return log[:half] + "\n... [TRUNCATED] ...\n" + log[-half:]

    def _compute_error_hash(self, log_snippet: str) -> str:
        """计算错误日志的 MD5 哈希"""
        return hashlib.md5(log_snippet.encode('utf-8')).hexdigest()

    def _compute_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """计算两个向量的余弦相似度"""
        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def _find_similar_error(self, error_hash: str, error_embedding: List[float]) -> Optional[ErrorMemoryEntry]:
        """
        查找相似的错误（两级过滤）

        Args:
            error_hash: 当前错误的哈希
            error_embedding: 当前错误的 embedding

        Returns:
            如果找到相似错误，返回对应的 ErrorMemoryEntry；否则返回 None
        """
        # 第一级：哈希完全匹配（O(1)）
        if error_hash in self._error_memory_by_hash:
            logger.info(f"[XPU] Found exact match by hash")
            return self._error_memory_by_hash[error_hash]

        # 第二级：embedding 相似度匹配（O(n)）
        for memory_entry in self._error_memory_list:
            similarity = self._compute_cosine_similarity(error_embedding, memory_entry.error_embedding)
            if similarity >= self.config.error_similarity_threshold:
                logger.info(f"[XPU] Found similar error by embedding (similarity={similarity:.3f})")
                return memory_entry

        return None

    def _add_error_memory(self, error_hash: str, error_embedding: List[float], candidates: List[Dict[str, Any]]):
        """
        添加新错误到记忆中（FIFO策略）

        Args:
            error_hash: 错误哈希
            error_embedding: 错误 embedding
            candidates: 检索到的所有候选经验
        """
        # 检查是否达到容量上限
        if len(self._error_memory_list) >= self.max_error_memory:
            # 删除最老的记录（FIFO）
            oldest = self._error_memory_list.pop(0)
            if oldest.error_hash in self._error_memory_by_hash:
                del self._error_memory_by_hash[oldest.error_hash]
            logger.info(f"[XPU] Removed oldest error from memory (FIFO), capacity={self.max_error_memory}")

        # 创建新的记忆条目
        memory_entry = ErrorMemoryEntry(
            error_hash=error_hash,
            error_embedding=error_embedding,
            all_candidates=candidates,
            exposed_batch=0  # 初始化为 0，表示还未暴露任何批次
        )

        # 添加到两个数据结构
        self._error_memory_by_hash[error_hash] = memory_entry
        self._error_memory_list.append(memory_entry)

        logger.info(f"[XPU] Added new error to memory (total={len(self._error_memory_list)})")

    def retrieve(self, error_log: str) -> XpuRetrievalResult:
        """
        检索相关经验 - 支持分批暴露

        Args:
            error_log: 错误日志文本

        Returns:
            XpuRetrievalResult 对象
        """
        empty_result = XpuRetrievalResult(prompt_block="", hints=[])

        # 1. 预检查
        if not self.vector_store:
            return empty_result

        log_snippet = self._truncate_log(error_log.strip())

        if not log_snippet:
            return empty_result

        # 2. 检查是否有错误关键词
        if not self._has_error_keywords(log_snippet):
            return empty_result

        # 3. 去重：跳过相同的查询（连续重复）
        if self._last_query == log_snippet:
            return empty_result

        # 4. 计算错误的哈希和 embedding
        try:
            error_hash = self._compute_error_hash(log_snippet)
            error_embedding = text_to_embedding(log_snippet)

            # 5. 查找是否是已知的相似错误
            memory_entry = self._find_similar_error(error_hash, error_embedding)

            if memory_entry is not None:
                # 已知错误，返回下一批经验
                next_batch, has_more = memory_entry.get_next_batch(self.config.expose_k)

                if not next_batch:
                    logger.info(f"[XPU] All {len(memory_entry.all_candidates)} experiences exhausted for this error")
                    return empty_result

                # 增加已暴露批次计数
                memory_entry.exposed_batch += 1
                batch_num = memory_entry.exposed_batch

                logger.info(
                    f"[XPU] Returning batch #{batch_num} (items {(batch_num-1)*self.config.expose_k + 1}-{batch_num*self.config.expose_k}), "
                    f"has_more={has_more}"
                )

                results = next_batch

            else:
                # 新错误，执行完整检索（top-N）
                ctx = XpuContext(lang="python")

                results = self.vector_store.search(
                    query_embedding=error_embedding,
                    ctx=ctx,
                    k=self.config.total_k,  # 检索 total_k 条
                    min_similarity=self.config.min_similarity,
                )

                if not results:
                    logger.info("[XPU] No similar entries found")
                    return empty_result

                logger.info(f"[XPU] New error detected, retrieved {len(results)} candidates (total_k={self.config.total_k})")

                # 保存到错误记忆
                self._add_error_memory(error_hash, error_embedding, results)

                # 只返回前 expose_k 条
                results = results[:self.config.expose_k]
                logger.info(f"[XPU] Exposing first batch (items 1-{self.config.expose_k})")

            # 6. 转换结果
            hints: List[XpuHint] = []
            entries: List[XpuEntry] = []

            for result in results:
                hint = XpuHint(
                    id=result["id"],
                    similarity=result.get("similarity", 0.0),
                    advice=result.get("advice_nl", []),
                    context=result.get("context", {}),
                )
                hints.append(hint)

                # 转换为 XpuEntry 用于渲染
                atoms_data = result.get("atoms", [])
                atoms = [XpuAtom(name=a["name"], args=a["args"]) for a in atoms_data]
                entry = XpuEntry(
                    id=result["id"],
                    context=result.get("context", {}),
                    signals=result.get("signals", {}),
                    advice_nl=result.get("advice_nl", []),
                    atoms=atoms,
                )
                entries.append(entry)

            # 7. 更新状态
            self._last_query = log_snippet
            hint_ids = [h.id for h in hints]
            self._session_ids.update(hint_ids)

            # 8. 记录命中
            if self.vector_store:
                self.vector_store.increment_telemetry(hint_ids, 'hits')

            logger.info(f"[XPU] Retrieved {len(hints)} hints: {hint_ids}")

            # 9. 渲染 prompt block
            prompt_block = render_candidates_block(entries)

            return XpuRetrievalResult(
                prompt_block=prompt_block,
                hints=hints,
            )

        except Exception as e:
            logger.error(f"[XPU] Retrieval error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return empty_result

    def feedback(self, hint_ids: List[str], is_helpful: bool):
        """
        反馈经验是否有帮助

        Args:
            hint_ids: 经验 ID 列表
            is_helpful: 是否有帮助
        """
        if not self.vector_store or not hint_ids:
            return

        metric = 'successes' if is_helpful else 'failures'
        self.vector_store.increment_telemetry(hint_ids, metric)
        logger.info(f"[XPU] Feedback: {len(hint_ids)} entries marked as {metric}")

    def close(self):
        """关闭连接"""
        if self.vector_store:
            self.vector_store.close()
            self.vector_store = None
        self._session_ids.clear()

    # ============================================================
    # 兼容旧接口（可选，方便迁移）
    # ============================================================

    def retrieve_hints(self, sandbox_res: str):
        """
        兼容旧接口

        Returns:
            Tuple[str, List[str], List[Dict]]
        """
        result = self.retrieve(sandbox_res)
        candidates_info = [
            {"id": h.id, "similarity": h.similarity}
            for h in result.hints
        ]
        return result.prompt_block, result.ids, candidates_info

    def finalize_session(self, is_task_success: bool):
        """兼容旧接口"""
        self._session_ids.clear()

    def _check_has_error(self, text: str) -> bool:
        """检查文本是否包含错误关键词（与 xpu_handler.py 接口保持一致）"""
        return self._has_error_keywords(text)

    # 注意：部署后经验提取已由 online_xpu_extractor.online_extract_and_store() 统一处理，
    # 通过 main.py --online_xpu 参数启用。此处不重复实现。
