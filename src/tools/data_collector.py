"""
Data Collector
Auto-collect advisor info from web, with fallback URLs
"""

from typing import List, Dict, Optional


class DataCollector:
    """Collect detailed info about advisors"""

    def __init__(self):
        self.fallback_urls = {}

    def collect_batch(self, advisor_names: List[str]) -> Dict:
        """
        Collect info for multiple advisors
        Auto-collection with fallback URLs

        Returns:
            {
                "collected": {advisor_name: {full_info}},
                "fallback_required": {advisor_name: [urls]},
                "summary": "X successfully collected, Y require manual check"
            }
        """

        collected = {}
        fallback_required = {}

        for name in advisor_names:
            try:
                info = self._collect_single(name)
                if info.get("complete"):
                    collected[name] = info
                else:
                    # Partial - need manual follow-up
                    collected[name] = info
                    fallback_required[name] = info.get("fallback_urls", [])
            except Exception as e:
                fallback_required[name] = [
                    f"Error collecting: {str(e)}",
                    "Please check advisor homepage manually"
                ]

        summary = f"Successfully collected: {len(collected)} | Need manual check: {len(fallback_required)}"

        return {
            "collected": collected,
            "fallback_required": fallback_required,
            "summary": summary
        }

    def _collect_single(self, advisor_name: str) -> Dict:
        """
        Collect info for single advisor
        MVP: Mock data
        Production: Use Google Scholar API, web scraping, etc.
        """

        # Mock implementation for MVP
        mock_data = {
            "name": advisor_name,
            "complete": True,
            "publication_info": {
                "h_index": 45,
                "total_citations": 2500,
                "papers_last_5y": 40,
                "avg_papers_per_year": 8,
                "citation_growth": "+10% per year",
                "source": "Google Scholar (auto-collected)"
            },
            "homepage_info": {
                "current_title": "Associate Professor",
                "research_focus": "Multimodal Learning",
                "recruiting": "Yes",
                "group_size": "8 PhD students, 3 postdocs",
                "source": "Advisor homepage (partial)"
            },
            "student_outcomes": {
                "avg_graduation_time": 5.2,
                "recent_graduates": 3,
                "industry_percentage": "30%",
                "academic_placement": "70%",
                "source": "Homepage + LinkedIn (partial)"
            },
            "co_author_network": {
                "collaborators": ["MIT", "Stanford", "Berkeley"],
                "industry_collaborations": "Intel, Google",
                "international": "Yes",
                "source": "Last 5 years papers (auto-collected)"
            },
            "fallback_urls": [
                f"Homepage: https://school.edu/~{advisor_name.lower().replace(' ', '_')}",
                f"Google Scholar: https://scholar.google.com/citations?user=SCHOLAR_ID",
                f"LinkedIn: https://linkedin.com/in/{advisor_name.lower().replace(' ', '-')}"
            ]
        }

        return mock_data

    def verify_recruiting_status(self, advisor_name: str, school: str) -> Dict:
        """
        Check if advisor is actively recruiting
        MVP: Return mock status
        """
        return {
            "advisor": advisor_name,
            "school": school,
            "recruiting": "Not explicitly stated",
            "fallback_url": f"Check {school} PhD program website and {advisor_name}'s homepage",
            "note": "Please verify directly"
        }
