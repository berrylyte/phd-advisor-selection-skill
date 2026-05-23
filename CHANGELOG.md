# Changelog

## [v1.0.0] - 2026-05-23

### Status
**MVP - Post-Testing (Alpha)**

First complete end-to-end test cycle completed with real user. Code is functional but has known issues that need fixing in v2.

### What's New
- ✅ Complete Stage 1-4 flow implementation
- ✅ Progress persistence (progress.md generation)
- ✅ Advisor candidate search and comparison table generation
- ✅ Email outreach template and tracker framework
- ✅ Data isolation support (ADVISOR_DATA_PATH environment variable)

### Known Issues (v1)

#### 🔴 Critical Issues (v2 Priority)

**Issue #1: Missing Stage 3A Interaction Checkpoint**
- After searching for candidates, skill should pause and ask user if they want to review findings before continuing
- Impact: User loses sense of control over search process
- Status: Not fixed in v1
- Fix planned: v2

**Issue #2: Stage 4 Outreach Strategy is Sequential (Should Be Parallel)**
- Current: Suggests emailing advisors one-by-one (Tim first, then Song if Tim fails)
- Should be: Email different institutions simultaneously (only same school/dept needs 1-2 week delay)
- Impact: Wastes 1-2 months of application timeline
- Status: Not fixed in v1
- Fix planned: v2

**Issue #3: Candidate Pool Too Small**
- Current: Only 3 candidates total
- Should be: 15-30 candidates (5-10 per tier: Tier 1/2/3)
- Method: Systematic venue-scanning (ASPLOS, ICLR, MLSys, etc.) adaptive to user's research direction
- Impact: High risk if primary choice not available
- Status: Not fixed in v1
- Fix planned: v2

### Test Results

**Test Date**: 2026-05-23  
**Test Subject**: Graduate student, EE background, CVPR + INFOCOM publications  
**Test Method**: Complete Stage 1-4 walk-through with real background and research interests  
**Result**: 3.5/5 overall satisfaction

**Detailed Feedback**: See `TEST_FEEDBACK_v1.md` and MyVault project directory

### Breaking Changes
None (first release)

### Deprecated
None (first release)

### Security
- No sensitive credentials in code ✓
- Placeholder author/email updated ✓
- All file paths use environment variable configuration ✓

### Docs
- Updated skill.yaml with correct author and GitHub repo
- Added known issues to README.md
- Added TODO comments to core.py for issue tracking
- Created this CHANGELOG

### Next Steps (v2 Roadmap)
- [ ] Implement Issue #1: Add Stage 3A pause point
- [ ] Implement Issue #2: Parallel outreach strategy
- [ ] Implement Issue #3: Systematic candidate pool generation (15-30 candidates)
- [ ] Small-group testing (3-5 users)
- [ ] Integration testing with Claude Code
- [ ] Performance optimization

### Contributors
- @berrylyte - Initial MVP development and testing

---

## How to Report Issues

Found a bug or have feedback? 
1. Create an issue on GitHub
2. Include your research direction and background
3. Describe what stage/step failed
4. Expected vs actual behavior

Thank you for testing! 🎓
