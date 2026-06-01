import pytest 
from pathlib import Path
from src.file_handler import FileHandler
from src.models import EmailDocument

def test_read_binary_file_handled_gracefully(tmp_path):
    """Проверка, что программа не падает при чтении бинарного файла."""
    bad_file = tmp_path / "corrupted_mail.bin"
    bad_file.write_bytes(b'\xff\xfe\x00\x11\x22')

    handler = FileHandler(inbox_dir=str(tmp_path), output_dir=str(tmp_path))
    
    email_doc = handler.read_email(bad_file)

    assert email_doc.is_readable is False
def test_dotfile_is_skipped(tmp_path):
    """Файл, начинающийся с точки, не читается."""
    dot_file = tmp_path / ".gitkeep"
    dot_file.touch()
    handler = FileHandler(inbox_dir=str(tmp_path), output_dir=str(tmp_path))
    doc = handler.read_email(dot_file)
    assert doc.is_readable is False

def test_get_all_inbox_files_excludes_hidden(tmp_path):
    """get_all_inbox_files не возвращает скрытые файлы (если бы они фильтровались)."""
    (tmp_path / ".gitkeep").touch()
    (tmp_path / "mail_001.txt").write_text("hello", encoding="utf-8")
    handler = FileHandler(inbox_dir=str(tmp_path), output_dir=str(tmp_path))
    files = handler.get_all_inbox_files()
    assert len(files) == 1
    assert files[0].name == "mail_001.txt"

def test_route_file_lands_in_correct_directory(tmp_path):
        """route_file копирует файл в нужную категорию с учетом уникального имени."""
        src = tmp_path / "mail.txt"
        src.write_text("test", encoding="utf-8")
        handler = FileHandler(inbox_dir=str(tmp_path), output_dir=str(tmp_path))
        doc = EmailDocument(file_path=src, is_readable=True, content="test")
        handler.route_file(doc, "critical_incidents")
        
        category_dir = tmp_path / "critical_incidents"
        assert category_dir.exists()
        files = list(category_dir.glob("mail_*.txt"))
        assert len(files) == 1