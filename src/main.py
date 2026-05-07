# src/main.py

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# __file__ dizininden yola çıkarak projenin kök dizinini sys.path'e ekle
# Bu sayede src.* importları çalışır
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.ui.main_window import MainWindow

def load_stylesheet() -> str:
    """QSS dosyasını okur ve string olarak döndürür."""
    qss_path = os.path.join(os.path.dirname(__file__), "ui", "styles", "main.qss")
    try:
        with open(qss_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Uyarı: Stil dosyası bulunamadı -> {qss_path}")
        return ""

def main():
    # HiDPI desteğini etkinleştir
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    
    # Stili uygula
    stylesheet = load_stylesheet()
    if stylesheet:
        app.setStyleSheet(stylesheet)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
