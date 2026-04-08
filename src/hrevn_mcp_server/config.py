from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    api_base_url: str = os.getenv("HREVN_API_BASE_URL", "https://api.hrevn.com")
    api_key: str = os.getenv("HREVN_API_KEY", "")
    request_timeout_seconds: int = int(os.getenv("HREVN_MCP_TIMEOUT_SECONDS", "30"))
    server_name: str = os.getenv("HREVN_MCP_SERVER_NAME", "hrevn-mcp-server")
    server_version: str = os.getenv("HREVN_MCP_SERVER_VERSION", "0.1.0a0")

    @property
    def normalized_api_base_url(self) -> str:
        return self.api_base_url.rstrip("/")


settings = Settings()
