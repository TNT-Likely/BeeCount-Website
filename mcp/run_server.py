import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.main import mcp
from src.vector_store import get_vector_store
from src.utils import logger


def rebuild_index(language: str = "zh", force: bool = False):
    """重建向量索引"""
    try:
        logger.info(f"Rebuilding vector index for language: {language}, force: {force}")
        vector_store = get_vector_store()
        
        if language.lower() == "all":
            result = vector_store.rebuild_all_indexes(force=force)
            
            if result["success"]:
                print(f"\n✓ 所有语言向量索引重建成功")
                print(f"  语言: {', '.join(result['languages'])}")
                print(f"  处理文件数: {result['total_files']}")
                print(f"  添加块数: {result['added_chunks']}")
                print(f"  跳过块数: {result['skipped_chunks']}")
                print(f"  总块数: {result['total_chunks']}")
                
                print(f"\n详细统计:")
                for lang, detail in result["details"].items():
                    print(f"\n  {lang.upper()}:")
                    print(f"    文件数: {detail['total_files']}")
                    print(f"    添加块数: {detail['added_chunks']}")
                    print(f"    跳过块数: {detail['skipped_chunks']}")
                    print(f"    总块数: {detail['total_chunks']}")
                    print(f"    集合名称: {detail['collection_name']}")
            else:
                print(f"\n✗ 向量索引重建失败: {result.get('error', 'Unknown error')}")
                sys.exit(1)
        else:
            result = vector_store.rebuild_index(language=language, force=force)
            
            if result["success"]:
                print(f"\n✓ 向量索引重建成功")
                print(f"  语言: {result['language']}")
                print(f"  处理文件数: {result['total_files']}")
                print(f"  添加块数: {result['added_chunks']}")
                print(f"  跳过块数: {result['skipped_chunks']}")
                print(f"  总块数: {result['total_chunks']}")
                print(f"  集合名称: {result['collection_name']}")
            else:
                print(f"\n✗ 向量索引重建失败: {result.get('error', 'Unknown error')}")
                sys.exit(1)
    except Exception as e:
        logger.error(f"Error rebuilding index: {e}")
        print(f"\n✗ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BeeCount MCP Server")
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="重建向量索引（首次部署或文档更新后使用）"
    )
    parser.add_argument(
        "--language",
        default="zh",
        choices=["zh", "en", "ALL"],
        help="文档语言（zh: 中文, en: 英文, ALL: 所有语言）"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制重建索引（删除现有数据后重新生成）"
    )
    
    args = parser.parse_args()
    
    if args.rebuild_index:
        rebuild_index(language=args.language, force=args.force)
    else:
        try:
            mcp.run()
        except KeyboardInterrupt:
            try:
                print("\nServer shutdown requested by user")
            except (ValueError, OSError):
                pass
        except Exception as e:
            try:
                print(f"Error: {e}")
            except (ValueError, OSError):
                pass
            sys.exit(1)
