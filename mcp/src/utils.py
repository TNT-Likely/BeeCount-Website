import logging
from typing import Any, Callable, Dict, List
from pathlib import Path

from .config import config


def setup_logger(name: str = "mcp_server") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, config.log_level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger


logger = setup_logger()


def format_error(error: Exception) -> str:
    return f"{type(error).__name__}: {str(error)}"


def safe_execute(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {format_error(e)}")
        raise


def truncate_text(text: str, max_length: int = 500) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def validate_path(path: str) -> Path:
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    return path_obj


def search_files(root_dir: Path, pattern: str = "*") -> List[Path]:
    if not root_dir.exists():
        raise FileNotFoundError(f"Directory not found: {root_dir}")
    
    files = list(root_dir.rglob(pattern))
    return [f for f in files if f.is_file()]


def read_file_content(file_path: Path, line_range: str = "0~100") -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    start_line = 0
    end_line = None
    
    if line_range.lower() == "all":
        end_line = None
    elif "~" in line_range:
        try:
            parts = line_range.split("~")
            start_line = int(parts[0])
            end_line = int(parts[1])
        except (ValueError, IndexError):
            raise ValueError(f"Invalid line_range format: {line_range}. Expected format: '0~100' or 'all'")
    else:
        try:
            max_lines = int(line_range)
            start_line = 0
            end_line = max_lines
        except ValueError:
            raise ValueError(f"Invalid line_range format: {line_range}. Expected format: '0~100' or 'all'")
    
    lines: List[str] = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            if end_line is not None and i > end_line:
                if start_line == 0:
                    lines.append(f"\n... (truncated after {end_line} lines)")
                break
            if i > start_line:
                lines.append(line)
    
    return "".join(lines)


def get_file_info(file_path: Path) -> Dict[str, Any]:
    stat = file_path.stat()
    return {
        "name": file_path.name,
        "path": str(file_path),
        "size": stat.st_size,
        "extension": file_path.suffix,
        "is_file": file_path.is_file(),
        "is_dir": file_path.is_dir(),
    }
