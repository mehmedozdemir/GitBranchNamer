# src/utils/clipboard.py

from PyQt6.QtWidgets import QApplication

def copy_to_clipboard(text: str) -> bool:
    """
    Verilen metni sistem panosuna (clipboard) kopyalar.
    """
    clipboard = QApplication.clipboard()
    if clipboard:
        clipboard.setText(text)
        return True
    return False
