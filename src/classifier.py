"""Модуль бизнес-логики и классификации писем."""
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class EmailClassifier:
    """Классификатор писем на основе лексических маркеров."""
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.rules: dict[str, list[str]] = {}
        self.default_category: str = "quarantine"
        self._load_rules()

    def _load_rules(self) -> None:
        """Загружает матрицу маршрутизации из JSON файла."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.rules = config.get("categories", {})
                self.default_category = config.get("default_category", "quarantine")
            logger.info("Успешно загружены правила маршрутизации из %s", self.config_path.name)
        except FileNotFoundError:
            logger.critical("Файл конфигурации не найден: %s", self.config_path)
            raise
        except json.JSONDecodeError:
            logger.critical("Ошибка чтения JSON в файле %s", self.config_path)
            raise

    def classify(self, content: str) -> str:
        """Определяет категорию письма на основе его содержимого."""
        if not content:
            return self.default_category

        content_lower = content.lower()

        for category, markers in self.rules.items():
            for marker in markers:
                if marker in content_lower:
                    logger.debug("Найдено совпадение: '%s' -> Категория: %s", marker, category)
                    return category

        logger.debug("Совпадений не найдено. Отправка в карантин.")
        return self.default_category
