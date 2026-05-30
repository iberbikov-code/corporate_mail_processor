from pathlib import Path
from src.file_handler import FileHandler

def test_read_binary_file_handled_gracefully(tmp_path):
    """Проверка, что программа не падает при чтении бинарного файла."""
    bad_file = tmp_path / "corrupted_mail.bin"
    bad_file.write_bytes(b'\xff\xfe\x00\x11\x22')

    handler = FileHandler(inbox_dir=str(tmp_path), output_dir=str(tmp_path))
    
    email_doc = handler.read_email(bad_file)

    assert email_doc.is_readable is False