# src/core/git_service.py

import subprocess
import os
from dataclasses import dataclass

@dataclass
class GitStatus:
    is_repo: bool
    active_branch: str
    uncommitted_count: int
    error: str = ""

def get_git_status(repo_path: str) -> GitStatus:
    """
    Belirtilen dizindeki Git repo durumunu döndürür.
    Aktif branch'i ve commit edilmemiş değişiklik sayısını içerir.
    """
    if not repo_path or not os.path.exists(repo_path):
        return GitStatus(is_repo=False, active_branch="", uncommitted_count=0)
        
    git_dir = os.path.join(repo_path, ".git")
    if not os.path.isdir(git_dir):
        # Worktree vb. durumlar için tam kontrol yapılabilir ama şimdilik .git klasörü yeterli
        return GitStatus(is_repo=False, active_branch="", uncommitted_count=0)

    try:
        # Get active branch
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=repo_path, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        active_branch = branch_result.stdout.strip()

        # Get uncommitted files count
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=repo_path, capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        lines = [line for line in status_result.stdout.split('\n') if line.strip()]
        uncommitted_count = len(lines)

        return GitStatus(is_repo=True, active_branch=active_branch, uncommitted_count=uncommitted_count)

    except subprocess.CalledProcessError as e:
        return GitStatus(is_repo=False, active_branch="", uncommitted_count=0, error="Git komutu başarısız oldu.")
    except FileNotFoundError:
        return GitStatus(is_repo=False, active_branch="", uncommitted_count=0, error="Git kurulu değil veya bulunamadı.")
