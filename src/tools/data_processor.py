"""
Data Processor
Generate tables, summaries, and synthesized information
"""

from typing import List, Dict


class TableGenerator:
    """Generate advisor comparison tables"""

    def generate(self, advisor_data: List[Dict], user_priorities: List[str]) -> str:
        """
        Generate markdown comparison table
        Based on user priorities and advisor data
        """

        if not advisor_data:
            return "No advisor data to display."

        # Create markdown table
        table = "| Advisor | School | H-Index | Pub/Yr | Citation Growth | Grad Time | Diversity | Activity |\n"
        table += "|---------|--------|---------|--------|-----------------|-----------|-----------|----------|\n"

        for advisor in advisor_data:
            table += f"| {advisor.get('name', 'Unknown')} "
            table += f"| {advisor.get('school', 'Unknown')} "
            table += f"| {advisor.get('h_index', 'N/A')} "
            table += f"| {advisor.get('pubs_per_year', 'N/A')} "
            table += f"| {advisor.get('recent_citation_growth', 'N/A')} "
            table += f"| {advisor.get('grad_time_years', 'N/A')}y "
            table += f"| {advisor.get('student_diversity', 'Unknown')} "
            table += f"| {'Y' if advisor.get('advisor_status') == 'Recruiting' else 'N'} "
            table += "|\n"

        return table

    def summarize_pool(self, advisor_data: List[Dict]) -> str:
        """
        Summarize advisor pool in concrete dimensions
        NOT abstract questions, but actual patterns
        """

        if not advisor_data:
            return "No data to summarize."

        summary = "## Advisor Pool Summary\n\n"

        # Academic Activity
        avg_pub_year = sum(a.get('pubs_per_year', 0) for a in advisor_data) / len(advisor_data)
        summary += f"**Academic Activity**: Average {avg_pub_year:.1f} papers/year across pool\n"
        summary += f"  - High activity (8+ papers/year): {sum(1 for a in advisor_data if a.get('pubs_per_year', 0) >= 8)} advisors\n"
        summary += f"  - Medium activity (5-7): {sum(1 for a in advisor_data if 5 <= a.get('pubs_per_year', 0) < 8)} advisors\n"
        summary += f"  - Lower activity (<5): {sum(1 for a in advisor_data if a.get('pubs_per_year', 0) < 5)} advisors\n\n"

        # Diversity
        high_diversity = sum(1 for a in advisor_data if a.get('student_diversity') == 'High')
        summary += f"**Student Diversity**: {high_diversity} groups with high diversity\n"
        summary += f"  → Suggests inclusive mentoring culture\n\n"

        # Graduation Time
        avg_grad = sum(a.get('grad_time_years', 0) for a in advisor_data) / len(advisor_data)
        summary += f"**Graduation Timeline**: Average {avg_grad:.1f} years\n"
        summary += f"  → Consider your patience/urgency\n\n"

        # Advisor Status
        recruiting = sum(1 for a in advisor_data if a.get('advisor_status') == 'Recruiting')
        summary += f"**Actively Recruiting**: {recruiting}/{len(advisor_data)} advisors\n"
        summary += f"  → Check others' homepages to confirm\n"

        return summary


class BackgroundSummarizer:
    """Synthesize student background into research interests"""

    def summarize(self, background_info: Dict) -> str:
        """
        Take student's background info and synthesize into:
        - Primary research area
        - Sub-areas
        - Search keywords
        """

        summary = "## Research Direction Summary\n\n"

        major = background_info.get('major', 'Unknown')
        projects = background_info.get('projects', [])
        interests = background_info.get('interests', '')

        summary += f"**Your Background**: {major}\n"
        summary += f"**Key Projects**: {', '.join(projects) if projects else 'None listed'}\n"

        if interests:
            summary += f"\n**Primary Interest Topic**: {interests}\n"

        # Extract keywords (MVP: simple approach)
        keywords = self._extract_keywords(interests, projects)
        if keywords:
            summary += f"\n**Suggested Search Keywords**:\n"
            for kw in keywords:
                summary += f"- {kw}\n"

        summary += "\n**Next Step**: Use these keywords to search for advisors in Stage 3.\n"

        return summary

    @staticmethod
    def _extract_keywords(interests: str, projects: List[str]) -> List[str]:
        """
        Simple keyword extraction from interests and projects
        MVP: Very basic
        Production: Use NLP
        """

        keywords = []

        # Extract from interests
        if interests:
            # Split by common delimiters
            parts = interests.lower().split()
            keywords.extend(parts[:5])  # Take first 5 words

        # Extract from projects
        if projects:
            for proj in projects[:2]:  # First 2 projects
                parts = proj.lower().split()
                keywords.extend(parts[:3])

        # Remove common words
        stopwords = {"i", "the", "a", "an", "and", "or", "for", "in", "on", "is"}
        keywords = [kw for kw in keywords if kw not in stopwords]

        return list(set(keywords))[:8]  # Return unique, up to 8
