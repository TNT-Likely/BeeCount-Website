from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

import chromadb
from chromadb.config import Settings

from .config import config
from .embeddings import get_embedding_model
from .utils import logger, read_file_content


class VectorStore:
    """向量存储管理类，基于ChromaDB"""
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        初始化向量存储
        
        Args:
            persist_directory: 持久化存储目录，默认从配置读取
        """
        self.persist_directory = persist_directory or str(config.vector_db_path)
        self._client: Any = None
        self._collections: Dict[str, Any] = {}
        self._embedding_model = get_embedding_model()
        self._initialize_client()
    
    def _initialize_client(self):
        """初始化ChromaDB客户端"""
        try:
            logger.info(f"Initializing ChromaDB client at: {self.persist_directory}")
            
            # 创建持久化目录
            persist_path = Path(self.persist_directory)
            persist_path.mkdir(parents=True, exist_ok=True)
            
            # 初始化ChromaDB客户端
            self._client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            logger.info("ChromaDB client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB client: {e}")
            raise
    
    def _get_collection(self, language: str = "zh"):
        """
        获取指定语言的集合
        
        Args:
            language: 语言代码（zh/en）
        
        Returns:
            ChromaDB集合对象
        """
        try:
            if self._client is None:
                raise RuntimeError("ChromaDB client not initialized")
            
            collection_name = f"docs_{language}"
            
            if collection_name not in self._collections:
                # 获取或创建集合，使用余弦距离
                self._collections[collection_name] = self._client.get_or_create_collection(
                    name=collection_name,
                    metadata={"language": language, "hnsw:space": "cosine"}  # 使用余弦距离
                )
            
            return self._collections[collection_name]
        except Exception as e:
            logger.error(f"Failed to get collection for language {language}: {e}")
            raise
    
    def _chunk_text(self, text: str, chunk_size: Optional[int] = None, chunk_overlap: Optional[int] = None) -> List[str]:
        """
        将文本分割为多个块
        
        Args:
            text: 输入文本
            chunk_size: 块大小，默认从配置读取
            chunk_overlap: 块重叠大小，默认从配置读取
        
        Returns:
            文本块列表
        """
        try:
            chunk_size = chunk_size or config.chunk_size
            chunk_overlap = chunk_overlap or config.chunk_overlap
            
            # 如果文本很短，直接返回
            if len(text) <= chunk_size:
                return [text]
            
            chunks: List[str] = []
            start = 0
            
            while start < len(text):
                end = start + chunk_size
                
                # 尝试在段落或句子边界分割
                if end < len(text):
                    # 查找最近的换行符
                    newline_pos = text.rfind('\n', start, end)
                    if newline_pos > start + chunk_size // 2:
                        end = newline_pos + 1
                    else:
                        # 查找最近的句号
                        period_pos = text.rfind('。', start, end)
                        if period_pos > start + chunk_size // 2:
                            end = period_pos + 1
                        else:
                            # 查找最近的英文句号
                            period_pos = text.rfind('.', start, end)
                            if period_pos > start + chunk_size // 2:
                                end = period_pos + 1
                
                chunk = text[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                
                start = end - chunk_overlap
                if start < 0:
                    start = 0
            
            return chunks
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return [text]
    
    def _extract_metadata(self, file_path: Path, chunk_index: int, language: str) -> Dict[str, Any]:
        """
        提取文档元数据
        
        Args:
            file_path: 文件路径
            chunk_index: 块索引
            language: 语言代码
        
        Returns:
            元数据字典
        """
        try:
            # 相对于项目根目录的路径
            relative_path = file_path.relative_to(config.project_root)
            
            # 提取文档标题（从文件名或内容）
            title = file_path.stem.replace('-', ' ').replace('_', ' ').title()
            
            # 提取分类（从目录结构）
            parts = relative_path.parts
            category = parts[0] if len(parts) > 1 else "root"
            
            # 生成在线查看URL
            doc_relative_path = file_path.relative_to(config.get_language_root(language))
            url = config.get_document_url(str(doc_relative_path), language)
            
            return {
                "file_path": str(relative_path),
                "language": language,
                "chunk_index": chunk_index,
                "title": title,
                "category": category,
                "url": url,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {
                "file_path": str(file_path),
                "language": language,
                "chunk_index": chunk_index,
                "title": "Unknown",
                "category": "unknown",
                "url": "",
                "timestamp": datetime.now().isoformat()
            }
    
    def add_document(self, file_path: Path, language: str = "zh", force: bool = False) -> int:
        """
        添加文档到向量存储
        
        Args:
            file_path: 文档路径
            language: 语言代码
            force: 是否强制重新添加
        
        Returns:
            添加的文档块数量
        """
        try:
            logger.info(f"Adding document: {file_path}, language: {language}")
            
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                return 0
            
            # 读取文件内容
            content = read_file_content(file_path, line_range="all")
            if not content or not content.strip():
                logger.warning(f"Empty content in file: {file_path}")
                return 0
            
            # 分割文本为块
            chunks = self._chunk_text(content)
            logger.info(f"Document split into {len(chunks)} chunks")
            
            # 获取集合
            collection = self._get_collection(language)
            
            # 为每个块生成ID和嵌入向量
            doc_id_prefix = str(file_path.relative_to(config.project_root)).replace('\\', '_').replace('/', '_')
            
            ids = []
            embeddings = []
            metadatas = []
            documents = []
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id_prefix}_chunk_{i}"
                
                # 检查是否已存在
                if not force:
                    existing = collection.get(ids=[chunk_id])
                    if existing['ids']:
                        logger.debug(f"Chunk {chunk_id} already exists, skipping")
                        continue
                
                # 生成嵌入向量
                embedding = self._embedding_model.encode(chunk)
                
                # 提取元数据
                metadata = self._extract_metadata(file_path, i, language)
                
                ids.append(chunk_id)  # type: ignore
                embeddings.append(embedding)  # type: ignore
                metadatas.append(metadata)  # type: ignore
                documents.append(chunk)  # type: ignore
            
            if ids:
                # 批量添加到集合
                collection.add(
                    ids=ids,
                    embeddings=embeddings,
                    metadatas=metadatas,
                    documents=documents
                )
                logger.info(f"Added {len(ids)} chunks to vector store")  # type: ignore
                return len(ids)  # type: ignore
            else:
                logger.info("No new chunks to add")
                return 0
            
        except Exception as e:
            logger.error(f"Error adding document {file_path}: {e}")
            return 0
    
    def search(self, query: str, top_k: int = 5, language: str = "zh", min_score: Optional[float] = None) -> List[Dict[str, Any]]:
        """
        语义搜索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            language: 语言代码
            min_score: 最小相似度分数，默认从配置读取
        
        Returns:
            搜索结果列表
        """
        try:
            logger.info(f"Searching for: {query}, language: {language}, top_k: {top_k}")
            
            min_score = min_score or config.min_similarity_score
            
            # 生成查询向量
            query_embedding = self._embedding_model.encode(query)
            
            # 获取集合
            collection = self._get_collection(language)
            
            # 执行搜索
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # 格式化结果
            formatted_results: List[Dict[str, Any]] = []
            if results.get('ids') and results['ids'][0]:
                for i, doc_id in enumerate(results['ids'][0]):
                    distance = results['distances'][0][i]
                    similarity = 1 - distance  # 转换为相似度分数
                    
                    # 过滤低相似度结果
                    if similarity < min_score:
                        continue
                    
                    formatted_results.append({
                        "id": doc_id,
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "similarity": similarity,
                        "distance": distance
                    })
            
            logger.info(f"Found {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def delete_document(self, file_path: Path, language: str = "zh") -> int:
        """
        删除文档的所有块
        
        Args:
            file_path: 文档路径
            language: 语言代码
        
        Returns:
            删除的块数量
        """
        try:
            logger.info(f"Deleting document: {file_path}, language: {language}")
            
            collection = self._get_collection(language)
            
            # 生成ID前缀
            doc_id_prefix = str(file_path.relative_to(config.project_root)).replace('\\', '_').replace('/', '_')
            
            # 获取所有文档
            all_docs = collection.get()
            
            # 查找匹配的文档块
            ids_to_delete = [doc_id for doc_id in all_docs['ids'] if doc_id.startswith(doc_id_prefix)]
            
            if ids_to_delete:
                collection.delete(ids=ids_to_delete)
                logger.info(f"Deleted {len(ids_to_delete)} chunks")
                return len(ids_to_delete)
            else:
                logger.info("No chunks found to delete")
                return 0
            
        except Exception as e:
            logger.error(f"Error deleting document {file_path}: {e}")
            return 0
    
    def rebuild_index(self, language: str = "zh", force: bool = False) -> Dict[str, Any]:
        """
        重建索引
        
        Args:
            language: 语言代码
            force: 是否强制重建
        
        Returns:
            重建结果统计
        """
        try:
            logger.info(f"Rebuilding index for language: {language}, force: {force}")
            
            # 获取文档根目录
            docs_root = config.get_language_root(language)
            
            if not docs_root.exists():
                logger.warning(f"Docs directory not found: {docs_root}")
                return {
                    "success": False,
                    "error": f"Directory not found: {docs_root}",
                    "total_files": 0,
                    "added_chunks": 0,
                    "skipped_chunks": 0
                }
            
            # 查找所有markdown文件
            from .utils import search_files
            md_files = search_files(docs_root, "*.md")
            
            logger.info(f"Found {len(md_files)} markdown files")
            
            # 如果强制重建，先删除现有集合
            if force:
                collection_name = f"docs_{language}"
                try:
                    if self._client is not None:
                        self._client.delete_collection(name=collection_name)
                    self._collections.pop(collection_name, None)
                    logger.info(f"Deleted existing collection: {collection_name}")
                except Exception as e:
                    logger.warning(f"Failed to delete collection: {e}")
            
            # 添加所有文档
            total_added = 0
            total_skipped = 0
            
            for file_path in md_files:
                added = self.add_document(file_path, language, force=force)
                total_added += added
                total_skipped += 0 if force else 1
            
            stats = self.get_stats(language)
            
            return {
                "success": True,
                "language": language,
                "total_files": len(md_files),
                "added_chunks": total_added,
                "skipped_chunks": total_skipped,
                "total_chunks": stats.get("total_chunks", 0),
                "collection_name": f"docs_{language}"
            }
            
        except Exception as e:
            logger.error(f"Error rebuilding index: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_files": 0,
                "added_chunks": 0,
                "skipped_chunks": 0
            }
    
    def rebuild_all_indexes(self, force: bool = False) -> Dict[str, Any]:
        """
        重建所有语言的索引
        
        Args:
            force: 是否强制重建
        
        Returns:
            重建结果统计（包含所有语言）
        """
        try:
            logger.info(f"Rebuilding all indexes, force: {force}")
            
            languages = ["zh", "en"]
            results: Dict[str, Dict[str, Any]] = {}
            
            for language in languages:
                result = self.rebuild_index(language=language, force=force)
                results[language] = result
            
            # 汇总统计
            total_files = sum(r.get("total_files", 0) for r in results.values())
            total_added = sum(r.get("added_chunks", 0) for r in results.values())
            total_skipped = sum(r.get("skipped_chunks", 0) for r in results.values())
            total_chunks = sum(r.get("total_chunks", 0) for r in results.values())
            
            success = all(r.get("success", False) for r in results.values())
            
            return {
                "success": success,
                "languages": languages,
                "total_files": total_files,
                "added_chunks": total_added,
                "skipped_chunks": total_skipped,
                "total_chunks": total_chunks,
                "details": results
            }
            
        except Exception as e:
            logger.error(f"Error rebuilding all indexes: {e}")
            return {
                "success": False,
                "error": str(e),
                "total_files": 0,
                "added_chunks": 0,
                "skipped_chunks": 0
            }
    
    def get_stats(self, language: str = "zh") -> Dict[str, Any]:
        """
        获取向量存储统计信息
        
        Args:
            language: 语言代码
        
        Returns:
            统计信息字典
        """
        try:
            collection = self._get_collection(language)
            
            # 获取集合统计
            count = collection.count()
            
            # 获取所有文档以计算更多统计信息
            all_docs = collection.get()
            
            # 按分类统计
            categories = {}
            for metadata in all_docs['metadatas']:
                category = metadata.get('category', 'unknown')  # type: ignore
                categories[category] = categories.get(category, 0) + 1  # type: ignore
            
            # 获取模型信息
            model_info = self._embedding_model.get_model_info()
            
            return {
                "language": language,
                "collection_name": f"docs_{language}",
                "total_chunks": count,
                "total_documents": len(set(doc_id.rsplit('_chunk_', 1)[0] for doc_id in all_docs['ids'])),
                "categories": categories,
                "model": model_info,
                "persist_directory": self.persist_directory
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "error": str(e),
                "language": language
            }


# 全局单例实例
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """
    获取全局向量存储实例（单例模式）
    
    Returns:
        向量存储实例
    """
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store
