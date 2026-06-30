import pytest
from messenger.domain.value_objects.email_address_vo import EmailAddress


def test_valid_email():
    vo = EmailAddress.from_raw("test@example.com")
    assert str(vo) == "test@example.com"


def test_email_normalized_to_lowercase():
    vo = EmailAddress.from_raw("TEST@EXAMPLE.COM")
    assert vo.value == "test@example.com"


def test_invalid_email_raises():
    with pytest.raises(ValueError):
        EmailAddress.from_raw("not-an-email")


def test_missing_domain_raises():
    with pytest.raises(ValueError):
        EmailAddress.from_raw("user@")
