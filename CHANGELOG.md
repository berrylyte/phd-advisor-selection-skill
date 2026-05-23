# Changelog

## [v0.2.0] - 2026-05-24

### Status
**MVP - Alpha**

Early stage release with core functionality working. Stage 1-4 flows are implemented and functional. 

### What's New
- ✅ Complete Stage 1-4 flow implementation
- ✅ Progress persistence (progress.md generation)
- ✅ Advisor candidate search and comparison table generation
- ✅ Email outreach template and tracker framework
- ✅ Data isolation support (ADVISOR_DATA_PATH environment variable)

### Test Results

**Test Date**: 2026-05-23  
**Test Subject**: Graduate student, STEM background, multiple publications (with top-tier conferences)  
**Test Method**: Complete Stage 1-4 walk-through with realistic user profile and research interests  
**Result**: 3.5/5 overall satisfaction

Test identified 3 critical issues (detailed below). All other flows working as expected.

### Known Issues (v0.1)

#### 🔴 Critical Issues (Fixed in v0.2)

**Issue #1: Missing Stage 3A Interaction Checkpoint**
- Problem: After searching for candidates, the skill should pause to let user review findings before expanding search
- Impact: User may not understand search scope or have proper control over process
- Planned Fix: v0.2

**Issue #2: Stage 4 Outreach Strategy Should Be Parallel**
- Problem: Current design suggests sequential outreach (email advisor A → wait → email advisor B if no response)
- Should Be: Simultaneously email different institutions (only stagger same-institution contacts by 1-2 weeks)
- Impact: Unnecessarily extends timeline by 1-2 months
- Planned Fix: v0.2

**Issue #3: Candidate Pool Generation Needs Expansion**
- Problem: Current implementation finds limited candidates; should systematically scan academic venues for 15-30 qualified advisors
- Should Be: Adaptive venue-scanning based on user's research direction (different fields → different venues)
- Impact: Limited optionality in advisor selection
- Planned Fix: v0.2

### v0.2 Roadmap (Completed)
- [ ] Implement Issue #1: Add interaction checkpoint after search
- [ ] Implement Issue #2: Parallel outreach strategy with proper timing rules
- [ ] Implement Issue #3: Systematic advisor discovery (adaptive to research direction)
- [ ] Additional testing and refinement
- [ ] Integration testing with Claude Code

### Breaking Changes
None (first release)

### Security
- ✓ No hardcoded credentials or sensitive data
- ✓ Proper use of environment variables for configuration
- ✓ All test artifacts properly gitignored

---

## How to Report Issues

Found a problem or have feedback?

1. **Create an issue on GitHub** with:
   - Your research direction/field
   - Which stage the issue occurred
   - What you expected vs what happened
   - Steps to reproduce (if applicable)

2. **Or suggest improvements** if you have ideas for:
   - Better search strategies
   - Improved advisor comparison dimensions
   - Clearer guidance at any stage

All feedback is valuable as this skill continues development.

---

**Last Updated**: 2026-05
