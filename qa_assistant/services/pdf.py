import asyncio
from dataclasses import dataclass
from io import BytesIO
from typing import Any, List, Dict, Tuple
import json
import tempfile

import httpx
import pdfplumber
import camelot

from qa_assistant.providers.base import HttpProvider
from qa_assistant.settings import settings


def _canonical_json_bytes(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


@dataclass
class PdfService:
    def __init__(self):
        self.http = httpx.AsyncClient()

    async def process_url(self, url: str, *, headers: dict | None = None, timeout: int = 60) -> Any:
        return await self.http.get(url, headers=headers, timeout=timeout)


if __name__ == "__main__":
    url = "https://api.itmo.su/constructor-ep/api/v1/static/programs/10033/plan/abit/pdf"
    pdf = PdfService()
    res = asyncio.run(pdf.process_url(url))
    print(res.json())
