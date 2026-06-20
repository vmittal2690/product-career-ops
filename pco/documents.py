from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .config import OUTPUT_DIR
from .ids import utc_now
from .io import slug
from .workbook import append_record, find_record

NAVY = "#183153"
TEAL = "#2D6F73"
INK = "#202A35"
MUTED = "#667085"
CREAM = "#F6F2E9"


def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="PCOTitle", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=23, leading=27, textColor=colors.HexColor(NAVY), spaceAfter=18,
    ))
    styles.add(ParagraphStyle(
        name="PCOH1", parent=styles["Heading1"], fontName="Helvetica-Bold",
        fontSize=14, leading=18, textColor=colors.HexColor(TEAL), spaceBefore=12, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="PCOBody", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=colors.HexColor(INK), alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="PCOMeta", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=8.5, leading=11, textColor=colors.HexColor(MUTED),
    ))
    return styles


def _safe(value: Any) -> str:
    return html.escape(str(value or "")).replace("\n", "<br/>")


def _sections_from_payload(payload: dict[str, Any]) -> list[tuple[str, str]]:
    preferred = [
        ("Executive recommendation", "recommendation"),
        ("Role and mandate", "role_brief"),
        ("Company and product", "company_brief"),
        ("Evidence match", "evidence_match"),
        ("Gaps and risks", "gaps_risks"),
        ("Diligence questions", "diligence_questions"),
        ("Interview preparation", "interview_packet"),
        ("Outreach draft", "outreach"),
        ("Cover letter", "cover_letter"),
        ("Tailored resume", "resume"),
    ]
    sections = []
    for title, key in preferred:
        value = payload.get(key)
        if value:
            sections.append((title, str(value)))
    return sections


def build_packet(opportunity_id: str, payload: dict[str, Any]) -> dict[str, str]:
    opportunity = find_record("Opportunities", opportunity_id)
    if not opportunity:
        raise ValueError(f"Unknown opportunity: {opportunity_id}")

    packet_dir = OUTPUT_DIR / "search" / opportunity_id
    packet_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{opportunity_id}-{slug(str(opportunity['Company']))}-{slug(str(opportunity['Role']))}"
    html_path = packet_dir / f"{filename}.html"
    pdf_path = packet_dir / f"{filename}.pdf"

    sections = _sections_from_payload(payload)
    html_sections = "".join(
        f"<section><h2>{html.escape(title)}</h2><div class='prose'>{_safe(body)}</div></section>"
        for title, body in sections
    )
    html_doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(filename)}</title>
<style>
@page {{ size: letter; margin: 0.65in; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; color: {INK}; font-family: Arial, Helvetica, sans-serif; line-height: 1.48; }}
header {{ border-top: 10px solid {NAVY}; padding: 28px 0 18px; border-bottom: 2px solid {TEAL}; }}
.eyebrow {{ color: {TEAL}; font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }}
h1 {{ color: {NAVY}; font-family: Georgia, serif; font-size: 30px; line-height: 1.1; margin: 8px 0; }}
.meta {{ color: {MUTED}; font-size: 12px; }}
main {{ max-width: 820px; margin: 0 auto; }}
section {{ padding: 18px 0; border-bottom: 1px solid #d9e2e8; break-inside: avoid; }}
h2 {{ color: {TEAL}; font-family: Georgia, serif; font-size: 18px; margin: 0 0 9px; }}
.prose {{ white-space: normal; font-size: 13px; }}
.score {{ display: inline-block; color: white; background: {TEAL}; padding: 5px 9px; border-radius: 2px; font-weight: 700; }}
footer {{ margin-top: 24px; padding: 12px; background: {CREAM}; color: {MUTED}; font-size: 10px; }}
</style>
</head>
<body><main>
<header>
<div class="eyebrow">Product Career Ops - Search Packet</div>
<h1>{html.escape(str(opportunity['Company']))}<br>{html.escape(str(opportunity['Role']))}</h1>
<div class="meta">{html.escape(opportunity_id)} &nbsp; | &nbsp; <span class="score">{opportunity['Score_100']}/100</span></div>
</header>
{html_sections}
<footer>Generated {utc_now()}. Claims must remain grounded in the approved evidence bank.</footer>
</main></body></html>"""
    html_path.write_text(html_doc, encoding="utf-8")

    styles = _styles()
    story = [
        Paragraph("PRODUCT CAREER OPS", styles["PCOMeta"]),
        Paragraph(f"{opportunity['Company']} - {opportunity['Role']}", styles["PCOTitle"]),
        Paragraph(f"{opportunity_id} | {opportunity['Score_100']}/100 | {opportunity['Recommendation']}", styles["PCOMeta"]),
        Spacer(1, 0.16 * inch),
    ]
    for index, (title, body) in enumerate(sections):
        if index and index % 4 == 0:
            story.append(PageBreak())
        story.append(Paragraph(title, styles["PCOH1"]))
        for paragraph in str(body).split("\n\n"):
            story.append(Paragraph(_safe(paragraph), styles["PCOBody"]))
            story.append(Spacer(1, 0.08 * inch))

    doc = SimpleDocTemplate(
        str(pdf_path), pagesize=letter, rightMargin=0.65 * inch, leftMargin=0.65 * inch,
        topMargin=0.58 * inch, bottomMargin=0.58 * inch,
        title=f"{opportunity['Company']} - {opportunity['Role']}",
    )
    doc.build(story)

    document_id = append_record("Documents", {
        "Opportunity_ID": opportunity_id,
        "Type": "Complete Search Packet",
        "Version": 1,
        "HTML_Path": str(html_path.relative_to(OUTPUT_DIR.parent)),
        "PDF_Path": str(pdf_path.relative_to(OUTPUT_DIR.parent)),
        "Created_At": utc_now(),
        "Evidence_Check": payload.get("evidence_check", "Agent-confirmed"),
        "Notes": payload.get("notes", ""),
    })
    return {"document_id": document_id, "html": str(html_path), "pdf": str(pdf_path)}


def build_review(kind: str, review_id: str, payload: dict[str, Any]) -> dict[str, str]:
    review_dir = OUTPUT_DIR / "development" / kind
    review_dir.mkdir(parents=True, exist_ok=True)
    base = f"{review_id}-{slug(payload.get('period', payload.get('quarter', 'review')))}"
    html_path = review_dir / f"{base}.html"
    pdf_path = review_dir / f"{base}.pdf"
    sections = [(key.replace("_", " ").title(), str(value)) for key, value in payload.items() if value]
    html_body = "".join(f"<h2>{html.escape(k)}</h2><p>{_safe(v)}</p>" for k, v in sections)
    html_path.write_text(
        f"""<!doctype html><html><head><meta charset="utf-8"><style>
        @page {{size: letter; margin: .7in}} body{{font:14px/1.5 Arial;color:{INK};max-width:820px;margin:auto}}
        h1{{font:30px Georgia;color:{NAVY};border-bottom:3px solid {TEAL};padding-bottom:14px}}
        h2{{font:19px Georgia;color:{TEAL};margin-top:24px}} p{{white-space:normal}}
        </style></head><body><h1>Product Leadership {kind.title()} Review</h1>{html_body}</body></html>""",
        encoding="utf-8",
    )
    styles = _styles()
    story = [Paragraph(f"Product Leadership {kind.title()} Review", styles["PCOTitle"])]
    for title, body in sections:
        story.extend([Paragraph(title, styles["PCOH1"]), Paragraph(_safe(body), styles["PCOBody"])])
    SimpleDocTemplate(str(pdf_path), pagesize=letter).build(story)
    return {"html": str(html_path), "pdf": str(pdf_path)}

