from pathlib import Path

from pco import privacy
from pco.privacy import scan_private


def test_privacy_detects_email(tmp_path: Path):
    email = "jane" + "@" + "example.com"
    (tmp_path / "file.txt").write_text(f"contact {email}", encoding="utf-8")
    assert scan_private(tmp_path)


def test_privacy_allows_synthetic_text(tmp_path: Path):
    (tmp_path / "file.txt").write_text("Example Product Leader", encoding="utf-8")
    assert scan_private(tmp_path) == []


def test_public_export_does_not_copy_itself(tmp_path: Path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "README.md").write_text("Safe public project", encoding="utf-8")
    (root / "docs").mkdir()
    (root / "docs" / "PUBLIC_README.md").write_text("Public demo README", encoding="utf-8")
    (root / "private").mkdir()
    (root / "private" / "profile.yml").write_text("private", encoding="utf-8")
    (root / "outputs").mkdir()
    (root / "outputs" / "job-packet.md").write_text("private output", encoding="utf-8")
    monkeypatch.setattr(privacy, "ROOT", root)
    destination = root / "public-export"
    privacy.export_public(destination)
    assert (destination / "README.md").exists()
    assert (destination / "README.md").read_text(encoding="utf-8") == "Public demo README"
    assert not (destination / "private").exists()
    assert not (destination / "outputs").exists()
    assert not (destination / "public-export").exists()
