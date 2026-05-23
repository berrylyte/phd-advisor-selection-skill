"""
Stage 3: Advisor Pool Search & Info Collection
Finds advisors, collects comprehensive data, helps prioritize
"""

from typing import Dict, List


class Stage3Handler:
    """Handles Stage 3: Advisor Pool Search & Collection"""

    def __init__(self, skill):
        self.skill = skill
        self.stage = 3

    def process(self, user_input: str) -> Dict:
        return {
            "stage": self.stage,
            "status": "in_progress",
            "message": "Let me search for relevant advisors in your research area.",
            "substage": self._get_current_substage(),
            "instructions": self._get_instructions()
        }

    def _get_current_substage(self) -> str:
        """Determine current substage (3A, 3B, 3C, 3D)"""
        data = self.skill.get_progress(self.stage)

        if not data.get("advisor_candidates"):
            return "3A"  # Find advisor candidates
        elif not data.get("advisor_details"):
            return "3B"  # Collect advisor information
        elif not data.get("user_priorities"):
            return "3C"  # Data organization & confirmation
        else:
            return "3D"  # Prioritization & filtering

    def _get_instructions(self) -> str:
        return """
Stage 3: Advisor Pool Search & Collection

Substages:
- 3A: Find advisor candidates (journals + job boards)
- 3B: Collect advisor info (auto + fallback)
- 3C: Organize data, confirm with user
- 3D: Prioritize based on user criteria

**For Claude**:
1. Substage 3A: Call search_advisors(keywords, region)
   → Get list of candidate advisors

2. Substage 3B: Call collect_advisor_info(names)
   → Auto-collect with fallback URLs for missing data

3. Substage 3C: Call generate_advisor_table(data, priorities)
   → Show user the data in concrete dimensions:
     * Academic Activity (pubs/year, citation growth)
     * Student Outcomes (graduation time, diversity, positions)
     * Advisor Seniority (age, tenure status, group stability)
     * Mentorship Style (inferred from student feedback)

4. Substage 3D: Help user prioritize
   - "Which of these dimensions matter most?"
   - "Any advisors you want to shortlist?"
   - Generate final ranked shortlist

**Data Dimensions** (NOT "importance"):
- Academic Activity: High (8+ pubs/yr, rising citations) / Medium / Low
- Student Diversity: High (varied backgrounds) / Medium / Low
- Advisor Seniority: Junior (<10yr) / Mid / Senior (20+yr)
- Mentorship Style: Supportive / Hands-off (inferred)
"""

    def save_answer(self, field: str, value):
        data = {field: value}
        self.skill.update_progress(self.stage, data)

    def get_stage_summary(self) -> str:
        data = self.skill.get_progress(self.stage)

        if not data:
            return "Stage 3: Not started"

        summary = "## Stage 3: Advisor Pool & Shortlist\n\n"

        if "advisor_candidates" in data:
            candidates = data.get("advisor_candidates", [])
            summary += f"**Candidates Found**: {len(candidates)}\n\n"

        if "advisor_shortlist" in data:
            shortlist = data.get("advisor_shortlist", [])
            summary += "**Final Shortlist (Ranked)**:\n"
            for i, advisor in enumerate(shortlist[:10], 1):
                summary += f"{i}. {advisor.get('name', 'Unknown')} ({advisor.get('school', 'Unknown')})\n"

        return summary
