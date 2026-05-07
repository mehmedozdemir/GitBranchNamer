# src/ui/components/copy_button.py

import os
import subprocess
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
from src.utils.clipboard import copy_to_clipboard

class CopyButtons(QWidget):
    def __init__(self):
        super().__init__()
        self.current_branch = ""
        self.current_command = ""
        self.project_path = ""
        self.is_valid = False
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.btn_copy_branch = QPushButton("Adı Kopyala")
        self.btn_copy_branch.clicked.connect(self.copy_branch)
        
        self.btn_copy_command = QPushButton("Komutu Kopyala")
        self.btn_copy_command.clicked.connect(self.copy_command)
        
        self.btn_create_branch = QPushButton("Branch Oluştur")
        self.btn_create_branch.clicked.connect(self.create_branch)
        
        layout.addWidget(self.btn_copy_branch)
        layout.addWidget(self.btn_copy_command)
        layout.addWidget(self.btn_create_branch)
        self.setLayout(layout)
        self.update_state("", "", False, "")

    def update_state(self, branch_name: str, git_command: str, is_valid: bool, project_path: str, is_git_clean: bool = False):
        self.current_branch = branch_name
        self.current_command = git_command
        self.is_valid = is_valid
        self.project_path = project_path
        
        self.btn_copy_branch.setEnabled(is_valid)
        self.btn_copy_command.setEnabled(is_valid)
        self.btn_create_branch.setEnabled(is_valid and is_git_clean)

    def copy_branch(self):
        if self.is_valid and self.current_branch:
            copy_to_clipboard(self.current_branch)
            self.show_feedback(self.btn_copy_branch, "Adı Kopyala")

    def copy_command(self):
        if self.is_valid and self.current_command:
            copy_to_clipboard(self.current_command)
            self.show_feedback(self.btn_copy_command, "Komutu Kopyala")

    def create_branch(self):
        if self.is_valid and self.current_command:
            if not self.project_path:
                QMessageBox.warning(self, "Uyarı", "Lütfen önce 'Hedef Proje' alanından bir git projesi seçin.")
                return
                
            if not os.path.exists(os.path.join(self.project_path, ".git")):
                QMessageBox.warning(self, "Uyarı", "Seçilen klasör geçerli bir Git deposu (.git klasörü) içermiyor!")
                return
                
            try:
                result = subprocess.run(self.current_command, shell=True, capture_output=True, text=True, cwd=self.project_path)
                if result.returncode == 0:
                    self.show_feedback(self.btn_create_branch, "Branch Oluştur")
                    QMessageBox.information(self, "Başarılı", f"Branch başarıyla oluşturuldu ve geçiş yapıldı:\n{self.current_branch}")
                else:
                    error_msg = result.stderr if result.stderr else result.stdout
                    QMessageBox.warning(self, "Hata", f"Branch oluşturulamadı:\n{error_msg}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Komut çalıştırılırken bir hata oluştu:\n{str(e)}")

    def show_feedback(self, button: QPushButton, original_text: str):
        button.setText("✓ İşlem Başarılı!")
        button.setProperty("state", "success")
        button.style().unpolish(button)
        button.style().polish(button)
        
        # 2 saniye sonra geri al
        QTimer.singleShot(2000, lambda: self.reset_button(button, original_text))

    def reset_button(self, button: QPushButton, original_text: str):
        button.setText(original_text)
        button.setProperty("state", "")
        button.style().unpolish(button)
        button.style().polish(button)
