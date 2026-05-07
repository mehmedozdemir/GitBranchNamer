# tests/test_validator.py

import pytest
from src.core.validator import validate_description, validate_ticket, validate_source_branch


class TestValidateDescription:
    def test_gecerli_aciklama(self):
        valid, err = validate_description("user-login")
        assert valid is True
        assert err == ""

    def test_bos_aciklama(self):
        valid, err = validate_description("")
        assert valid is False

    def test_cok_kisa_aciklama(self):
        valid, err = validate_description("ab")
        assert valid is False


class TestValidateTicket:
    def test_bos_ticket_gecerli(self):
        valid, err = validate_ticket("")
        assert valid is True

    def test_gecerli_ticket(self):
        valid, err = validate_ticket("PRJ-123")
        assert valid is True

    def test_gecersiz_ticket_format(self):
        valid, err = validate_ticket("123-PRJ")
        assert valid is False

    def test_gecersiz_ticket_bosluk(self):
        valid, err = validate_ticket("PRJ 123")
        assert valid is False


class TestValidateSourceBranch:
    def test_feat_dev_gecerli(self):
        valid, err = validate_source_branch("feat", "dev")
        assert valid is True

    def test_hotfix_master_gecerli(self):
        valid, err = validate_source_branch("hotfix", "master")
        assert valid is True

    def test_feat_master_gecersiz(self):
        valid, err = validate_source_branch("feat", "master")
        assert valid is False

    def test_hotfix_dev_gecersiz(self):
        valid, err = validate_source_branch("hotfix", "dev")
        assert valid is False
