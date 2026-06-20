from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import yaml

from .config import (
    EVIDENCE_PATH,
    EVIDENCE_DATA_PATH,
    OUTPUT_DIR,
    PRIVATE_DIR,
    PROFILE_PATH,
    ROOT,
    SCORE_DIMENSIONS,
    SOURCES_PATH,
    WORKBOOK_PATH,
)
from .documents import build_packet, build_review
from .ids import utc_now
from .io import dump_json, load_json
from .privacy import export_public
from .scanner import scan
from .scoring import parse_scores, recommendation_for_score, status_for_score, total
from .workbook import (
    append_record,
    counts,
    create_workbook,
    find_record,
    read_rows,
    validate_workbook,
)


def _print_menu() -> None:
    print(
        """Product Career Ops

Job Search
  Evaluate an exciting role and decide whether to pursue it
  /pco search <URL or pasted JD>

Development
  Strengthen product judgment, leadership capability, and career evidence
  /pco develop
"""
    )


def _seed_profile() -> None:
    if not PROFILE_PATH.exists():
        return
    profile = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8")) or {}
    flat = {
        "Full Name": profile.get("candidate", {}).get("full_name", ""),
        "Location": profile.get("candidate", {}).get("location", ""),
        "Current Company": profile.get("candidate", {}).get("current_company", ""),
        "Current Title": profile.get("candidate", {}).get("current_title", ""),
        "Experience": profile.get("candidate", {}).get("experience_years", ""),
        "LinkedIn": profile.get("candidate", {}).get("linkedin", ""),
        "Headline": profile.get("narrative", {}).get("headline", ""),
        "Career Thesis": profile.get("narrative", {}).get("career_thesis", ""),
        "Target Roles": ", ".join(profile.get("target_roles", [])),
        "Differentiators": "; ".join(profile.get("narrative", {}).get("differentiators", [])),
        "Domains": "; ".join(profile.get("domains", [])),
        "Core Capabilities": "; ".join(profile.get("core_capabilities", [])),
        "Updated At": utc_now(),
    }
    existing = read_rows("Profile")
    if existing:
        return
    for key, value in flat.items():
        append_record("Profile", {"Key": key, "Value": value, "Updated_At": utc_now()})


def _seed_evidence() -> None:
    if not EVIDENCE_DATA_PATH.exists() or read_rows("Evidence"):
        return
    records = yaml.safe_load(EVIDENCE_DATA_PATH.read_text(encoding="utf-8")) or []
    for data in records:
        append_record("Evidence", {
            "Date": data.get("date", ""),
            "Context": data.get("context", ""),
            "Problem": data.get("problem", ""),
            "Role": data.get("role", ""),
            "Actions": data.get("actions", ""),
            "Result": data.get("result", ""),
            "Metrics": data.get("metrics", ""),
            "Stakeholders": data.get("stakeholders", ""),
            "Tradeoffs": data.get("tradeoffs", ""),
            "Reflection": data.get("reflection", ""),
            "Competencies": data.get("competencies", ""),
            "Confidentiality": data.get("confidentiality", "Private"),
            "Source": data.get("source", "Resume"),
            "Updated_At": utc_now(),
        }, summary=f"Seed evidence: {data.get('context', '')}")


def cmd_init(_: argparse.Namespace) -> None:
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not WORKBOOK_PATH.exists():
        create_workbook()
    validate_workbook()
    _seed_profile()
    _seed_evidence()
    print(WORKBOOK_PATH)


def cmd_reset(args: argparse.Namespace) -> None:
    if args.confirm != "RESET":
        raise ValueError("Refusing reset. Pass --confirm RESET.")
    create_workbook(WORKBOOK_PATH)
    _seed_profile()
    _seed_evidence()
    print(WORKBOOK_PATH)


