"""
PhD Advisor Selection Skill - Core Logic
Claude-driven multi-stage skill for PhD advisor selection
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class PhDAdvisorSkill:
    """Main skill class managing all stages and persistence"""

    def __init__(self, user_id: str, data_dir: str = "./data"):
        self.user_id = user_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.progress_file = self.data_dir / f"progress_{user_id}.json"
        self.progress_md_file = self.data_dir / f"progress_{user_id}.md"
        self.tracker_file = self.data_dir / f"tracker_{user_id}.md"

        self.current_stage = None
        self.progress_data = self._load_progress()

    # ==================== File Management ====================

    def _load_progress(self) -> Dict:
        """Load progress.json as dict, or create new one"""
        if self.progress_file.exists():
            try:
                content = self.progress_file.read_text(encoding='utf-8')
                return json.loads(content)
            except Exception as e:
                print(f"Error loading progress: {e}")
                return self._create_new_progress()
        else:
            return self._create_new_progress()

    def _create_new_progress(self) -> Dict:
        """Create new progress structure"""
        return {
            "user_id": self.user_id,
            "created_at": datetime.now().isoformat(),
            "stage1": {},
            "stage2": {},
            "stage3": {},
            "stage4": {},
            "stage5": {}
        }

    def save_progress(self):
        """Save progress_data to both JSON and MD"""
        # Save as JSON for persistence
        json_content = json.dumps(self.progress_data, indent=2, ensure_ascii=False)
        self.progress_file.write_text(json_content, encoding='utf-8')

        # Also save as readable MD
        md_content = self._dict_to_progress_md(self.progress_data)
        self.progress_md_file.write_text(md_content, encoding='utf-8')

    def _dict_to_progress_md(self, data: Dict) -> str:
        """Convert progress dict to markdown format"""
        md = f"""# PhD Advisor Selection Progress

**User ID**: {self.user_id}
**Last Updated**: {datetime.now().isoformat()}

## Stage 1: Self-Assessment

{self._format_section(data.get('stage1', {}))}

## Stage 2: Research Direction

{self._format_section(data.get('stage2', {}))}

## Stage 3: Advisor Pool & Shortlist

{self._format_section(data.get('stage3', {}))}

## Stage 4: Email Outreach & Tracking

See separate tracker file.

## Stage 5: Offer Evaluation

