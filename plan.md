# Git Branch Naming Tool — Geliştirme Planı

## Proje Özeti

5-10 kişilik yazılım ekiplerinde git branch isimlendirmesini standartlaştıran PyQt6 masaüstü uygulaması.  
Developer birkaç soruyu yanıtlar, uygulama dünya standartlarında bir branch adı üretir ve kopyalamaya hazır sunar.

---

## Teknoloji Yığını

| Katman       | Teknoloji              |
|--------------|------------------------|
| Dil          | Python 3.11+           |
| UI Framework | PyQt6                  |
| Stil         | Qt StyleSheets (QSS)   |
| Dağıtım      | PyInstaller (tek .exe) |
| Test         | pytest + pytest-qt     |

---

## Branch Standardı (Karar Verildi)

### Format

```
# Ticket numarası olmadan:
{tip}/{kısa-açıklama}

# Ticket numarası ile:
{tip}/{TICKET-NO}-{kısa-açıklama}
```

### Örnekler

```
feat/user-authentication
feat/PRJ-123-user-authentication
fix/login-redirect-loop
hotfix/PRJ-456-payment-null-pointer
bugfix/PRJ-789-session-timeout
refactor/auth-service-cleanup
chore/update-dependencies
docs/api-endpoints
```

### Branch Tipleri ve Kaynak Branch Kuralları

| Tip        | Kaynak Branch          | Açıklama                        |
|------------|------------------------|---------------------------------|
| `feat`     | `dev`                  | Yeni özellik geliştirme         |
| `fix`      | `dev`                  | Normal hata düzeltme            |
| `refactor` | `dev`                  | Kod yeniden yapılandırma        |
| `chore`    | `dev`                  | Bağımlılık, config, altyapı     |
| `docs`     | `dev`                  | Dokümantasyon güncellemesi      |
| `bugfix`   | `test` / `preprod`     | Ortamda tespit edilen hata      |
| `hotfix`   | `master` / `preprod`   | Canlı ortamda acil düzeltme     |

### İsimlendirme Kuralları

- Tümü **küçük harf**
- Boşluk yerine **tire** (`-`)
- **Türkçe karakter** kullanılmaz → otomatik dönüştürülür
- **Özel karakter** kullanılmaz (`!`, `@`, `#`, vb.)
- Açıklama kısmı maksimum **50 karakter**
- Ticket numarası varsa açıklamadan önce tire ile ayrılır

---

## Proje Dizin Yapısı

```
git-branch-naming/
│
├── plan.md                  # Bu dosya — geliştirme planı
├── requirements.txt         # Python bağımlılıkları
├── README.md                # Kullanım kılavuzu
│
├── src/
│   ├── main.py              # Uygulama giriş noktası
│   ├── app.py               # QApplication başlatma
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Ana pencere widget'ı
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── branch_form.py     # Form alanları
│   │   │   ├── preview_box.py     # Canlı önizleme kutusu
│   │   │   └── copy_button.py     # Kopyala / Git komutu butonu
│   │   └── styles/
│   │       └── main.qss           # Uygulama teması
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── branch_generator.py    # Branch adı üretim motoru
│   │   ├── normalizer.py          # Metin normalleştirme (TR→EN, boşluk→tire vb.)
│   │   ├── validator.py           # Kural doğrulama
│   │   └── constants.py           # Tip listesi, kaynak branch kuralları
│   │
│   └── utils/
│       ├── __init__.py
│       └── clipboard.py           # Pano işlemleri
│
├── tests/
│   ├── test_normalizer.py
│   ├── test_validator.py
│   └── test_branch_generator.py
│
└── build/
    └── branch-tool.spec           # PyInstaller config
```

---

## Geliştirme Fazları

---

### FAZA 1 — Temel Çekirdek (Core) `[~2 saat]`

> **Hedef:** UI olmadan iş mantığı tamamlanmış ve test edilmiş olsun.

#### Görevler

