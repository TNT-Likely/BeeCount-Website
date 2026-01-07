import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import config
from src.utils import (
    setup_logger,
    format_error,
    truncate_text,
    validate_path,
    search_files,
    read_file_content,
    get_file_info,
)


def test_config():
    """测试配置管理"""
    print("Testing config...")
    assert config.server_name == "BeeCount MCP Server"
    assert config.server_version == "1.0.0"
    assert config.log_level == "INFO"
    print("✓ Config test passed")


def test_logger():
    """测试日志功能"""
    print("Testing logger...")
    logger = setup_logger("test_logger")
    logger.info("Test log message")
    print("✓ Logger test passed")


def test_format_error():
    """测试错误格式化"""
    print("Testing error formatting...")
    error = ValueError("Test error")
    formatted = format_error(error)
    assert "ValueError" in formatted
    assert "Test error" in formatted
    print("✓ Error formatting test passed")


def test_truncate_text():
    """测试文本截断"""
    print("Testing text truncation...")
    short_text = "Short text"
    long_text = "A" * 1000
    
    assert truncate_text(short_text, 500) == short_text
    assert len(truncate_text(long_text, 500)) == 503
    print("✓ Text truncation test passed")


def test_validate_path():
    """测试路径验证"""
    print("Testing path validation...")
    valid_path = config.project_root
    result = validate_path(str(valid_path))
    assert result == valid_path
    
    try:
        validate_path("/nonexistent/path")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        pass
    
    print("✓ Path validation test passed")


def test_search_files():
    """测试文件搜索"""
    print("Testing file search...")
    project_root = config.project_root
    
    python_files = search_files(project_root, "*.py")
    assert len(python_files) > 0
    
    md_files = search_files(project_root, "*.md")
    assert len(md_files) > 0
    
    print(f"✓ File search test passed (found {len(python_files)} Python files, {len(md_files)} Markdown files)")


def test_read_file_content():
    """测试文件读取"""
    print("Testing file reading...")
    test_file = config.project_root / "mcp" / "src" / "config.py"
    
    content = read_file_content(test_file, line_range="0~10")
    assert len(content) > 0
    assert "Settings" in content
    
    print("✓ File reading test passed")


def test_get_file_info():
    """测试文件信息获取"""
    print("Testing file info...")
    test_file = config.project_root / "mcp" / "src" / "config.py"
    
    info = get_file_info(test_file)
    assert info["name"] == "config.py"
    assert info["is_file"] == True
    assert info["size"] > 0
    
    print("✓ File info test passed")


def test_mcp_tools():
    """测试MCP工具函数"""
    print("Testing MCP tools...")
    from src.main import mcp
    
    tools = mcp._tool_manager._tools  # type: ignore
    assert len(tools) > 0
    
    tool_names = list(tools.keys())
    assert "query_document" in tool_names
    assert "list_files" in tool_names
    assert "read_file" in tool_names
    assert "get_project_info" in tool_names
    
    print(f"✓ MCP tools test passed (found {len(tools)} tools)")


def run_all_tests():
    """运行所有测试"""
    print("\n" + "="*50)
    print("Running MCP Server Basic Tests")
    print("="*50 + "\n")
    
    tests = [
        test_config,
        test_logger,
        test_format_error,
        test_truncate_text,
        test_validate_path,
        test_search_files,
        test_read_file_content,
        test_get_file_info,
        test_mcp_tools,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
