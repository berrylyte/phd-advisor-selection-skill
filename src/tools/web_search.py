"""
Web Search Tools
Search for advisors from journals, conferences, job boards
"""

from typing import List, Dict, Optional
import json


class AdvisorSearcher:
    """Search for advisor candidates from academic sources"""

    def __init__(self):
        self.job_boards = {
            "UK": ["https://www.jobs.ac.uk/", "https://euraxess.ec.europa.eu/jobs"],
            "US/Canada": [
                "https://jobs.chronicle.com/",
                "https://jobs.sciencecareers.org/",
                "https://www.higheredjobs.com/"
            ],
            "Europe": [
                "https://euraxess.ec.europa.eu/jobs/search",
                "https://universitypositions.eu/jobs/phd",
                "https://www.eurosciencejobs.com/"
            ],
            "Asia": [
                "https://www.timeshighereducation.com/unijobs/",
                "https://jobs.sciencecareers.org/jobs/asia/",
                "https://www.nature.com/naturecareers/jobs/asia-pacific/academia/"
            ],
            "Global": [
                "https://academicpositions.com/jobs/position/phd",
                "https://phdfinder.com/",
                "https://www.phdscanner.com/",
                "https://jobrxiv.org/job-category/phd/"
            ]
        }

    def search(self, keywords: List[str], region: Optional[str] = None) -> List[Dict]:
        """
        Search for advisors by keywords
        Returns list of candidate advisors

        Implementation notes:
        - In MVP: Return mock data
        - In full version: Use Anthropic API to search web,
          scrape top conferences/journals, extract PI names
        """

        # MVP: Mock data for testing
        candidates = [
            {
                "name": "Dr. Alice Chen",
                "school": "MIT",
                "department": "EECS",
                "research_area": "Multimodal Learning",
                "h_index": 45,
                "pubs_per_year": 8,
                "recent_citation_growth": "+10%/yr",
                "student_diversity": "High",
                "grad_time_years": 5.2,
                "advisor_status": "Recruiting",
                "homepage": "https://mit.edu/~achen",
                "scholar": "https://scholar.google.com/citations?user=chen_alice"
            },
            {
                "name": "Dr. Bob Kumar",
                "school": "Stanford",
                "department": "CS",
                "research_area": "Vision Language Models",
                "h_index": 38,
                "pubs_per_year": 6,
                "recent_citation_growth": "-2%/yr",
                "student_diversity": "Medium",
                "grad_time_years": 5.8,
                "advisor_status": "Recruiting",
                "homepage": "https://stanford.edu/~bkumar",
                "scholar": "https://scholar.google.com/citations?user=kumar_bob"
            },
            {
                "name": "Dr. Carol Wong",
                "school": "Berkeley",
                "department": "EECS",
                "research_area": "Multimodal AI",
                "h_index": 52,
                "pubs_per_year": 9,
                "recent_citation_growth": "+15%/yr",
                "student_diversity": "High",
                "grad_time_years": 5.5,
                "advisor_status": "Not currently recruiting",
                "homepage": "https://berkeley.edu/~cwong",
                "scholar": "https://scholar.google.com/citations?user=wong_carol"
            }
        ]

        # Filter by keywords if provided
        if keywords:
            candidates = [
                c for c in candidates
                if any(kw.lower() in c["research_area"].lower() for kw in keywords)
            ]

        # Filter by region if provided
        if region and region != "Global":
            # Mock region filtering
            region_schools = {
                "US": ["MIT", "Stanford", "Berkeley"],
                "UK": ["Oxford", "Cambridge", "Imperial"],
                "Canada": ["UofT", "UBC"]
            }
            school_list = region_schools.get(region, [])
            candidates = [c for c in candidates if c["school"] in school_list]

        return candidates

    def get_job_board_urls(self, region: Optional[str] = None) -> List[Dict]:
        """Return relevant job board URLs for region"""
        if region:
            return [
                {"name": url, "region": region}
                for url in self.job_boards.get(region, [])
            ]

        # Return all
        all_urls = []
        for region, urls in self.job_boards.items():
            all_urls.extend([{"name": url, "region": region} for url in urls])
        return all_urls
