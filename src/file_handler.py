"""Модуль для работы с файловой системой и маршрутизации файлов."""
import shutil
import logging
from pathlib import Path
from src.models import EmailDocument
from typing import Union

logger = logging.getLogger(__name__)


class FileHandler:
    """Класс для безопасной работы с файловой системой."""
    def __init__(self, inbox_dir: Union[str, Path], output_dir: Union[str, Path]):
        self.inbox_dir = Path(inbox_dir)
        self.output_dir = Path(output_dir)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Создает базовые папки, если их случайно удалили."""
        self.inbox_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def read_email(self, file_path: Path) -> EmailDocument:
        """Безопасно читает файл. Перехватывает ошибки бинарников."""
        if file_path.name.startswith('.'):
            return EmailDocument(file_path=file_path, is_readable=False)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return EmailDocument(file_path=file_path, is_readable=True, content=content)

        except UnicodeDecodeError:
            logger.warning("Файл %s не является текстом. Пропуск.", file_path.name)
            return EmailDocument(file_path=file_path, is_readable=False)

        except Exception as e:
            logger.error("Непредвиденная ошибка при чтении %s: %s", file_path.name, e)
            return EmailDocument(file_path=file_path, is_readable=False)

    def route_file(self, document: EmailDocument, category: str) -> None:
        """Копирует файл в папку соответствующей категории."""
        category_dir = self.output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        destination = category_dir / document.file_path.name
        try:
            shutil.copy2(document.file_path, destination)
            logger.debug("Файл %s успешно отправлен в %s", document.file_path.name, category)
        except Exception as e:
            logger.error("Ошибка маршрутизации %s: %s", document.file_path.name, e)

    def get_all_inbox_files(self) -> list[Path]:
        """Возвращает список всех файлов в папке входящих."""
        return [f for f in self.inbox_dir.iterdir() if f.is_file()]