**`src/core/constants.py`**
- Branch tip listesini tanımla (`feat`, `fix`, `hotfix`, `bugfix`, `refactor`, `chore`, `docs`)
- Her tip için izin verilen kaynak branch listesini tanımla
- Separator karakterini tanımla

**`src/core/normalizer.py`**
- Türkçe karakterleri Latin karşılıklarına çevir (`ş→s`, `ğ→g`, `ı→i`, `ö→o`, `ü→u`, `ç→c`, `İ→i` vb.)
- Büyük harfleri küçük harfe çevir
- Boşlukları ve alt çizgileri tireye çevir
- İzin verilmeyen karakterleri temizle (`[^a-z0-9\-]`)
- Birden fazla ardışık tireyi tekli tireye indir
- Başındaki ve sonundaki tireleri temizle
- 50 karakter sınırını uygula

**`src/core/validator.py`**
- Branch adının boş olmadığını kontrol et
- Açıklamanın en az 3 karakter olduğunu doğrula
- Ticket no girildiyse format kontrolü yap (sadece harf, rakam, tire — örn. `PRJ-123`, `PROJ-1`)
- Seçilen tip ile kaynak branch uyumunu doğrula

**`src/core/branch_generator.py`**
- `normalizer` ve `validator` kullanarak final branch adını üret
- Ticket no varsa: `{tip}/{ticket_no}-{açıklama}`
- Ticket no yoksa: `{tip}/{açıklama}`
- `git checkout -b {branch_adı}` komutunu da üret

**`tests/`**
- Normalizer için birim testler yaz (Türkçe karakterler, özel karakterler, uzun metin)
- Validator için hata durumu testleri yaz
- Branch generator için kombinasyon testleri yaz

#### Faz 1 Çıktısı
`python -c "from src.core.branch_generator import generate; print(generate('feat', 'PRJ-123', 'Kullanıcı Girişi'))"`  
→ `feat/PRJ-123-kullanici-girisi`

---

### FAZA 2 — Ana UI `[~3 saat]`

> **Hedef:** Çalışan, form doldurulabilir, önizlemeli uygulama penceresi.

#### Görevler

**`src/ui/main_window.py`**
- `QMainWindow` sınıfını kur
- Pencere boyutunu sabitle: **480 × 400 px** (yeniden boyutlandırılamaz)
- Pencere başlığı: `Git Branch Generator`
- Layout: Dikey merkez hizamalı, 24px kenar boşluğu
- Form bölümü + önizleme bölümü + buton bölümü şeklinde üç blok

**`src/ui/components/branch_form.py`**
- **Branch Tipi** → `QComboBox` (feat, fix, hotfix, bugfix, refactor, chore, docs)
- **Kaynak Branch** → `QComboBox` — seçilen tipe göre otomatik filtrele (sadece uygun olanları göster)
- **Ticket No** → `QLineEdit` — placeholder: `PRJ-123  (opsiyonel)`, büyük harfe otomatik çevir
- **Açıklama** → `QLineEdit` — placeholder: `kısa açıklama`, karakter sayacı göster (`0/50`)
- Her alan değiştiğinde `branch_changed` sinyali yayınla

**`src/ui/components/preview_box.py`**
- Koyu arka planlı `QLabel` kutusu
- İçeriği anlık güncellenir (branch adı büyük monospace font ile)
- Geçersiz durumda kırmızı çerçeve + hata mesajı göster
- Geçerli durumda yeşil çerçeve

**`src/ui/components/copy_button.py`**
- **"Branch Adını Kopyala"** butonu → sadece branch adını panoya kopyalar
- **"Git Komutunu Kopyala"** butonu → `git checkout -b {branch}` komutunu kopyalar
- Kopyalama sonrası 2 saniye "✓ Kopyalandı!" göster, sonra eski haline dön

**Sinyal-Slot bağlantıları**
- Form değişikliği → `branch_generator.generate()` çağır → preview güncelle
- Copy butonları → `clipboard.copy()` çağır

#### Faz 2 Çıktısı
Uygulama açılır, form doldurulur, branch adı anlık görünür, kopyalanır.

---

