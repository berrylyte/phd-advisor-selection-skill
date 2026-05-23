"""
Stage 1: Self-Assessment
Clarifies core needs, constraints, and mindset
"""

from typing import Dict, List


class Stage1Handler:
    """Handles Stage 1 interactions with Claude"""

    def __init__(self, skill):
        self.skill = skill
        self.stage = 1

    def process(self, user_input: str) -> Dict:
        """
        Process user input for Stage 1
        Returns structured data for Claude to use

        Claude will ask questions and this processes the answers
        """
        return {
            "stage": self.stage,
            "status": "in_progress",
            "message": "Let me help you clarify your PhD goals and constraints.",
            "next_questions": self._get_next_questions(),
            "instructions": self._get_instructions()
        }

    def _get_next_questions(self) -> List[str]:
        """Generate next set of questions for Claude to ask user"""
        current_data = self.skill.get_progress(self.stage)

        if not current_data:
            return [
                "Why do you want a PhD? (career advancement / academic interest / immigration / degree-driven / exploring)",
                "Do you have visa/immigration needs that would affect your choice? (Yes/No/Unsure)"
            ]

        if "core_motivation" in current_data and "visa_needs" not in current_data:
            return [
                "Do you have strong economic pressure on your family? (Strong/Moderate/None)",
                "What's your English proficiency level? (Fluent/Intermediate/Learning)"
            ]

        if "english_level" in current_data and "abroad_experience" not in current_data:
            return [
                "Have you lived abroad alone before? (Yes/No)",
                "Do you have location preferences? (Flexible/Some preference/Specific region)"
            ]

        # Stage 1 complete
        return []

    def _get_instructions(self) -> str:
        """Instructions for Claude on how to handle Stage 1"""
        return """
Stage 1: Self-Assessment

**Goal**: Help user clarify their PhD motivation and key constraints.

**Key Points for Claude**:
1. Light touch - don't overwhelm. User can skip unclear answers and revisit later.
2. Explain *why* each question matters (e.g., visa needs affect school choice)
3. After gathering info, summarize: "So if I understand correctly, your core motivation is [X],
   and your hard constraints are [Y]. Sound right?"
4. Remind them: "PhD is a match game, not a merit game. Rejection is data, not personal failure."

**Mindset Check**:
- "I can master out if needed" → healthy ✓
- "I must succeed or I fail as a person" → needs reset

**After Stage 1 Complete**:
Claude should ask: "Ready to move to Stage 2 (clarify research direction)
or would you like to skip to looking at schools directly?"
"""

    def save_answer(self, question_key: str, answer: str):
        """Save user's answer to progress"""
        data = {question_key: answer}
        self.skill.update_progress(self.stage, data)

    def get_stage_summary(self) -> str:
        """Generate summary of Stage 1 data"""
        data = self.skill.get_progress(self.stage)

        if not data:
            return "Stage 1: Not started"

        summary = "## Stage 1: Self-Assessment Summary\n\n"
        summary += f"- **Core Motivation**: {data.get('core_motivation', 'Not provided')}\n"
        summary += f"- **Visa/Immigration Needs**: {data.get('visa_needs', 'Not specified')}\n"
        summary += f"- **Economic Pressure**: {data.get('economic_pressure', 'Not specified')}\n"
        summary += f"- **English Level**: {data.get('english_level', 'Not specified')}\n"
        summary += f"- **Abroad Experience**: {data.get('abroad_experience', 'Not specified')}\n"
        summary += f"- **Location Preference**: {data.get('location_preference', 'Flexible')}\n"

        return summary