{self._format_section(data.get('stage5', {}))}
"""
        return md

    @staticmethod
    def _format_section(section_dict: Dict) -> str:
        """Format a section dict as markdown"""
        if not section_dict:
            return "(Not started)"
        lines = []
        for key, value in section_dict.items():
            if isinstance(value, list):
                lines.append(f"- **{key}**:")
                for item in value:
                    lines.append(f"  - {item}")
            elif isinstance(value, dict):
                lines.append(f"- **{key}**:")
                for k, v in value.items():
                    lines.append(f"  - {k}: {v}")
            else:
                lines.append(f"- **{key}**: {value}")
        return "\n".join(lines)

    def update_progress(self, stage: int, data: Dict):
        """Update progress for a specific stage"""
        stage_key = f"stage{stage}"
        if stage_key not in self.progress_data:
            self.progress_data[stage_key] = {}
        self.progress_data[stage_key].update(data)
        self.save_progress()

    def get_progress(self, stage: Optional[int] = None) -> Dict:
        """Get progress data for specific stage or all"""
        if stage:
            return self.progress_data.get(f"stage{stage}", {})
        return self.progress_data

    # ==================== Stage Router ====================

    def determine_entry_stage(self, user_context: str) -> int:
        """
        Claude provides context about where user is.
        Skill determines which stage to start/resume.

        Args:
            user_context: e.g., "Already decided on PhD, need to find advisors"

        Returns:
            Stage number (1-5)
        """
        # Check if user has existing progress
        if self.progress_data.get('stage1') and not self.progress_data.get('stage2'):
            return 2  # Resume from Stage 2

        if self.progress_data.get('stage3'):
            return 4  # Offer stage

        # Default routing based on context
        if "already decided" in user_context.lower() or "find advisor" in user_context.lower():
            return 2
        elif "have offer" in user_context.lower():
            return 5
        else:
            return 1

    # ==================== Stage Implementations ====================

    def run_stage_1(self, user_input: str) -> Dict:
        """
        Stage 1: Self-Assessment
        Gathers core motivation, constraints, mindset
        """
        from .stages.stage1 import Stage1Handler
        handler = Stage1Handler(self)
        return handler.process(user_input)

    def run_stage_2(self, user_input: str) -> Dict:
        """
        Stage 2: Research Direction
        Clarifies research interests, builds keywords
        """
        from .stages.stage2 import Stage2Handler
        handler = Stage2Handler(self)
        return handler.process(user_input)

    def run_stage_3(self, user_input: str) -> Dict:
        """
        Stage 3: Advisor Pool Search & Collection
        Finds advisors, collects data, helps prioritize
        """
        from .stages.stage3 import Stage3Handler
        handler = Stage3Handler(self)
        return handler.process(user_input)

    def run_stage_4(self, user_input: str) -> Dict:
        """
        Stage 4: Email Outreach & Tracking
        Manages advisor contact timeline
        """
        from .stages.stage4 import Stage4Handler
        handler = Stage4Handler(self)
        return handler.process(user_input)

    def run_stage_5(self, user_input: str) -> Dict:
        """
        Stage 5: Offer Evaluation
        Compares offers, aids decision-making
        """
        from .stages.stage5 import Stage5Handler
        handler = Stage5Handler(self)
        return handler.process(user_input)

    # ==================== Tool Functions (callable by Claude) ====================

    def search_advisors(self, keywords: List[str], region: Optional[str] = None) -> List[Dict]:
        """
        Search for advisors by keywords in journals + job boards
        Called by Claude during Stage 3A

        Returns list of advisor candidates
        """
        from .tools.web_search import AdvisorSearcher
        searcher = AdvisorSearcher()
        results = searcher.search(keywords, region)
        return results

    def collect_advisor_info(self, advisor_names: List[str]) -> Dict:
        """
        Collect detailed info about advisors
        Auto-collection with fallback URLs
        Called by Claude during Stage 3B
        """
        from .tools.data_collector import DataCollector
        collector = DataCollector()
        results = collector.collect_batch(advisor_names)
        return results

    def generate_advisor_table(self, advisor_data: List[Dict], user_priorities: List[str]) -> str:
        """
        Generate advisor comparison table markdown
        Called by Claude during Stage 3C-D
        """
        from .tools.data_processor import TableGenerator
        generator = TableGenerator()
        table = generator.generate(advisor_data, user_priorities)
        return table

    def summarize_student_background(self, background_info: Dict) -> str:
        """
        Summarize student's background into research interests
        Called by Claude during Stage 2
        """
        from .tools.data_processor import BackgroundSummarizer
        summarizer = BackgroundSummarizer()
        summary = summarizer.summarize(background_info)
        return summary

    def update_email_tracker(self, action: str, details: Dict) -> bool:
        """
        Update email/application tracker
        Actions: send_email, follow_up, receive_response, etc.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "details": details
        }

        # Append to tracker
        if not self.tracker_file.exists():
            self.tracker_file.write_text("# Email & Application Tracker\n\n")

        tracker_content = self.tracker_file.read_text(encoding='utf-8')
        tracker_content += f"\n{self._format_tracker_entry(entry)}"
        self.tracker_file.write_text(tracker_content, encoding='utf-8')

        return True

    @staticmethod
    def _format_tracker_entry(entry: Dict) -> str:
        """Format tracker entry as markdown"""
        return f"- **{entry['timestamp']}**: {entry['action']} - {entry['details']}"


# ==================== Skill Entry Point ====================

def create_skill_context(user_id: str) -> Dict:
    """
    Create skill context for Claude to use
    This is what Claude receives and can interact with
    """
    skill = PhDAdvisorSkill(user_id)

    return {
        "skill_name": "PhD Advisor Selection",
        "skill_id": "phd-advisor-selection",
        "user_id": user_id,
        "stages": {
            1: "Self-Assessment (core needs, constraints, mindset)",
            2: "Research Direction (clarify interests, build keywords)",
            3: "Advisor Pool Search (find advisors, collect data, prioritize)",
            4: "Email Outreach (manage contact timeline)",
            5: "Offer Evaluation (compare offers, decide)"
        },
        "tools": {
            "search_advisors": skill.search_advisors,
            "collect_advisor_info": skill.collect_advisor_info,
            "generate_advisor_table": skill.generate_advisor_table,
            "summarize_background": skill.summarize_student_background,
            "update_tracker": skill.update_email_tracker,
            "get_progress": skill.get_progress,
            "update_progress": skill.update_progress,
        },
        "current_progress": skill.get_progress(),
    }


if __name__ == "__main__":
    # Quick test
    skill = PhDAdvisorSkill("test_user_001")
    skill.update_progress(1, {"core_motivation": "Career advancement"})
    print(skill.get_progress(1))
    skill.save_progress()
