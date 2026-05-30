import pytest
from src.models import EmailDocument
from src.classifier import EmailClassifier
from pathlib import Path

@pytest.fixture
def classifier():
    return EmailClassifier(config_path=Path("src/config.json"))

@pytest.mark.parametrize("email_text, expected_category", [
    ("У нас упал сервер базы данных, ошибка 500", "critical_incidents"),
    ("Прошу выдать доступ к Jira для нового сотрудника", "access_management"),
    ("Сломался экран у ноутбука, ничего не видно", "hardware_issues"),
    ("Направляю закрывающие документы и счет на оплату", "hr_finance_docs"),
    ("Срочно введите данные банковской карты для подтверждения", "security_phishing"),
    ("Обычное письмо про то, как прошел день", "quarantine"),
    ("", "quarantine"),
    ("   \n  \t ", "quarantine")
])
def test_classification_logic(classifier, email_text, expected_category):
    email = EmailDocument(file_path="dummy.txt", is_readable=True, content=email_text)
    result = classifier.classify(email.content)
    assert result == expected_category