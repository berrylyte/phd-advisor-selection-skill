# PhD Advisor Selection Skill - MVP Status

**Status**: MVP Framework Complete ✓ All 5 Stages Implemented

**Date**: 2026-05-23

---

## What's Done

### Core Infrastructure
✓ **Project Structure** - Clean src/ organization with stages/ and tools/ modules
✓ **All 5 Stages** - Complete basic implementation
  - Stage 1: Self-Assessment (questions, constraint gathering)
  - Stage 2: Research Direction (background → keywords)
  - Stage 3: Advisor Pool Search (search, data collection, prioritization)
  - Stage 4: Email Tracking (timeline management)
  - Stage 5: Offer Evaluation (comparison & decision)

✓ **Persistence Layer** - progress.json + readable progress.md
  - Cross-session data carry-forward
  - Separate email tracker (stage4_tracker.md)
  
✓ **Tool Functions** - Callable by Claude
  - search_advisors() - Find advisor candidates
  - collect_advisor_info() - Gather advisor data (auto + fallback URLs)
  - generate_advisor_table() - Create comparison tables
  - summarize_background() - Extract research interests from projects
  - update_tracker() - Log email/application actions

✓ **System Prompts** - Instructions for Claude's flow management

✓ **Integration Tests** - All 5 stages + persistence verified

### Project Files
```
phd-advisor-selection-skill/
├── src/
│   ├── core.py (main logic, stage router, persistence)
│   ├── prompts.py (system prompts for Claude)
│   ├── stages/
│   │   ├── stage1.py
│   │   ├── stage2.py
│   │   ├── stage3.py
│   │   ├── stage4.py
│   │   └── stage5.py
│   └── tools/
│       ├── web_search.py (advisor search)
│       ├── data_collector.py (auto + fallback)
│       ├── data_processor.py (tables, summaries)
│       └── file_manager.py (file I/O)
├── test_integration.py (7 test functions, all passing)
├── requirements.txt
├── skill.yaml (skill metadata)
├── README.md
└── MVP_STATUS.md (this file)
```

---

## What's Working

### Basic Flow Examples

**Stage 1 Flow**:
```
User: "Help me choose a PhD"
Claude: Asks about motivation, constraints, mindset
User: Answers (can skip unclear ones)
Claude: Summarizes back, routes to Stage 2
```

**Stage 3 Flow** (most complex):
```
Claude: Calls search_advisors(keywords) → finds 50-100 candidates
Claude: Calls collect_advisor_info() → gathers data (auto + fallback URLs)
Claude: Calls generate_advisor_table() → shows concrete dimensions
Claude: Helps user prioritize → saves shortlist
```

**Data Persistence**:
```
Session 1: User completes Stage 1-2, saves to progress.json
Session 2: Load progress.json automatically, continue from Stage 3
```

---

## What's MVP (Working with Mock Data)

- ✓ Framework structure
- ✓ Stage flow logic
- ✓ Progress persistence
- ⚠️ Advisor search (currently mock data for testing)
- ⚠️ Data collection (mock advisor info for testing)

---

## What Needs Implementation (Phase 2)

### High Priority
1. **Real Web Scraping**
   - Actual Google Scholar lookups (h-index, citation data)
   - Homepage scraping for recruiting status
   - Job board searches (jobs.ac.uk, etc.)
   - Currently returns mock data

2. **Claude API Integration**
   - Framework supports calling, but not integrated yet
   - Need to wire up: skill context → Claude → tools → progress updates
   - Streaming conversation management

3. **Small-Group Testing**
   - Give to 3-5 actual PhD applicants
   - Collect feedback on Stage 3 data quality
   - Validate question clarity in Stage 1-2
   - Get feedback on email tracking usefulness

### Medium Priority
1. **Better Data Collection**
   - Handle more edge cases (advisor retired, homepage down, etc.)
   - Improve fallback URL suggestions
   - Cache results to avoid re-scraping

2. **Enhanced UX**
   - Better table formatting
   - More context in Claude prompts
   - Clearer guidance for edge cases

3. **GitHub Deployment**
   - Create GitHub repo
   - Add CI/CD for tests
   - Document setup instructions

---

## Quick Test Run Results

```
[PASS] Stage 1: Self-Assessment questions working
[PASS] Stage 2: Background → keywords synthesis working
[PASS] Stage 3: Advisor search, collection, table generation working
[PASS] Stage 4: Email tracking working
[PASS] Stage 5: Offer comparison working
[PASS] Data persistence across sessions working
[PASS] Skill context creation for Claude working
```

---

## Next Steps

### Immediate (This Week)
1. [ ] Create GitHub repo and push code
2. [ ] Prepare skill for small-group testing (3-5 users)
3. [ ] Document how to run locally
4. [ ] Set up feedback collection mechanism

### During Testing (Next 1-2 Weeks)
1. [ ] Gather feedback from testers on each stage
2. [ ] Identify missing information in advisor data
3. [ ] Find bugs/edge cases in flow
4. [ ] Iterate on Stage 3 advisor recommendations

### After Testing (Phase 2)
1. [ ] Implement real web scraping based on feedback
2. [ ] Integrate with Claude API properly
3. [ ] Deploy to GitHub with Claude Code skill format
4. [ ] Make skill publicly available

---

## Running Tests Locally

```bash
# Setup
git clone <repo>
cd phd-advisor-selection-skill
pip install -r requirements.txt

# Run tests
python test_integration.py

# Expected: All tests pass, ~60 seconds
```

---

## Known Limitations (MVP)

1. **Mock Advisor Data**: Uses hardcoded advisor list for testing
2. **No Real Web Scraping**: Returns placeholder advisor info
3. **No Claude API**: Framework ready but not integrated
4. **Simplified NLP**: Keyword extraction is basic
5. **Limited Error Handling**: Basic fallback for collection failures

All of these are explicitly flagged as "MVP" and planned for Phase 2.

---

## Architecture Principles

The MVP follows these principles (preserved for iteration):

1. **Claude-Driven**: Not user commands; Claude manages flow intelligently
2. **Flexible Entry**: User can start at any stage
3. **Persistent Progress**: Data carries across sessions in progress.json
4. **Concrete Over Abstract**: Advisor metrics (pub rate, grad time) not feelings
5. **Graceful Degradation**: If auto-collection fails, provide fallback URLs
6. **Separation of Concerns**: Stages are independent, can be tweaked individually

These are maintained through Phase 2 testing.

---

## Feedback Form for Testers

When testing, focus on:

**Stage 1**:
- Clear enough questions?
- Too much cognitive load?
- Missing important constraints?

**Stage 2**:
- Does keyword extraction match your interests?
- Missing important sub-areas?

**Stage 3**:
- Are advisor metrics concrete/useful?
- Missing key information about advisors?
- Table format clear?

**Stage 4**:
- Email template helpful?
- Timing rules clear?

**Stage 5**:
- Offer comparison framework helpful?
- Missing important decision factors?

---

**Status**: Ready for small-group testing.
