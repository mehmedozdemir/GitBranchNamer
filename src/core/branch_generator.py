# src/core/branch_generator.py

from dataclasses import dataclass
from .normalizer import normalize_description, normalize_ticket
from .validator import validate_description, validate_ticket, validate_source_branch


@dataclass
class BranchResult:
    branch_name: str
    git_command: str
    is_valid: bool
    error: str


def generate(branch_type: str, source_branch: str, ticket: str, description: str) -> BranchResult:
    """
    Verilen girdilerden standart bir branch adı üretir.

    Args:
        branch_type:   Seçilen tip (feat, fix, hotfix, ...)
        source_branch: Kaynak branch (dev, test, preprod, master)
        ticket:        Ticket numarası — opsiyonel, boş olabilir
        description:   Kısa açıklama metni

    Returns:
        BranchResult — branch_name, git_command, is_valid, error
    """

    # Kaynak branch doğrula
    src_valid, src_err = validate_source_branch(branch_type, source_branch)
    if not src_valid:
        return BranchResult("", "", False, src_err)

    # Ticket normalize + doğrula
    normalized_ticket = normalize_ticket(ticket) if ticket.strip() else ""
    ticket_valid, ticket_err = validate_ticket(normalized_ticket)
    if not ticket_valid:
        return BranchResult("", "", False, ticket_err)

    # Açıklama normalize + doğrula
    normalized_desc = normalize_description(description)
    desc_valid, desc_err = validate_description(normalized_desc)
    if not desc_valid:
        return BranchResult("", "", False, desc_err)

    # Branch adını birleştir
    if normalized_ticket:
        branch_name = f"{branch_type}/{normalized_ticket}-{normalized_desc}"
    else:
        branch_name = f"{branch_type}/{normalized_desc}"

    git_command = f"git checkout -b {branch_name}"

    return BranchResult(branch_name, git_command, True, "")
