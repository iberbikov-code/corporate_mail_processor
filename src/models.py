"""Модули данных для проекта."""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class EmailDocument:
    """Модель данных, представляющая входящее письмо или файл."""
    file_path: Path
    is_readable: bool
    content: str = ""
    category: Optional[str] = None
