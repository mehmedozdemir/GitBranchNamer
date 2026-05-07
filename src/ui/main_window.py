# src/ui/main_window.py

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QSettings
from src.ui.components.project_selector import ProjectSelector
from src.ui.components.branch_form import BranchForm
from src.ui.components.preview_box import PreviewBox
from src.ui.components.copy_button import CopyButtons
from src.core.branch_generator import generate
from src.core.git_service import get_git_status

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Branch Generator")
        self.setFixedSize(550, 480)
        
        self.settings = QSettings("GitBranchNamer", "Settings")
        self.is_git_clean = False
        
        self.setup_ui()
        self.connect_signals()
        self.load_settings()
        
        # İlk güncellemeyi tetikle (hata mesajını göstermesi için)
        self.on_branch_changed(
            self.form.type_combo.currentText(),
            self.form.source_combo.currentText(),
            self.form.ticket_input.text(),
            self.form.desc_input.text()
        )

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(24)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.project_selector = ProjectSelector()
        self.form = BranchForm()
        self.preview = PreviewBox()
        self.buttons = CopyButtons()
        
        layout.addWidget(self.project_selector)
        layout.addWidget(self.form)
        layout.addWidget(self.preview)
        layout.addStretch() # Aradaki boşluğu doldur
        layout.addWidget(self.buttons)
        
        central_widget.setLayout(layout)

    def connect_signals(self):
        self.form.branch_changed.connect(self.on_branch_changed)
        self.project_selector.project_changed.connect(self.on_project_changed)

    def load_settings(self):
        saved_path = self.settings.value("last_project_path", "")
        if saved_path:
            self.project_selector.set_path(saved_path)
            self.on_project_changed(saved_path) # Durumu başlangıçta kontrol et

    def on_project_changed(self, path: str):
        self.settings.setValue("last_project_path", path)
        
        if not path:
            self.project_selector.set_status("Git Durumu: Proje seçilmedi")
            self.is_git_clean = False
        else:
            status = get_git_status(path)
            if not status.is_repo:
                self.project_selector.set_status(f"Git Durumu: {status.error or 'Geçerli bir repo değil'}", is_error=True)
                self.is_git_clean = False
            else:
                if status.uncommitted_count > 0:
                    self.project_selector.set_status(f"⚠️ Aktif: {status.active_branch} ({status.uncommitted_count} uncommitted dosya)", is_warning=True)
                    self.is_git_clean = False
                else:
                    self.project_selector.set_status(f"🌿 Aktif: {status.active_branch} (Temiz)", is_error=False, is_warning=False)
                    self.is_git_clean = True
                    
        # Butonların durumunu güncellemek için mevcut form verileriyle tekrar tetikle
        self.on_branch_changed(
            self.form.type_combo.currentText(),
            self.form.source_combo.currentText(),
            self.form.ticket_input.text(),
            self.form.desc_input.text()
        )

    def on_branch_changed(self, branch_type: str, source_branch: str, ticket: str, description: str):
        # İş mantığı (core) çağrısı
        result = generate(branch_type, source_branch, ticket, description)
        
        project_path = self.project_selector.get_path()
        
        # Önizleme ve butonları güncelle
        self.preview.update_preview(result.branch_name, result.is_valid, result.error)
        self.buttons.update_state(result.branch_name, result.git_command, result.is_valid, project_path, self.is_git_clean)
