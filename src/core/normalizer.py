# src/core/normalizer.py

import re
from .constants import TR_CHAR_MAP, MAX_DESCRIPTION_LENGTH


def normalize_description(text: str) -> str:
    """
    Ham açıklama metnini geçerli branch parçasına dönüştürür.
    Adımlar:
      1. Türkçe karakterleri Latin karşılıklarına çevir
      2. Küçük harfe çevir
      3. Boşluk ve alt çizgiyi tireye çevir
      4. İzin verilmeyen karakterleri sil
      5. Ardışık tireleri tekli tireye indir
      6. Baş/son tireleri temizle
      7. 50 karakter sınırını uygula
    """
    # 1. Türkçe karakter dönüşümü
    for tr_char, lat_char in TR_CHAR_MAP.items():
        text = text.replace(tr_char, lat_char)

    # 2. Küçük harfe çevir
    text = text.lower()

    # 3. Boşluk ve alt çizgiyi tireye çevir
    text = re.sub(r"[\s_]+", "-", text)

    # 4. İzin verilmeyen karakterleri sil (sadece a-z, 0-9, - kalır)
    text = re.sub(r"[^a-z0-9\-]", "", text)

    # 5. Ardışık tireleri tekli tireye indir
    text = re.sub(r"-{2,}", "-", text)

    # 6. Baş/son tireleri temizle
    text = text.strip("-")

    # 7. Uzunluk sınırı
    text = text[:MAX_DESCRIPTION_LENGTH]

    # Kırpma sonrası oluşan sondaki tireyi temizle
    text = text.strip("-")

    return text


def normalize_ticket(ticket: str) -> str:
    """
    Ticket numarasını normalize eder.
    Büyük harfe çevirir, boşlukları temizler.
    Örn: 'prj-123' → 'PRJ-123'
    """
    ticket = ticket.strip().upper()
    ticket = re.sub(r"\s+", "", ticket)
    return ticket
