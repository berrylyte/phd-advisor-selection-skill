"""
Stage 2: Research Direction Clarification
Identifies research interests from background, builds search keywords
"""

from typing import Dict, List


class Stage2Handler:
    """Handles Stage 2 interactions"""

    def __init__(self, skill):
        self.skill = skill
        self.stage = 2

    def process(self, user_input: str) -> Dict:
        return {
            "stage": self.stage,
            "status": "in_progress",
            "message": "Let me understand your research background and interests.",
            "next_questions": self._get_next_questions(),
            "instructions": self._get_instructions()
        }

    def _get_next_questions(self) -> List[str]:
        """Generate questions for Stage 2"""
        current_data = self.skill.get_progress(self.stage)

        if not current_data:
            return [
                "What's your major or field of study?",
                "What year are you in? (undergrad/masters/working professional)"
            ]

        if "major" in current_data and "publications" not in current_data:
            return [
                "Have you published or co-authored any papers? If yes, briefly describe topics.",
                "Have you done internships, research assistant roles, or lab work? Describe."
            ]

        if "publications" in current_data and "thesis_topic" not in current_data:
            return [
                "What was your thesis/capstone/main project about?",
                "Looking at your background, which ONE topic made you think 'I want to understand this deeply'?"
            ]

        if "interest_topic" in current_data and "flexibility" not in current_data:
            return [
                "Do you have a clear research direction, or are you still exploring? (clear/exploring/very open)"
            ]

        return []

    def _get_instructions(self) -> str:
        return """
Stage 2: Research Direction Clarification

**Goal**: Use student's background to pinpoint research areas and build search keywords.

**Key Points for Claude**:
1. Ask about: major, publications, internships, thesis, specific interests
2. DON'T just ask "what interests you?" - ask about concrete projects
3. Synthesize answers: "It sounds like your background is in [X], and your projects suggest interest in [Y]. Accurate?"
4. Build keywords from their answers (not generic keywords)

**Examples**:
- Student: "I did thesis on vision-language models for captioning"
- Claude extracts: Primary area = Multimodal Learning
  Sub-areas = Vision-Language, Image Captioning, Cross-modal Alignment
  Keywords = {multimodal, vision-language, VLM, image captioning, CLIP, alignment}

**After Stage 2 Complete**:
Claude should ask: "Ready to search for advisors in these areas? (Stage 3)"
"""

    def save_answer(self, field: str, value: str):
        data = {field: value}
        self.skill.update_progress(self.stage, data)

    def get_stage_summary(self) -> str:
        data = self.skill.get_progress(self.stage)

        if not data:
            return "Stage 2: Not started"

        summary = "## Stage 2: Research Direction Summary\n\n"
        summary += f"- **Major**: {data.get('major', 'Not provided')}\n"
        summary += f"- **Background**: {data.get('publications', 'No publications yet')}\n"
        summary += f"- **Thesis/Project**: {data.get('thesis_topic', 'Not specified')}\n"
        summary += f"- **Primary Interest**: {data.get('interest_topic', 'To be determined')}\n"

        if "research_area" in data:
            summary += f"\n**Research Area**: {data.get('research_area')}\n"

        if "search_keywords" in data:
            summary += f"**Search Keywords**: {', '.join(data.get('search_keywords', []))}\n"

        return summary
