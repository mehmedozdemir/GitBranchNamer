# src/ui/components/preview_box.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class PreviewBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.preview_label = QLabel("Branch adı burada görünecek")
        self.preview_label.setObjectName("preview_label")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setWordWrap(True)
        self.preview_label.setMinimumHeight(60)
        
        self.error_label = QLabel("")
        self.error_label.setObjectName("error_label")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide() # Başlangıçta gizli
        
        layout.addWidget(self.preview_label)
        layout.addWidget(self.error_label)
        self.setLayout(layout)
        
        self.set_valid_state(False, "Açıklama giriniz.")

    def update_preview(self, branch_name: str, is_valid: bool, error: str = ""):
        self.preview_label.setText(branch_name if branch_name else "...")
        self.set_valid_state(is_valid, error)

    def set_valid_state(self, is_valid: bool, error: str):
        if is_valid:
            self.preview_label.setProperty("state", "valid")
            self.error_label.hide()
        else:
            self.preview_label.setProperty("state", "invalid")
            self.error_label.setText(error)
            self.error_label.show()
            
        # Stil güncellemesini tetikle
        self.preview_label.style().unpolish(self.preview_label)
        self.preview_label.style().polish(self.preview_label)
