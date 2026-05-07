# src/ui/components/branch_form.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit
from PyQt6.QtCore import pyqtSignal, Qt
from src.core.constants import BRANCH_TYPES

class BranchForm(QWidget):
    # Formdaki herhangi bir alan değiştiğinde tetiklenir
    branch_changed = pyqtSignal(str, str, str, str) # type, source, ticket, description

    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(0, 0, 0, 15)
        
        # Branch Tipi
        type_layout = QHBoxLayout()
        type_label = QLabel("Branch Tipi:")
        type_label.setFixedWidth(100)
        self.type_combo = QComboBox()
        self.type_combo.addItems(list(BRANCH_TYPES.keys()))
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        
        # Kaynak Branch
        source_layout = QHBoxLayout()
        source_label = QLabel("Kaynak Branch:")
        source_label.setFixedWidth(100)
        self.source_combo = QComboBox()
        self.source_combo.currentTextChanged.connect(self.emit_changed)
        source_layout.addWidget(source_label)
        source_layout.addWidget(self.source_combo)
        
        # Ticket No
        ticket_layout = QHBoxLayout()
        ticket_label = QLabel("Ticket No:")
        ticket_label.setFixedWidth(100)
        self.ticket_input = QLineEdit()
        self.ticket_input.setPlaceholderText("PRJ-123 (opsiyonel)")
        self.ticket_input.textChanged.connect(self.emit_changed)
        ticket_layout.addWidget(ticket_label)
        ticket_layout.addWidget(self.ticket_input)
        
        # Açıklama
        desc_layout = QHBoxLayout()
        desc_label = QLabel("Açıklama:")
        desc_label.setFixedWidth(100)
        
        desc_input_layout = QVBoxLayout()
        desc_input_layout.setSpacing(4)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("kısa açıklama")
        self.desc_input.textChanged.connect(self.on_desc_changed)
        
        self.char_counter = QLabel("0/50")
        self.char_counter.setObjectName("char_counter")
        
        desc_input_layout.addWidget(self.desc_input)
        desc_input_layout.addWidget(self.char_counter, alignment=Qt.AlignmentFlag.AlignRight)
        
        desc_layout.addWidget(desc_label, alignment=Qt.AlignmentFlag.AlignTop)
        desc_layout.addLayout(desc_input_layout)
        
        # Layouts add
        layout.addLayout(type_layout)
        layout.addLayout(source_layout)
        layout.addLayout(ticket_layout)
        layout.addLayout(desc_layout)
        
        self.setLayout(layout)
        
        # İlk filtrelemeyi yap
        self.on_type_changed(self.type_combo.currentText())

    def on_type_changed(self, branch_type: str):
        self.source_combo.blockSignals(True)
        self.source_combo.clear()
        allowed_sources = BRANCH_TYPES.get(branch_type, [])
        self.source_combo.addItems(allowed_sources)
        self.source_combo.blockSignals(False)
        self.emit_changed()

    def on_desc_changed(self, text: str):
        length = len(text)
        self.char_counter.setText(f"{length}/50")
        if length > 50:
            self.char_counter.setStyleSheet("color: #f38ba8;") # Kırmızı
        else:
            self.char_counter.setStyleSheet("color: #cdd6f4;") # Normal metin rengi
        self.emit_changed()

    def emit_changed(self):
        self.branch_changed.emit(
            self.type_combo.currentText(),
            self.source_combo.currentText(),
            self.ticket_input.text(),
            self.desc_input.text()
        )
