# tests/test_branch_generator.py

import pytest
from src.core.branch_generator import generate


class TestGenerate:
    def test_ticket_ile_feat(self):
        result = generate("feat", "dev", "PRJ-123", "user login")
        assert result.is_valid is True
        assert result.branch_name == "feat/PRJ-123-user-login"
        assert result.git_command == "git checkout -b feat/PRJ-123-user-login"

    def test_ticket_olmadan_feat(self):
        result = generate("feat", "dev", "", "user login")
        assert result.is_valid is True
        assert result.branch_name == "feat/user-login"

    def test_turkce_aciklama(self):
        result = generate("feat", "dev", "", "Kullanıcı Girişi")
        assert result.is_valid is True
        assert result.branch_name == "feat/kullanici-girisi"

    def test_hotfix_master(self):
        result = generate("hotfix", "master", "PRJ-456", "payment null pointer")
        assert result.is_valid is True
        assert result.branch_name == "hotfix/PRJ-456-payment-null-pointer"

    def test_yanlis_kaynak_branch(self):
        result = generate("feat", "master", "", "user login")
        assert result.is_valid is False
        assert result.error != ""

    def test_bos_aciklama(self):
        result = generate("feat", "dev", "", "")
        assert result.is_valid is False

    def test_gecersiz_ticket(self):
        result = generate("feat", "dev", "123prj", "user login")
        assert result.is_valid is False

    def test_bugfix_test_branch(self):
        result = generate("bugfix", "test", "PRJ-789", "session timeout")
        assert result.is_valid is True
        assert result.branch_name == "bugfix/PRJ-789-session-timeout"

    def test_kucuk_ticket_normalize(self):
        result = generate("fix", "dev", "prj-100", "fix login")
        assert result.is_valid is True
        assert "PRJ-100" in result.branch_name
