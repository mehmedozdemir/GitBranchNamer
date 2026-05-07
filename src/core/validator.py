# src/core/validator.py

import re
from .constants import BRANCH_TYPES


def validate_description(description: str) -> tuple[bool, str]:
    """
    Normalize edilmiş açıklamayı doğrular.
    Returns: (geçerli_mi, hata_mesajı)
    """
    if not description:
        return False, "Açıklama boş olamaz."
    if len(description) < 3:
        return False, "Açıklama en az 3 karakter olmalı."
    return True, ""


def validate_ticket(ticket: str) -> tuple[bool, str]:
    """
    Ticket numarasını doğrular. Boşsa geçerli sayılır (opsiyonel).
    Kabul edilen formatlar: PRJ-123, PROJ-1, ISSUE-9999
    Returns: (geçerli_mi, hata_mesajı)
    """
    if not ticket:
        return True, ""  # Opsiyonel — boş geçerli

    pattern = r"^[A-Z][A-Z0-9]*-[0-9]+$"
    if not re.match(pattern, ticket):
        return False, "Ticket formatı geçersiz. Örn: PRJ-123"
    return True, ""


def validate_source_branch(branch_type: str, source_branch: str) -> tuple[bool, str]:
    """
    Branch tipi ile kaynak branch uyumunu doğrular.
    Returns: (geçerli_mi, hata_mesajı)
    """
    allowed = BRANCH_TYPES.get(branch_type, [])
    if source_branch not in allowed:
        return False, f"'{branch_type}' tipi için kaynak branch şunlardan biri olmalı: {', '.join(allowed)}"
    return True, ""
