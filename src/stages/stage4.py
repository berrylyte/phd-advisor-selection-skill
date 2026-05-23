"""
Stage 4: Email Outreach & Tracking
Manages advisor contact timeline, prevents mistakes
"""

from typing import Dict, List
from datetime import datetime, timedelta


class Stage4Handler:
    """Handles Stage 4: Email Outreach & Tracking"""

    def __init__(self, skill):
        self.skill = skill
        self.stage = 4

    def process(self, user_input: str) -> Dict:
        return {
            "stage": self.stage,
            "status": "in_progress",
            "message": "Let me help you manage email outreach.",
            "instructions": self._get_instructions(),
            "tracking_rules": self._get_tracking_rules()
        }

    def _get_instructions(self) -> str:
        return """
Stage 4: Email Outreach & Tracking

**For Claude**:
1. Help user sequence emails by priority (from Stage 3 shortlist)
2. Provide email template scaffold
3. Track each email: date sent, advisor, priority, follow-up deadline
4. **CRITICAL TIMING RULE** - Parallel Outreach Strategy:
   - DIFFERENT institutions: Email SIMULTANEOUSLY (no delay)
   - SAME institution, DIFFERENT departments: Can email simultaneously
   - SAME institution, SAME department: Stagger by 1-2 weeks (avoid overwhelming single department)
   - One email per advisor only (no second round)
   - IMPORTANT: Do NOT wait for one advisor's response before emailing others from different schools

5. Call update_tracker(action, details) to log each action:
   - send_email: {advisor, school, date, subject}
   - follow_up: {advisor, days_since_send, action}
   - receive_response: {advisor, content_type}

**Email Template Scaffold**:
Subject: Prospective PhD Student - [Your Research Interest]

Dear Dr. [Name],

[Relevant background sentence - your project/course that connects]

I have been following your recent work on [specific paper/topic],
and I am particularly interested in [specific aspect].
[Why this specific advisor/lab]

I am currently applying to PhD programs and would be grateful
to discuss potential fit with your group.

[CV, research statement, other materials if requested]

Best regards,
[Your name]

---

**Reminders**:
- Emails should be SHORT (≤200 words)
- Specific to advisor's recent work
- No generic bulk emails
- Be prepared for: silence (wait 2 weeks), rejection (move to next), or interview offer
"""

    def _get_tracking_rules(self) -> Dict:
        return {
            "same_school_same_dept_delay": "1-2 weeks",
            "different_school_delay": "none (email simultaneously)",
            "follow_up_window": "1-2 weeks",
            "max_emails_per_advisor": 1,
            "critical_rule": "PARALLEL OUTREACH: Email different institutions simultaneously. Only stagger same-institution same-department contacts (1-2 weeks apart). Do NOT wait for response from one institution before emailing another."
        }

    def log_email(self, advisor_name: str, school: str, status: str = "sent") -> bool:
        """Log an email action to tracker"""
        self.skill.update_email_tracker(
            action="send_email",
            details={
                "advisor": advisor_name,
                "school": school,
                "status": status,
                "timestamp": datetime.now().isoformat()
            }
        )
        return True

    def get_stage_summary(self) -> str:
        data = self.skill.get_progress(self.stage)

        if not data:
            return "Stage 4: Not started (see tracker file for email log)"

        summary = "## Stage 4: Email & Application Tracking\n\n"
        summary += "See **stage4_tracker.md** for complete log.\n"
        summary += "\nKey tracking info:\n"
        summary += f"- Emails sent: {len(data.get('emails_sent', []))}\n"
        summary += f"- Pending responses: {len(data.get('pending_responses', []))}\n"
        summary += f"- Responses received: {len(data.get('responses_received', []))}\n"

        return summary
