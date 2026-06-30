import pytest
from messenger.domain.entities.mail_entity import Mail


def test_create_mail():
    mail = Mail.create(to="rx@example.com", subject="안녕하세요", body="내용입니다.")
    assert mail.to == "rx@example.com"
    assert str(mail.subject) == "안녕하세요"
    assert mail.is_valid()


def test_empty_body_is_invalid():
    mail = Mail.create(to="rx@example.com", subject="제목", body="   ")
    assert not mail.is_valid()


def test_invalid_recipient_raises():
    with pytest.raises(ValueError):
        Mail.create(to="bad-email", subject="제목", body="내용")
