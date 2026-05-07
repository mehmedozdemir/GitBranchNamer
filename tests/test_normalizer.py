# tests/test_normalizer.py

import pytest
from src.core.normalizer import normalize_description, normalize_ticket


class TestNormalizeDescription:
    def test_turkce_karakterler(self):
        assert normalize_description("Kullanıcı Girişi") == "kullanici-girisi"

    def test_buyuk_harf(self):
        assert normalize_description("UserLogin") == "userlogin"

    def test_bosluk_tire_donusumu(self):
        assert normalize_description("user login page") == "user-login-page"

    def test_alt_cizgi_tire_donusumu(self):
        assert normalize_description("user_login_page") == "user-login-page"

    def test_ozel_karakter_temizleme(self):
        assert normalize_description("user@login!page") == "userloginpage"

    def test_ardisik_tire(self):
        assert normalize_description("user  login") == "user-login"

    def test_bas_son_tire_temizleme(self):
        assert normalize_description("  user login  ") == "user-login"

    def test_50_karakter_siniri(self):
        uzun_metin = "a" * 60
        assert len(normalize_description(uzun_metin)) <= 50

    def test_tum_turkce(self):
        assert normalize_description("şğıöüçİĞŞÖÜÇ") == "sgioucigsouc"

    def test_bos_metin(self):
        assert normalize_description("") == ""


class TestNormalizeTicket:
    def test_kucuk_harf_buyutur(self):
        assert normalize_ticket("prj-123") == "PRJ-123"

    def test_bosluk_temizler(self):
        assert normalize_ticket("  PRJ-123  ") == "PRJ-123"

    def test_bos_string(self):
        assert normalize_ticket("") == ""
