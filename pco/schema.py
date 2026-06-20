from __future__ import annotations

from dataclasses import dataclass

SHEETS: dict[str, list[str]] = {
    "Profile": ["Key", "Value", "Updated_At"],
    "Career_Thesis": ["Thesis_ID", "Statement", "Status", "Evidence", "Updated_At"],
    "Evidence": [
        "Evidence_ID", "Date", "Context", "Problem", "Role", "Actions", "Result",
        "Metrics", "Stakeholders", "Tradeoffs", "Reflection", "Competencies",
        "Confidentiality", "Source", "Updated_At",
    ],
    "Competencies": [
        "Competency_ID", "Competency", "Category", "Current_Level", "Target_Level",
        "Evidence_Strength", "Gap_Type", "Notes", "Updated_At",
    ],
    "Research_Principles": ["Principle_ID", "Principle", "Source", "URL", "Accessed", "Notes"],
    "Opportunities": [
        "Opportunity_ID", "Added_At", "Company", "Role", "URL", "Source",
        "Location", "Work_Model", "Status", "Priority", "Score_100",
        "Recommendation", "Archetype", "Posting_Status", "Next_Action",
        "Next_Action_Date", "Report_Path", "Notes", "Updated_At",
    ],
    "Companies": [
        "Company_ID", "Company", "Domain", "Stage", "Product", "Leadership",
        "Market_Thesis", "Risks", "Source_URLs", "Researched_At",
    ],
    "Scorecards": [
        "Scorecard_ID", "Opportunity_ID", "Dimension", "Max_Points", "Points",
        "Rationale", "Evidence", "Unknowns", "Created_At",
    ],
    "Applications": [
        "Application_ID", "Opportunity_ID", "Applied_At", "Channel", "Referral",
        "Resume_Path", "Cover_Letter_Path", "Status", "Notes", "Updated_At",
    ],
    "Interviews": [
        "Interview_ID", "Opportunity_ID", "Round", "Audience", "Scheduled_At",
        "Topics", "Packet_Path", "Feedback", "Result", "Updated_At",
    ],
    "Documents": [
        "Document_ID", "Opportunity_ID", "Type", "Version", "HTML_Path", "PDF_Path",
        "Created_At", "Evidence_Check", "Notes",
    ],
    "Outcomes": [
        "Outcome_ID", "Opportunity_ID", "Outcome", "Date", "Market_Feedback",
        "Development_Implication", "Notes",
    ],
    "Coaching_Sessions": [
        "Coaching_ID", "Date", "Topic", "Situation", "Decision", "Stakeholders",
        "Constraints", "Evidence", "Uncertainty", "Desired_Outcome",
        "Initial_Recommendation", "Useful", "Weak", "Unsupported_Assumptions",
        "Missing_Context", "Risks", "Refined_Question", "Refined_Response",
        "Human_Judgment", "Final_Decision", "Confidence", "Next_Action",
        "Review_Date", "Prompt_Lesson",
    ],
    "Decisions": [
        "Decision_ID", "Coaching_ID", "Date", "Decision", "Rationale", "Alternatives",
        "Dissent", "Confidence", "Next_Action", "Review_Date", "Outcome",
    ],
    "Weekly_Reviews": [
        "Review_ID", "Week_Ending", "Decisions", "Shipped_Learned_Influenced",
        "Feedback", "Evidence_Candidates", "AI_Helped", "AI_Misled",
        "Next_Week", "Document_Path", "Created_At",
    ],
    "Quarterly_Reviews": [
        "Review_ID", "Quarter", "Career_Direction", "Competency_Growth",
        "Strengths", "Blind_Spots", "Decision_Quality", "Evidence_Implications",
        "Market_Feedback", "Next_Quarter_Bets", "HTML_Path", "PDF_Path", "Created_At",
    ],
    "Development_Experiments": [
        "Experiment_ID", "Created_At", "Hypothesis", "Competency", "Action",
        "Success_Metric", "Deadline", "Status", "Result", "Reflection",
    ],
    "Prompt_Lessons": [
        "Lesson_ID", "Date", "Context", "Original_Question", "Problem",
        "Improved_Question", "Lesson",
    ],
    "Feedback": [
        "Feedback_ID", "Date", "Source", "Context", "Feedback", "Theme",
        "Action", "Confidentiality",
    ],
    "History": [
        "Event_ID", "Timestamp", "Actor", "Action", "Entity_Type", "Entity_ID",
        "Summary", "Before_JSON", "After_JSON",
    ],
    "Lists": ["List", "Value", "Sort_Order"],
}


@dataclass(frozen=True)
class Score:
    key: str
    label: str
    maximum: int
    points: int
    rationale: str = ""
    evidence: str = ""
    unknowns: str = ""

    def validate(self) -> None:
        if self.points < 0 or self.points > self.maximum:
            raise ValueError(f"{self.label}: points {self.points} outside 0-{self.maximum}")

