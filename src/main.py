"""Главный модуль запуска конвейера маршрутизации IT-обращений."""
import logging
import sys
from pathlib import Path
from src.file_handler import FileHandler
from src.classifier import EmailClassifier


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def main():
    """Точка входа в программу."""
    logger.info("Запуск конвейера маршрутизации IT-обращений...")

    base_dir = Path(__file__).resolve().parent.parent
    inbox_dir = base_dir / 'inbox'
    output_dir = base_dir / 'output'
    config_path = base_dir / 'src' / 'config.json'

    try:
        file_handler = FileHandler(inbox_dir, output_dir)
        classifier = EmailClassifier(config_path)
    except Exception as e:
        logger.critical("Сбой инициализации: %s", e)
        return

    files_to_process = file_handler.get_all_inbox_files()
    if not files_to_process:
        logger.warning("Папка %s пуста. Нечего обрабатывать.", inbox_dir)
        return

    logger.info("Найдено файлов для обработки: %s", len(files_to_process))

    stats = {category: 0 for category in classifier.rules}
    stats[classifier.default_category] = 0

    for file_path in files_to_process:
        document = file_handler.read_email(file_path)

        if document.is_readable:
            category = classifier.classify(document.content)
        else:
            category = classifier.default_category

        file_handler.route_file(document, category)
        stats[category] += 1

    logger.info("===" * 15)
    logger.info("ОТЧЕТ О МАРШРУТИЗАЦИИ:")
    for cat, count in stats.items():
        if count > 0:
            logger.info("  - %s: %s писем", cat, count)
    logger.info("===" * 15)
    logger.info("Все отсортированные файлы находятся в: %s", output_dir)


if __name__ == "__main__":
    main()
