"""
Stage 5: Offer Evaluation & Decision
Compares offers systematically, aids final decision
"""

from typing import Dict, List


class Stage5Handler:
    """Handles Stage 5: Offer Evaluation & Decision"""

    def __init__(self, skill):
        self.skill = skill
        self.stage = 5

    def process(self, user_input: str) -> Dict:
        return {
            "stage": self.stage,
            "status": "in_progress",
            "message": "Let me help you compare your offers.",
            "instructions": self._get_instructions(),
            "key_mindset": self._get_mindset()
        }

    def _get_instructions(self) -> str:
        return """
Stage 5: Offer Evaluation & Decision

**For Claude**:
1. Gather offer details from user:
   - School, advisor, funding (amount, type, duration, coverage)
   - Expected graduation time (from advisor's historical avg)
   - Location, cost of living
   - PhD requirements (quals, dissertation, teaching load)
   - Any special circumstances

2. Remind user of their Stage 1 constraints:
   - Visa/immigration needs
   - Funding requirements
   - Location preferences
   - Timeline expectations

3. Help user rank decision factors:
   - "Do you care more about: advisor quality, school reputation, location, funding, graduation time?"
   - Generate comparison table with user's stated priorities

4. Decision framework:
   - **Good advisor >> Good school** (but both matter)
   - Offer is about MATCH, not MERIT
   - If multiple good fits, pick the one most exciting

5. Final check:
   - "You're ready to accept [offer]. Understand this is binding, right?"
   - **Critical**: NEVER accept then decline later (reputation risk)

**Common Decision Mistakes to Warn Against**:
- Rejecting offer just because "graduation takes 6 years" (context matters: US vs UK)
- Overthinking if all offers are good (pick the one most exciting)
- Accepting multiple offers and declining later (reputation damage)
"""

    def _get_mindset(self) -> str:
        return """
Key Reminders:
1. Offer = Match, not Merit
   This is about good fit, not whether you're smart enough.

2. All offers are wins
   If you have multiple offers, you've already succeeded.
   Pick the one that excites you most.

3. No offer is perfect
   Every option has tradeoffs. Accept that and choose.

4. Offer acceptance is binding
   Don't accept then decline. Reputation matters in academia.

5. This is not the end of your journey
   Your advisor relationship evolves. You can adjust focus during PhD.
"""

    def save_offer(self, offer_data: Dict):
        """Save offer information"""
        if "stage5" not in self.skill.progress_data:
            self.skill.progress_data["stage5"] = {}
        if "offers" not in self.skill.progress_data["stage5"]:
            self.skill.progress_data["stage5"]["offers"] = []

        self.skill.progress_data["stage5"]["offers"].append(offer_data)
        self.skill.save_progress()

    def save_decision(self, accepted_offer: Dict, reasoning: str):
        """Save final decision"""
        decision_data = {
            "accepted_offer": accepted_offer,
            "decision_reasoning": reasoning,
            "decided_at": self._get_timestamp()
        }
        self.skill.update_progress(self.stage, decision_data)

    @staticmethod
    def _get_timestamp() -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    def get_stage_summary(self) -> str:
        data = self.skill.get_progress(self.stage)

        if not data:
            return "Stage 5: Not started"

        summary = "## Stage 5: Offer Evaluation & Decision\n\n"

        if "offers" in data:
            offers = data.get("offers", [])
            summary += f"**Offers Received**: {len(offers)}\n\n"
            for i, offer in enumerate(offers, 1):
                summary += f"{i}. {offer.get('school')} - {offer.get('advisor')}\n"
                summary += f"   Funding: {offer.get('funding', 'Not specified')}\n"

        if "accepted_offer" in data:
            accepted = data.get("accepted_offer", {})
            summary += f"\n**Accepted Offer**: {accepted.get('school')} - {accepted.get('advisor')}\n"
            summary += f"**Reasoning**: {data.get('decision_reasoning', 'Not provided')}\n"

        return summary
