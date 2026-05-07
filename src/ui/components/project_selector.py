# src/ui/components/project_selector.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtCore import pyqtSignal

class ProjectSelector(QWidget):
    project_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel("Hedef Proje:")
        label.setFixedWidth(100)
        
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        self.path_input.setPlaceholderText("Lütfen bir git projesi klasörü seçin...")
        
        self.btn_select = QPushButton("Seç...")
        self.btn_select.setFixedWidth(80)
        self.btn_select.clicked.connect(self.select_directory)
        
        layout.addWidget(label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.btn_select)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(layout)
        
        self.status_label = QLabel("Git Durumu: Proje seçilmedi")
        self.status_label.setObjectName("git_status_label")
        
        self.btn_refresh = QPushButton("↻ Yenile")
        self.btn_refresh.setFixedWidth(80)
        self.btn_refresh.clicked.connect(lambda: self.project_changed.emit(self.get_path()))
        
        status_layout = QHBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.btn_refresh)
        
        main_layout.addLayout(status_layout)
        self.setLayout(main_layout)

    def set_status(self, text: str, is_error: bool = False, is_warning: bool = False):
        self.status_label.setText(text)
        if is_error:
            self.status_label.setStyleSheet("color: #f38ba8; font-weight: bold;")
        elif is_warning:
            self.status_label.setStyleSheet("color: #f9e2af; font-weight: bold;") # Sarı/Turuncu
        else:
            self.status_label.setStyleSheet("color: #a6e3a1; font-weight: bold;") # Yeşil


    def set_path(self, path: str):
        self.path_input.setText(path)
        self.project_changed.emit(path)

    def get_path(self) -> str:
        return self.path_input.text()

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "Git Proje Klasörünü Seçin",
            self.path_input.text() or ""
        )
        if dir_path:
            self.set_path(dir_path)