def cmd_demo_init(args: argparse.Namespace) -> None:
    demo_dir = ROOT / "demo"
    if not demo_dir.exists():
        raise FileNotFoundError("Demo data directory is missing")
    if PRIVATE_DIR.exists() and any(PRIVATE_DIR.iterdir()) and not args.force:
        raise ValueError(
            "Refusing to overwrite existing private career data. "
            "Use --force only if you intend to replace it with fictional demo data."
        )
    PRIVATE_DIR.mkdir(parents=True, exist_ok=True)
    for source_name, target_name in (
        ("profile.yml", "profile.yml"),
        ("resume.md", "resume.md"),
        ("evidence.yml", "evidence.yml"),
        ("sources.yml", "sources.yml"),
    ):
        shutil.copy2(demo_dir / source_name, PRIVATE_DIR / target_name)
    evidence_md = PRIVATE_DIR / "evidence.md"
    evidence_records = yaml.safe_load((demo_dir / "evidence.yml").read_text(encoding="utf-8")) or []
    lines = ["# Fictional Demo Evidence Bank", "", "All records below are invented demonstration data.", ""]
    for item in evidence_records:
        lines.extend([
            f"## {item.get('context', 'Evidence')}",
            "",
            f"- **Role:** {item.get('role', '')}",
            f"- **Problem:** {item.get('problem', '')}",
            f"- **Actions:** {item.get('actions', '')}",
            f"- **Result:** {item.get('result', '')}",
            f"- **Metrics:** {item.get('metrics', '')}",
            "",
        ])
    evidence_md.write_text("\n".join(lines), encoding="utf-8")
    create_workbook(WORKBOOK_PATH)
    _seed_profile()
    _seed_evidence()
    print(WORKBOOK_PATH)
    print("Fictional demo initialized. Add roles from demo/opportunities/ to populate the tracker.")


def cmd_doctor(_: argparse.Namespace) -> None:
    checks = {
        "workbook_exists": WORKBOOK_PATH.exists(),
        "profile_exists": PROFILE_PATH.exists(),
        "evidence_exists": EVIDENCE_PATH.exists(),
        "sources_exists": SOURCES_PATH.exists(),
        "skill_exists": (ROOT / ".agents/skills/pco/SKILL.md").exists(),
        "agent_contract_exists": (ROOT / "AGENTS.md").exists(),
    }
    if checks["workbook_exists"]:
        try:
            validate_workbook()
            checks["workbook_valid"] = True
        except Exception as exc:
            checks["workbook_valid"] = False
            checks["workbook_error"] = str(exc)
    print(dump_json(checks))
    if not all(value for key, value in checks.items() if key != "workbook_error"):
        raise SystemExit(1)


def cmd_opportunity_add(args: argparse.Namespace) -> None:
    data = load_json(args.input)
    scores = parse_scores(data["scores"])
    score_total = total(scores)
    opportunity = data["opportunity"]
    status = status_for_score(score_total)
    opportunity_id = append_record("Opportunities", {
        "Added_At": utc_now(),
        "Company": opportunity["company"],
        "Role": opportunity["role"],
        "URL": opportunity.get("url", ""),
        "Source": opportunity.get("source", "Manual"),
        "Location": opportunity.get("location", ""),
        "Work_Model": opportunity.get("work_model", ""),
        "Status": status,
        "Priority": opportunity.get("priority", "High" if score_total >= 90 else "Medium"),
        "Score_100": score_total,
        "Recommendation": data.get("recommendation", recommendation_for_score(score_total)),
        "Archetype": data.get("archetype", ""),
        "Posting_Status": data.get("posting_status", "Unconfirmed"),
        "Next_Action": data.get("next_action", ""),
        "Next_Action_Date": data.get("next_action_date", ""),
        "Report_Path": data.get("report_path", ""),
        "Notes": data.get("notes", ""),
        "Updated_At": utc_now(),
    }, summary=f"Added {opportunity['company']} - {opportunity['role']} ({score_total}/100)")
    for score in scores:
        append_record("Scorecards", {
            "Opportunity_ID": opportunity_id,
            "Dimension": score.label,
            "Max_Points": score.maximum,
            "Points": score.points,
            "Rationale": score.rationale,
            "Evidence": score.evidence,
            "Unknowns": score.unknowns,
            "Created_At": utc_now(),
        })
    print(dump_json({"opportunity_id": opportunity_id, "score": score_total, "status": status}))


def cmd_opportunity_list(args: argparse.Namespace) -> None:
    rows = read_rows("Opportunities")
    if args.status:
        rows = [row for row in rows if row["Status"] == args.status]
    if args.json:
        print(dump_json(rows))
        return
    if not rows:
        print("No opportunities.")
        return
    for row in rows:
        print(
            f"{row['Opportunity_ID']}  {row['Score_100']:>3}/100  "
            f"{row['Status']:<10}  {row['Company']} - {row['Role']}"
        )


