from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    server_name: str = Field(default="BeeCount MCP Server", description="服务器名称")
    server_version: str = Field(default="1.0.0", description="服务器版本")
    log_level: str = Field(default="INFO", description="日志级别")
    website_url: str = Field(default="https://beecount.youths.cc", description="网站URL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


class Config:
    _instance: Optional["Config"] = None
    _settings: Optional[Settings] = None
    
    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if self._settings is None:
            self._settings = Settings()
    
    @property
    def settings(self) -> Settings:
        if self._settings is None:
            self._settings = Settings()
        return self._settings
    
    @property
    def server_name(self) -> str:
        return self.settings.server_name
    
    @property
    def server_version(self) -> str:
        return self.settings.server_version
    
    @property
    def log_level(self) -> str:
        return self.settings.log_level
    
    @property
    def website_url(self) -> str:
        return self.settings.website_url
    
    def get_document_url(self, file_path: str, language: str = "zh") -> str:
        """根据文件路径生成对应的网站 URL"""
        if language == "zh":
            path = file_path.replace(".md", "")
            return f"{self.website_url}/docs/{path}"
        else:
            path = file_path.replace(".md", "")
            return f"{self.website_url}/{language}/docs/{path}"
    
    def get_media_url(self, file_path: str) -> str:
        """根据媒体文件路径生成对应的网站 URL"""
        relative_path = Path(file_path).relative_to(self.project_root / "static")
        return f"{self.website_url}/{relative_path.as_posix()}"
    
    @property
    def project_root(self) -> Path:
        return Path(__file__).parent.parent.parent
    
    @property
    def mcp_root(self) -> Path:
        return Path(__file__).parent.parent
    
    @property
    def docs_root(self) -> Path:
        return self.project_root / "docs"
    
    @property
    def i18n_root(self) -> Path:
        return self.project_root / "i18n"
    
    def get_i18n_language_root(self, language: str) -> Path:
        """获取指定语言的文档根目录"""
        return self.i18n_root / language / "docusaurus-plugin-content-docs" / "current"

    def get_language_root(self, language: str) -> Path:
        """获取指定语言的文档根目录（支持中文和多语言）"""
        if language == "zh":
            return self.docs_root
        return self.get_i18n_language_root(language)


config = Config()
