from typing import List
from pathlib import Path

from fastmcp import FastMCP

from .config import config
from .utils import logger, search_files, read_file_content, get_file_info


mcp = FastMCP(config.server_name)


@mcp.tool()
def query_document(query: str, max_results: int = 5, language: str = "zh") -> str:
    """
    在项目文档中搜索内容
    
    Args:
        query: 搜索查询字符串
        max_results: 返回的最大结果数
        language: 语言选择，"zh"表示中文文档，"en"表示英文文档
    
    Returns:
        匹配的文档内容摘要
    """
    try:
        logger.info(f"Querying documents with: {query}, language: {language}")
        
        search_dirs = [config.get_language_root(language)]
        
        results: List[str] = []
        for search_dir in search_dirs:
            if not search_dir.exists():
                logger.warning(f"Directory not found: {search_dir}")
                continue
            
            files = search_files(search_dir, "*.md")
            
            for file_path in files:
                try:
                    content = read_file_content(file_path, line_range="0~50")
                    if query.lower() in content.lower():
                        relative_path = file_path.relative_to(config.project_root)
                        doc_relative_path = file_path.relative_to(search_dir)
                        doc_url = config.get_document_url(str(doc_relative_path), language)
                        results.append(f"\n--- {relative_path} ---\n在线查看: {doc_url}\n\n{content}")
                        if len(results) >= max_results:
                            break
                except Exception as e:
                    logger.warning(f"Failed to read {file_path}: {e}")
            if len(results) >= max_results:
                break
        
        if not results:
            return f"No documents found matching query: {query}"
        
        return f"Found {len(results)} documents:\n" + "\n".join(results)
    except Exception as e:
        logger.error(f"Error in query_document: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def list_files(directory: str = ".", language: str = "zh") -> str:
    """
    列出指定目录中的md文档文件
    
    Args:
        directory: 目录路径（相对于语言根目录），默认当前目录
        language: 语言选择，"zh"表示中文文档，"en"表示英文文档
    
    Returns:
        文件列表信息
    """
    try:
        logger.info(f"Listing md files in {directory}, language: {language}")
        
        base_dir = config.get_language_root(language) / directory
        
        if not base_dir.exists():
            return f"Directory not found: {directory}"
        
        # 只搜索md文件，不搜索其他类型
        files = search_files(base_dir, "*.md")
        
        if not files:
            return f"No md files found in {directory}"
        
        result = f"Found {len(files)} md files in {directory}:\n"
        for file_path in files[:50]:
            info = get_file_info(file_path)
            # 相对于语言根目录的路径，不包含docs或i18n前缀
            relative_path = file_path.relative_to(base_dir)
            doc_url = config.get_document_url(str(relative_path), language)
            result += f"- {relative_path} ({info['size']} bytes)\n  在线查看: {doc_url}\n"
        
        if len(files) > 50:
            result += f"\n... and {len(files) - 50} more files"
        
        return result
    except Exception as e:
        logger.error(f"Error in list_files: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def read_file(file_path: str, line_range: str = "0~100", language: str = "zh") -> str:
    """
    读取文件内容
    
    Args:
        file_path: 文件路径（相对于docs或i18n根目录）
        line_range: 行范围，支持以下格式：
            - "0~100": 读取第1-100行（默认）
            - "101~200": 读取第101-200行
            - "all": 读取整个文件
            - "50": 读取前50行（等同于"0~50"）
        language: 语言选择，"zh"表示中文文档，"en"表示英文文档
    
    Returns:
        文件内容（包含在线查看链接）
    """
    try:
        if not file_path or not file_path.strip():
            return "Error: file_path cannot be empty"
        
        logger.info(f"Reading file: {file_path}, line_range: {line_range}, language: {language}")
        
        full_path = config.get_language_root(language) / file_path
        
        if not full_path.exists():
            return f"Error: File not found: {file_path}"
        
        if not full_path.is_file():
            return f"Error: Path is not a file: {file_path}"
        
        content = read_file_content(full_path, line_range)
        relative_path = full_path.relative_to(config.project_root)
        doc_url = config.get_document_url(file_path, language)
        
        return f"""Content of {relative_path}:
在线查看: {doc_url}

{content}"""
    except Exception as e:
        logger.error(f"Error in read_file: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def list_media_files(directory: str = ".", media_type: str = "image", language: str = "zh") -> str:
    """
    列出指定目录中的媒体文件（图片/视频）并获取基本信息
    
    Args:
        directory: 目录路径（相对于static目录），默认当前目录
        media_type: 媒体类型，"image"表示图片文件，"video"表示视频文件，"all"表示所有媒体文件
        language: 语言选择，"zh"表示中文文档，"en"表示英文文档
    
    Returns:
        媒体文件列表及基本信息
    """
    try:
        logger.info(f"Listing {media_type} files in {directory}, language: {language}")
        
        # 静态资源根目录
        base_dir = config.project_root / "static" / directory
        
        if not base_dir.exists():
            return f"Directory not found: {directory}"
        
        # 定义媒体文件扩展名
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
        video_extensions = [".mp4", ".avi", ".mov", ".wmv", ".flv", ".webm"]
        
        # 根据media_type选择要搜索的扩展名
        if media_type == "image":
            extensions = image_extensions
            patterns = [f"*{ext}" for ext in image_extensions]
        elif media_type == "video":
            extensions = video_extensions
            patterns = [f"*{ext}" for ext in video_extensions]
        else:  # all
            extensions = image_extensions + video_extensions
            patterns = [f"*{ext}" for ext in extensions]
        
        # 搜索所有匹配的媒体文件
        media_files: List[Path] = []
        for pattern in patterns:
            media_files.extend(search_files(base_dir, pattern))
        
        if not media_files:
            return f"No {media_type} files found in {directory}"
        
        # 准备结果
        result = f"Found {len(media_files)} {media_type} files in {directory}:\n"
        for file_path in media_files:
            info = get_file_info(file_path)
            relative_path = file_path.relative_to(config.project_root)
            media_url = config.get_media_url(str(file_path))
            
            # 获取文件大小（友好格式）
            size = info["size"]
            if size < 1024:
                size_str = f"{size} bytes"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.2f} MB"
            
            result += f"- {relative_path} ({size_str}, {file_path.suffix.lower()})\n  在线查看: {media_url}\n"
        
        return result
    except Exception as e:
        logger.error(f"Error in list_media_files: {e}")
        return f"Error: {str(e)}"


@mcp.tool()
def get_project_info() -> str:
    """
    获取项目基本信息
    
    Returns:
        项目信息
    """
    try:
        project_root = config.project_root
        info = {
            "name": config.server_name,
            "version": config.server_version,
            "root": str(project_root),
            "docs_root": str(config.docs_root),
            "i18n_root": str(config.i18n_root),
            "description": "BeeCount MCP Server for documentation access (docs and i18n directories)"
        }
        
        return f"""Project Information:
Name: {info['name']}
Version: {info['version']}
Root: {info['root']}
Docs Root: {info['docs_root']}
i18n Root: {info['i18n_root']}
Description: {info['description']}"""
    except Exception as e:
        logger.error(f"Error in get_project_info: {e}")
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run()