def cmd_packet_build(args: argparse.Namespace) -> None:
    payload = load_json(args.input)
    print(dump_json(build_packet(args.id, payload)))


def cmd_coach_add(args: argparse.Namespace) -> None:
    data = load_json(args.input)
    required = ["topic", "situation", "initial_recommendation", "human_judgment"]
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise ValueError("Coaching record missing: " + ", ".join(missing))
    coaching_id = append_record("Coaching_Sessions", {
        "Date": data.get("date", utc_now()[:10]),
        "Topic": data["topic"],
        "Situation": data["situation"],
        "Decision": data.get("decision", ""),
        "Stakeholders": data.get("stakeholders", ""),
        "Constraints": data.get("constraints", ""),
        "Evidence": data.get("evidence", ""),
        "Uncertainty": data.get("uncertainty", ""),
        "Desired_Outcome": data.get("desired_outcome", ""),
        "Initial_Recommendation": data["initial_recommendation"],
        "Useful": data.get("useful", ""),
        "Weak": data.get("weak", ""),
        "Unsupported_Assumptions": data.get("unsupported_assumptions", ""),
        "Missing_Context": data.get("missing_context", ""),
        "Risks": data.get("risks", ""),
        "Refined_Question": data.get("refined_question", ""),
        "Refined_Response": data.get("refined_response", ""),
        "Human_Judgment": data["human_judgment"],
        "Final_Decision": data.get("final_decision", ""),
        "Confidence": data.get("confidence", ""),
        "Next_Action": data.get("next_action", ""),
        "Review_Date": data.get("review_date", ""),
        "Prompt_Lesson": data.get("prompt_lesson", ""),
    }, summary=f"Coaching: {data['topic']}")
    decision_id = ""
    if data.get("final_decision"):
        decision_id = append_record("Decisions", {
            "Coaching_ID": coaching_id,
            "Date": data.get("date", utc_now()[:10]),
            "Decision": data["final_decision"],
            "Rationale": data.get("rationale", ""),
            "Alternatives": data.get("alternatives", ""),
            "Dissent": data.get("dissent", ""),
            "Confidence": data.get("confidence", ""),
            "Next_Action": data.get("next_action", ""),
            "Review_Date": data.get("review_date", ""),
            "Outcome": "",
        }, summary=f"Decision from {coaching_id}")
    if data.get("prompt_lesson"):
        append_record("Prompt_Lessons", {
            "Date": data.get("date", utc_now()[:10]),
            "Context": data["topic"],
            "Original_Question": data.get("original_question", ""),
            "Problem": data.get("weak", ""),
            "Improved_Question": data.get("refined_question", ""),
            "Lesson": data["prompt_lesson"],
        }, summary=f"Prompt lesson from {coaching_id}")
    print(dump_json({"coaching_id": coaching_id, "decision_id": decision_id}))


def cmd_weekly(args: argparse.Namespace) -> None:
    data = load_json(args.input)
    review_id = append_record("Weekly_Reviews", {
        "Week_Ending": data["week_ending"],
        "Decisions": data.get("decisions", ""),
        "Shipped_Learned_Influenced": data.get("shipped_learned_influenced", ""),
        "Feedback": data.get("feedback", ""),
        "Evidence_Candidates": data.get("evidence_candidates", ""),
        "AI_Helped": data.get("ai_helped", ""),
        "AI_Misled": data.get("ai_misled", ""),
        "Next_Week": data.get("next_week", ""),
        "Document_Path": "",
        "Created_At": utc_now(),
    }, summary=f"Weekly review ending {data['week_ending']}")
    paths = build_review("weekly", review_id, {**data, "period": data["week_ending"]})
    print(dump_json({"review_id": review_id, **paths}))


def cmd_quarterly(args: argparse.Namespace) -> None:
    data = load_json(args.input)
    paths = build_review("quarterly", "pending", data)
    review_id = append_record("Quarterly_Reviews", {
        "Quarter": data["quarter"],
        "Career_Direction": data.get("career_direction", ""),
        "Competency_Growth": data.get("competency_growth", ""),
        "Strengths": data.get("strengths", ""),
        "Blind_Spots": data.get("blind_spots", ""),
        "Decision_Quality": data.get("decision_quality", ""),
        "Evidence_Implications": data.get("evidence_implications", ""),
        "Market_Feedback": data.get("market_feedback", ""),
        "Next_Quarter_Bets": data.get("next_quarter_bets", ""),
        "HTML_Path": str(Path(paths["html"]).relative_to(ROOT)),
        "PDF_Path": str(Path(paths["pdf"]).relative_to(ROOT)),
        "Created_At": utc_now(),
    }, summary=f"Quarterly review {data['quarter']}")
    print(dump_json({"review_id": review_id, **paths}))


