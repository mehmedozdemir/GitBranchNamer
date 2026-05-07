# Git Branch Naming Tool

5-10 kişilik yazılım ekiplerinde git branch isimlendirmesini standartlaştıran PyQt6 masaüstü uygulaması.

## Branch Standardı

### Format

```
# Ticket numarası olmadan:
{tip}/{kısa-açıklama}

# Ticket numarası ile:
{tip}/{TICKET-NO}-{kısa-açıklama}
```

### Branch Tipleri

| Tip        | Kaynak Branch        | Açıklama                    |
|------------|----------------------|-----------------------------|
| `feat`     | `dev`                | Yeni özellik                |
| `fix`      | `dev`                | Bug fix                     |
| `refactor` | `dev`                | Kod iyileştirme             |
| `chore`    | `dev`                | Altyapı, bağımlılık         |
| `docs`     | `dev`                | Dokümantasyon               |
| `bugfix`   | `test` / `preprod`   | Ortamda tespit edilen hata  |
| `hotfix`   | `preprod` / `master` | Canlıda acil düzeltme       |

---

## Geliştirici Kurulumu

```bash
# 1. Sanal ortam oluştur
python -m venv .venv

# 2. Aktive et
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. Çalıştır
python src/main.py
```

## Testleri Çalıştır

```bash
pytest tests/ -v
```

## Build (Dağıtım)

```bash
pyinstaller build/branch-tool.spec
# Çıktı: dist/branch-tool.exe
```
