from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

from .config import config
from .utils import logger


class EmbeddingModel:
    """文本嵌入模型封装类"""
    
    def __init__(self, model_name: Optional[str] = None):
        """
        初始化嵌入模型
        
        Args:
            model_name: 模型名称，默认从配置读取
        """
        self.model_name = model_name or config.embedding_model
        self._model: Optional[SentenceTransformer] = None
        self._load_model()
    
    def _load_model(self):
        """加载嵌入模型"""
        try:
            logger.info(f"Loading embedding model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    def encode(self, text: str) -> List[float]:
        """
        将文本编码为向量
        
        Args:
            text: 输入文本
        
        Returns:
            文本向量（浮点数列表）
        """
        try:
            if self._model is None:
                logger.error("Model not loaded")
                raise RuntimeError("Embedding model not loaded")
            
            if not text or not text.strip():
                logger.warning("Empty text provided for encoding")
                return [0.0] * self._model.get_sentence_embedding_dimension()  # type: ignore
            
            embedding = self._model.encode(text, convert_to_numpy=True)  # type: ignore
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error encoding text: {e}")
            raise
    
    def encode_batch(self, texts: List[str]) -> List[List[float]]:
        """
        批量编码文本为向量
        
        Args:
            texts: 输入文本列表
        
        Returns:
            文本向量列表
        """
        try:
            if not texts:
                logger.warning("Empty text list provided for batch encoding")
                return []
            
            if self._model is None:
                logger.error("Model not loaded")
                return []
            
            # 过滤空文本
            valid_texts = [t for t in texts if t and t.strip()]
            if not valid_texts:
                return []
            
            embeddings = self._model.encode(valid_texts, convert_to_numpy=True)  # type: ignore
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error encoding batch texts: {e}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            模型信息字典
        """
        try:
            if self._model is None:
                return {
                    "model_name": self.model_name,
                    "dimension": 0,
                    "max_seq_length": 0,
                    "is_loaded": False
                }
            
            return {
                "model_name": self.model_name,
                "dimension": self._model.get_sentence_embedding_dimension(),
                "max_seq_length": self._model.max_seq_length,
                "is_loaded": True
            }
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {
                "model_name": self.model_name,
                "dimension": 0,
                "max_seq_length": 0,
                "is_loaded": False,
                "error": str(e)
            }
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        计算两个向量的余弦相似度
        
        Args:
            embedding1: 第一个向量
            embedding2: 第二个向量
        
        Returns:
            相似度分数（0-1之间）
        """
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # 计算余弦相似度
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            return float(similarity)
        except Exception as e:
            logger.error(f"Error computing similarity: {e}")
            return 0.0


# 全局单例实例
_embedding_model: Optional[EmbeddingModel] = None


def get_embedding_model() -> EmbeddingModel:
    """
    获取全局嵌入模型实例（单例模式）
    
    Returns:
        嵌入模型实例
    """
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = EmbeddingModel()
    return _embedding_model
