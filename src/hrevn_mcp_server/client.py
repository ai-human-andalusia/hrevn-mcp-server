from __future__ import annotations

import json
from typing import Any
from urllib import error, request

from .config import settings


class HrevnApiError(RuntimeError):
    def __init__(self, status_code: int, payload: dict[str, Any] | None = None, message: str | None = None):
        self.status_code = status_code
        self.payload = payload or {}
        self.message = message or self.payload.get("message") or "HREVN managed API request failed"
        super().__init__(self.message)


class HrevnManagedClient:
    def __init__(self, base_url: str | None = None, api_key: str | None = None, timeout_seconds: int | None = None):
        self.base_url = (base_url or settings.normalized_api_base_url).rstrip("/")
        self.api_key = api_key if api_key is not None else settings.api_key
        self.timeout_seconds = timeout_seconds or settings.request_timeout_seconds

    def _request(self, method: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
        body = None
        headers = {
            "Accept": "application/json",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except error.HTTPError as exc:
            raw = exc.read().decode("utf-8")
            try:
                payload = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                payload = {"message": raw or f"HTTP {exc.code}"}
            raise HrevnApiError(status_code=exc.code, payload=payload) from exc
        except error.URLError as exc:
            raise HrevnApiError(status_code=0, message=str(exc.reason)) from exc

    def baseline_check(self, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/baseline-check", arguments)

    def profile_validate(self, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/profile/validate", arguments)

    def generate_bundle(self, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/generate-bundle", arguments)

    def verify_bundle(self, arguments: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", "/v1/verify-bundle", arguments)
