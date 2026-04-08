import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.embeddings import get_embedding_model
from src.vector_store import get_vector_store


def test_embedding_model():
    """测试嵌入模型"""
    print("Testing embedding model...")
    
    try:
        model = get_embedding_model()
        
        # 测试单个文本编码
        text = "这是一个测试文本"
        embedding = model.encode(text)
        
        assert len(embedding) > 0, "Embedding should not be empty"
        assert all(isinstance(x, float) for x in embedding), "All embedding values should be floats"
        
        print(f"PASSED: Single text encoding passed (dimension: {len(embedding)})")
        
        # 测试批量编码
        texts = ["文本1", "文本2", "文本3"]
        embeddings = model.encode_batch(texts)
        
        assert len(embeddings) == len(texts), "Batch encoding should return same number of embeddings"
        assert all(len(emb) > 0 for emb in embeddings), "All embeddings should not be empty"
        
        print(f"PASSED: Batch encoding passed (encoded {len(texts)} texts)")
        
        # 测试相似度计算
        similarity = model.compute_similarity(embedding, embedding)
        assert similarity == 1.0, "Similarity of same vector should be 1.0"
        
        print(f"PASSED: Similarity computation passed (self-similarity: {similarity})")
        
        # 测试模型信息
        model_info = model.get_model_info()
        assert model_info["is_loaded"], "Model should be loaded"
        assert model_info["dimension"] > 0, "Model dimension should be positive"
        
        print(f"PASSED: Model info passed")
        print(f"  - Model: {model_info['model_name']}")
        print(f"  - Dimension: {model_info['dimension']}")
        print(f"  - Max Seq Length: {model_info['max_seq_length']}")
        
        print("PASSED: Embedding model test passed\n")
        
    except Exception as e:
        print(f"FAILED: Embedding model test failed: {e}")
        raise


def test_vector_store():
    """测试向量存储"""
    print("Testing vector store...")
    
    try:
        vector_store = get_vector_store()
        
        # 测试获取统计信息
        zh_stats = vector_store.get_stats("zh")
        en_stats = vector_store.get_stats("en")
        
        print(f"PASSED: Get stats passed")
        print(f"  - Chinese: {zh_stats.get('total_chunks', 0)} chunks")
        print(f"  - English: {en_stats.get('total_chunks', 0)} chunks")
        
        # 测试语义搜索
        query = "如何创建预算"
        results = vector_store.search(query, top_k=3, language="zh")
        
        print(f"PASSED: Semantic search passed (found {len(results)} results)")
        
        for i, result in enumerate(results[:2], 1):
            print(f"  Result {i}:")
            print(f"    - Similarity: {result['similarity']:.3f}")
            print(f"    - File: {result['metadata'].get('file_path', 'Unknown')}")
            print(f"    - Content preview: {result['content'][:100]}...")
        
        print("PASSED: Vector store test passed\n")
        
    except Exception as e:
        print(f"FAILED: Vector store test failed: {e}")
        raise


def test_vector_store_rebuild():
    """测试向量存储重建索引"""
    print("Testing vector store rebuild...")
    
    try:
        vector_store = get_vector_store()
        
        # 测试重建中文索引（不强制）
        result = vector_store.rebuild_index(language="zh", force=False)
        
        print(f"PASSED: Rebuild index passed")
        print(f"  - Total files: {result['total_files']}")
        print(f"  - Added chunks: {result['added_chunks']}")
        print(f"  - Skipped chunks: {result['skipped_chunks']}")
        print(f"  - Total chunks: {result['total_chunks']}")
        
        assert result["success"], "Rebuild should succeed"
        
        print("PASSED: Vector store rebuild test passed\n")
        
    except Exception as e:
        print(f"FAILED: Vector store rebuild test failed: {e}")
        raise


def test_mcp_vector_tools():
    """测试MCP向量工具"""
    print("Testing MCP vector tools...")
    
    try:
        from src.main import mcp
        
        tools = mcp._tool_manager._tools  # type: ignore
        
        # 检查新工具是否存在
        new_tools = ["semantic_search", "rebuild_vector_index", "get_vector_stats"]
        
        for tool_name in new_tools:
            assert tool_name in tools, f"Tool {tool_name} should be registered"
            print(f"Tool {tool_name} registered")
        
        print(f"PASSED: MCP vector tools test passed")
        
    except Exception as e:
        print(f"FAILED: MCP vector tools test failed: {e}")
        raise


def test_integration():
    """集成测试"""
    print("Testing integration...")
    
    try:
        # 获取向量存储
        vector_store = get_vector_store()
        
        # 重建索引
        print("Rebuilding index...")
        result = vector_store.rebuild_index(language="zh", force=False)
        assert result["success"], "Rebuild should succeed"
        
        # 执行搜索
        print("Performing semantic search...")
        query = "预算管理"
        results = vector_store.search(query, top_k=5, language="zh", min_score=0.0)  # 降低阈值以测试
        
        assert len(results) > 0, "Should find at least one result"
        print(f"Found {len(results)} results for query: {query}")
        
        # 获取统计信息
        print("Getting statistics...")
        stats = vector_store.get_stats("zh")
        assert stats["total_chunks"] > 0, "Should have chunks in store"
        print(f"Total chunks: {stats['total_chunks']}")
        
        print(f"PASSED: Integration test passed\n")
        
    except Exception as e:
        print(f"FAILED: Integration test failed: {e}")
        raise


def run_all_tests():
    """运行所有向量测试"""
    print("\n" + "="*50)
    print("Running MCP Server Vector Tests")
    print("="*50 + "\n")
    
    tests = [
        test_embedding_model,
        test_vector_store,
        test_vector_store_rebuild,
        test_mcp_vector_tools,
        test_integration,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"FAILED: {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Vector Test Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
