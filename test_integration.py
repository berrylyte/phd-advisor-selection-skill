"""
Integration Test for PhD Advisor Selection Skill
Test basic flow of all 5 stages
"""

from src.core import PhDAdvisorSkill, create_skill_context
from src.stages.stage1 import Stage1Handler
from src.stages.stage2 import Stage2Handler
from src.stages.stage3 import Stage3Handler
from src.stages.stage4 import Stage4Handler
from src.stages.stage5 import Stage5Handler


def test_stage_1():
    """Test Stage 1: Self-Assessment"""
    print("\n=== Testing Stage 1: Self-Assessment ===\n")

    skill = PhDAdvisorSkill("test_user_001")
    handler = Stage1Handler(skill)

    # Simulate user input
    handler.save_answer("core_motivation", "Career advancement + research interest")
    handler.save_answer("visa_needs", "Yes, interested in US immigration")
    handler.save_answer("economic_pressure", "Moderate - prefer full funding")
    handler.save_answer("english_level", "Fluent")
    handler.save_answer("abroad_experience", "No")
    handler.save_answer("location_preference", "US East Coast preferred")

    # Print summary
    print(handler.get_stage_summary())
    print("\n[PASS] Stage 1 test passed")


def test_stage_2():
    """Test Stage 2: Research Direction"""
    print("\n=== Testing Stage 2: Research Direction ===\n")

    skill = PhDAdvisorSkill("test_user_001")
    handler = Stage2Handler(skill)

    # Simulate user input
    handler.save_answer("major", "Computer Science")
    handler.save_answer("publications", "2 conference papers on multimodal learning")
    handler.save_answer("thesis_topic", "Vision-Language Models for Image Captioning")
    handler.save_answer("interest_topic", "Multimodal AI, specifically vision-language alignment")
    handler.save_answer("research_area", "Multimodal Machine Learning")
    handler.save_answer("search_keywords", [
        "multimodal learning",
        "vision-language models",
        "image captioning",
        "cross-modal alignment",
        "VLM"
    ])
    handler.save_answer("flexibility", "clear")

    print(handler.get_stage_summary())
    print("\n[PASS] Stage 2 test passed")


def test_stage_3():
    """Test Stage 3: Advisor Pool Search"""
    print("\n=== Testing Stage 3: Advisor Pool Search ===\n")

    skill = PhDAdvisorSkill("test_user_001")

    # Simulate Stage 3A: Search
    print("Substage 3A: Searching for advisors...")
    advisors = skill.search_advisors(
        keywords=["multimodal", "vision-language"],
        region="US"
    )
    print(f"Found {len(advisors)} advisor candidates")
    for adv in advisors[:3]:
        print(f"  - {adv['name']} ({adv['school']})")

    # Simulate Stage 3B: Collect Info
    print("\nSubstage 3B: Collecting advisor information...")
    advisor_names = [adv['name'] for adv in advisors]
    info = skill.collect_advisor_info(advisor_names)
    print(f"Collected info for {len(info['collected'])} advisors")
    if info.get('fallback_required'):
        print(f"Fallback URLs provided for {len(info['fallback_required'])} advisors")

    # Simulate Stage 3C: Generate Table
    print("\nSubstage 3C: Generating comparison table...")
    table = skill.generate_advisor_table(
        advisor_data=advisors,
        user_priorities=["academic_activity", "student_diversity"]
    )
    print(table)

    # Simulate Stage 3D: Save Shortlist
    print("\nSubstage 3D: Saving shortlist...")
    handler = Stage3Handler(skill)
    handler.save_answer("advisor_shortlist", advisors[:3])  # Top 3
    print(handler.get_stage_summary())

    print("\n[PASS] Stage 3 test passed")


def test_stage_4():
    """Test Stage 4: Email Tracking"""
    print("\n=== Testing Stage 4: Email Outreach ===\n")

    skill = PhDAdvisorSkill("test_user_001")
    handler = Stage4Handler(skill)

    # Simulate email tracking
    print("Logging email actions...")
    handler.log_email("Dr. Alice Chen", "MIT", "sent")
    handler.log_email("Dr. Bob Kumar", "Stanford", "sent")

    skill.update_email_tracker(
        action="follow_up",
        details={
            "advisor": "Dr. Alice Chen",
            "days_since_send": 14,
            "action": "Send follow-up email"
        }
    )

    print("Email tracker updated")
    print(handler.get_stage_summary())
    print("\n[PASS] Stage 4 test passed")


def test_stage_5():
    """Test Stage 5: Offer Evaluation"""
    print("\n=== Testing Stage 5: Offer Evaluation ===\n")

    skill = PhDAdvisorSkill("test_user_001")
    handler = Stage5Handler(skill)

    # Simulate receiving offers
    print("Saving offer information...")
    offer_1 = {
        "school": "MIT",
        "advisor": "Dr. Alice Chen",
        "funding": "$40k/year (TA/RA mix)",
        "grad_time": "5.2 years",
        "location": "Cambridge, MA",
        "requirements": "4 quals, dissertation, 2yr TA"
    }

    offer_2 = {
        "school": "Stanford",
        "advisor": "Dr. Bob Kumar",
        "funding": "$38k/year (RA)",
        "grad_time": "5.8 years",
        "location": "Palo Alto, CA",
        "requirements": "3 quals, dissertation, 1yr TA"
    }

    handler.save_offer(offer_1)
    handler.save_offer(offer_2)

    # Save decision
    print("\nSaving final decision...")
    handler.save_decision(
        accepted_offer=offer_1,
        reasoning="Better advisor-student fit, supportive lab culture, more aligned research direction"
    )

    print(handler.get_stage_summary())
    print("\n[PASS] Stage 5 test passed")


def test_persistence():
    """Test that progress persists across sessions"""
    print("\n=== Testing Persistence ===\n")

    # Create skill, save data
    skill1 = PhDAdvisorSkill("persistent_user")
    skill1.update_progress(1, {"core_motivation": "Research interest"})
    skill1.update_progress(2, {"research_area": "Multimodal AI"})
    skill1.save_progress()
    print(f"Saved progress to {skill1.progress_file}")

    # Load skill again
    skill2 = PhDAdvisorSkill("persistent_user")
    stage1_data = skill2.get_progress(1)
    stage2_data = skill2.get_progress(2)

    print(f"Stage 1: {stage1_data}")
    print(f"Stage 2: {stage2_data}")

    assert stage1_data.get("core_motivation") == "Research interest"
    assert stage2_data.get("research_area") == "Multimodal AI"

    print("\n[PASS] Persistence test passed")


def test_skill_context():
    """Test that skill context is properly created for Claude"""
    print("\n=== Testing Skill Context ===\n")

    context = create_skill_context("test_user_001")

    print(f"Skill Name: {context['skill_name']}")
    print(f"Stages: {len(context['stages'])}")
    print(f"Available Tools: {list(context['tools'].keys())}")

    assert context['skill_id'] == "phd-advisor-selection"
    assert len(context['stages']) == 5
    assert 'search_advisors' in context['tools']

    print("\n[PASS] Skill context test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("PhD Advisor Selection Skill - Integration Tests")
    print("=" * 60)

    test_stage_1()
    test_stage_2()
    test_stage_3()
    test_stage_4()
    test_stage_5()
    test_persistence()
    test_skill_context()

    print("\n" + "=" * 60)
    print("[SUCCESS] All tests passed!")
    print("=" * 60)
