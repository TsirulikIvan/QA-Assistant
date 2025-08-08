from typing import Protocol


class HttpProvider(Protocol):
    def get(self, url: str, *, headers: dict | None = None, timeout: int = 60) -> bytes: ...
