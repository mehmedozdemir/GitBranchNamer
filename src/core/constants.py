# src/core/constants.py

# Branch tipleri ve izin verilen kaynak branch'ler
BRANCH_TYPES = {
    "feat":     ["dev"],
    "fix":      ["dev"],
    "refactor": ["dev"],
    "chore":    ["dev"],
    "docs":     ["dev"],
    "bugfix":   ["test", "preprod"],
    "hotfix":   ["preprod", "master"],
}

# Kaynak branch'e göre izin verilen branch tipleri (BRANCH_TYPES'ın tersi)
SOURCE_TO_TYPES: dict[str, list[str]] = {}
for _btype, _sources in BRANCH_TYPES.items():
    for _src in _sources:
        SOURCE_TO_TYPES.setdefault(_src, []).append(_btype)

# Ortam branch'leri (kalıcı)
ENV_BRANCHES = ["dev", "test", "preprod", "master"]

# Açıklama maksimum karakter sayısı
MAX_DESCRIPTION_LENGTH = 50

# Türkçe karakter dönüşüm tablosu
TR_CHAR_MAP = {
    "ş": "s", "Ş": "s",
    "ğ": "g", "Ğ": "g",
    "ı": "i", "I": "i",
    "İ": "i", "i": "i",
    "ö": "o", "Ö": "o",
    "ü": "u", "Ü": "u",
    "ç": "c", "Ç": "c",
}