def cmd_evidence_add(args: argparse.Namespace) -> None:
    data = load_json(args.input)
    evidence_id = append_record("Evidence", {
        "Date": data.get("date", utc_now()[:10]),
        "Context": data.get("context", ""),
        "Problem": data.get("problem", ""),
        "Role": data.get("role", ""),
        "Actions": data.get("actions", ""),
        "Result": data.get("result", ""),
        "Metrics": data.get("metrics", ""),
        "Stakeholders": data.get("stakeholders", ""),
        "Tradeoffs": data.get("tradeoffs", ""),
        "Reflection": data.get("reflection", ""),
        "Competencies": data.get("competencies", ""),
        "Confidentiality": data.get("confidentiality", "Private"),
        "Source": data.get("source", "User confirmed"),
        "Updated_At": utc_now(),
    }, summary=f"Evidence: {data.get('context', '')}")
    print(evidence_id)


def cmd_scan(_: argparse.Namespace) -> None:
    print(dump_json(scan()))


def cmd_export_public(args: argparse.Namespace) -> None:
    destination = Path(args.destination or ROOT / "public-export")
    print(export_public(destination))


def cmd_counts(_: argparse.Namespace) -> None:
    print(dump_json(counts()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pco")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("menu").set_defaults(func=lambda _: _print_menu())
    sub.add_parser("init").set_defaults(func=cmd_init)
    reset = sub.add_parser("reset")
    reset.add_argument("--confirm", required=True)
    reset.set_defaults(func=cmd_reset)
    demo_init = sub.add_parser("demo-init")
    demo_init.add_argument("--force", action="store_true")
    demo_init.set_defaults(func=cmd_demo_init)
    sub.add_parser("doctor").set_defaults(func=cmd_doctor)
    sub.add_parser("counts").set_defaults(func=cmd_counts)

    opportunity = sub.add_parser("opportunity")
    opp_sub = opportunity.add_subparsers(dest="opportunity_command", required=True)
    add = opp_sub.add_parser("add")
    add.add_argument("--input", required=True)
    add.set_defaults(func=cmd_opportunity_add)
    ls = opp_sub.add_parser("list")
    ls.add_argument("--status")
    ls.add_argument("--json", action="store_true")
    ls.set_defaults(func=cmd_opportunity_list)

    packet = sub.add_parser("packet")
    packet_sub = packet.add_subparsers(dest="packet_command", required=True)
    packet_build = packet_sub.add_parser("build")
    packet_build.add_argument("--id", required=True)
    packet_build.add_argument("--input", required=True)
    packet_build.set_defaults(func=cmd_packet_build)

    coach = sub.add_parser("coach")
    coach_sub = coach.add_subparsers(dest="coach_command", required=True)
    coach_add = coach_sub.add_parser("add")
    coach_add.add_argument("--input", required=True)
    coach_add.set_defaults(func=cmd_coach_add)

    review = sub.add_parser("review")
    review_sub = review.add_subparsers(dest="review_command", required=True)
    weekly = review_sub.add_parser("weekly")
    weekly.add_argument("--input", required=True)
    weekly.set_defaults(func=cmd_weekly)
    quarterly = review_sub.add_parser("quarterly")
    quarterly.add_argument("--input", required=True)
    quarterly.set_defaults(func=cmd_quarterly)

    evidence = sub.add_parser("evidence")
    ev_sub = evidence.add_subparsers(dest="evidence_command", required=True)
    ev_add = ev_sub.add_parser("add")
    ev_add.add_argument("--input", required=True)
    ev_add.set_defaults(func=cmd_evidence_add)

    sub.add_parser("scan").set_defaults(func=cmd_scan)
    export = sub.add_parser("export-public")
    export.add_argument("--destination")
    export.set_defaults(func=cmd_export_public)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not getattr(args, "command", None):
        _print_menu()
        return
    try:
        args.func(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
