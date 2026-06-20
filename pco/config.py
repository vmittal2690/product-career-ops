from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_DIR = ROOT / "private"
WORKBOOK_PATH = PRIVATE_DIR / "product-career-ops.xlsx"
PROFILE_PATH = PRIVATE_DIR / "profile.yml"
EVIDENCE_PATH = PRIVATE_DIR / "evidence.md"
EVIDENCE_DATA_PATH = PRIVATE_DIR / "evidence.yml"
SOURCES_PATH = PRIVATE_DIR / "sources.yml"
OUTPUT_DIR = ROOT / "outputs"
BACKUP_DIR = ROOT / "backups"
TMP_DIR = ROOT / "tmp"
LOCK_PATH = ROOT / ".pco.lock"

ACTIVE_THRESHOLD = 80

SHEET_ORDER = [
    "Dashboard",
    "Profile",
    "Career_Thesis",
    "Evidence",
    "Competencies",
    "Research_Principles",
    "Opportunities",
    "Companies",
    "Scorecards",
    "Applications",
    "Interviews",
    "Documents",
    "Outcomes",
    "Coaching_Sessions",
    "Decisions",
    "Weekly_Reviews",
    "Quarterly_Reviews",
    "Development_Experiments",
    "Prompt_Lessons",
    "Feedback",
    "History",
    "Lists",
]

SCORE_DIMENSIONS = [
    ("mandate_authority", "Mandate and decision authority", 20),
    ("target_alignment", "Target-role alignment", 15),
    ("domain_fit", "Product and clinical/domain fit", 15),
    ("leadership_scope", "Scope and organizational leadership", 15),
    ("evidence_match", "Evidence match", 10),
    ("career_growth", "Strategic career growth", 10),
    ("product_quality", "Company and product quality", 5),
    ("commercial_upside", "Commercial upside", 5),
    ("practical_fit", "Practical constraints", 5),
]

STATUSES = [
    "Inbox",
    "Active",
    "Archived",
    "Applied",
    "Interview",
    "Offer",
    "Accepted",
    "Declined",
    "Rejected",
    "Closed",
]

PRIORITIES = ["High", "Medium", "Low"]
CONFIDENTIALITY = ["Public", "Shareable", "Private", "Confidential"]