### FAZA 3 — Tema ve Stil `[~1 saat]`

> **Hedef:** Profesyonel, sade, geliştirici dostu görünüm.

#### Görevler

**`src/ui/styles/main.qss`**
- Genel arka plan: `#1e1e2e` (koyu mor-gri)
- Form alanları: `#2a2a3e` arka plan, `#cdd6f4` yazı rengi
- Önizleme kutusu: `#11111b` arka plan, `#a6e3a1` yeşil monospace yazı (Catppuccin Mocha paleti)
- Butonlar: `#89b4fa` mavi arka plan, hover'da açılır
- Hata durumu: `#f38ba8` kırmızı çerçeve
- Başarı durumu: `#a6e3a1` yeşil çerçeve
- Font: Sistem monospace (Consolas / SF Mono / DejaVu Sans Mono)

**`src/app.py`**
- QSS dosyasını yükle ve uygulamaya uygula
- HiDPI desteğini aç (`Qt.HighDpiScaleFactorRoundingPolicy`)

#### Faz 3 Çıktısı
Görsel olarak karanlık temalı, okunabilir, profesyonel uygulama.

---

### FAZA 4 — Dağıtım `[~1 saat]`

> **Hedef:** Ekipteki herkese dağıtılabilir tek dosya çalıştırılabilir.

#### Görevler

**`requirements.txt`**
```
PyQt6>=6.6.0
PyInstaller>=6.0.0
pytest>=8.0.0
pytest-qt>=4.4.0
```

**`build/branch-tool.spec`**
- PyInstaller spec dosyasını yapılandır
- QSS ve ikon dosyalarını bundle'a dahil et
- Windows için: tek `.exe` çıktısı, konsol penceresi gizli
- macOS için: `.app` bundle

**`README.md`**
- Kurulum adımları
- Geliştirici ortamı kurulumu (`python -m venv`, `pip install`)
- Build komutu
- Branch standardı referansı (kısa özet)

**`Makefile` (opsiyonel)**
```makefile
run:    python src/main.py
test:   pytest tests/ -v
build:  pyinstaller build/branch-tool.spec
```

#### Faz 4 Çıktısı
`dist/branch-tool.exe` — çift tıkla çalışır, kurulum gerektirmez.

---

## UI Akışı (Kullanıcı Perspektifi)

```
┌─────────────────────────────────────┐
│  🌿 Git Branch Generator            │
├─────────────────────────────────────┤
│                                     │
│  Branch Tipi   [ feat          ▼ ]  │
│                                     │
│  Kaynak Branch [ dev           ▼ ]  │
│                                     │
│  Ticket No     [ PRJ-123          ] │
│                (opsiyonel)          │
│                                     │
│  Açıklama      [ user login       ] │
│                               8/50  │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  feat/PRJ-123-user-login    │    │
│  └─────────────────────────────┘    │
│                                     │
│  [ Branch Adını Kopyala ]           │
│  [ Git Komutunu Kopyala ]           │
│                                     │
└─────────────────────────────────────┘
```

---

## Hata Senaryoları ve Davranışlar

| Durum                              | Davranış                                      |
|------------------------------------|-----------------------------------------------|
| Açıklama boş                       | Önizleme boş, butonlar disabled              |
| Açıklama 3 karakterden kısa        | Kırmızı çerçeve + "En az 3 karakter girin"   |
| Ticket no geçersiz format          | Kırmızı çerçeve + "Geçersiz ticket formatı"  |
| Tip-kaynak branch uyumsuzluğu      | Otomatik kaynak branch filtrele              |
| Açıklama 50 karakteri aştı         | Otomatik kes + sayaç kırmızıya döner         |

---

## Geliştirme Sırası (Özet)

```
Faz 1 → core/ klasörü + testler     (iş mantığı)
Faz 2 → ui/ klasörü                  (pencere + form + önizleme)
Faz 3 → styles/main.qss              (görsel tema)
Faz 4 → build + README               (dağıtım)
```

Her faz bağımsız olarak tamamlanabilir ve test edilebilir.
