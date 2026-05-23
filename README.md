# PhD Advisor Selection Skill

A Claude-driven interactive skill to help junior researchers systematically select PhD advisors and programs through structured decision-making across 5 stages.

## Overview

This skill guides students through:
1. **Stage 1**: Self-Assessment (core needs, constraints, mindset)
2. **Stage 2**: Research Direction (clarify research interests from background)
3. **Stage 3**: Advisor Pool Search & Info Collection (find advisors, collect data, prioritize)
4. **Stage 4**: Email Outreach & Tracking (manage advisor contact timeline)
5. **Stage 5**: Offer Evaluation (compare offers systematically)

## Key Features

- **Claude-driven flow**: Claude manages stage progression intelligently
- **Flexible entry points**: Start at any stage based on where you are
- **Persistent progress tracking**: Automatically saves to `progress.md` across sessions
- **Dual-route advisor search**: Academic route (journals/papers) + Country-specific job boards
- **Data-driven decisions**: Concrete advisor comparison metrics vs abstract questions
- **Fallback mechanisms**: Auto-collection with manual URL fallback for missing data

## Quick Start

```bash
# Installation
git clone https://github.com/yourusername/phd-advisor-selection-skill.git
cd phd-advisor-selection-skill
pip install -r requirements.txt

# Usage with Claude Code
/phd-advisor-selection

# Or start a conversation
# "Help me choose a PhD advisor"
```

## Project Structure

```
phd-advisor-selection-skill/
├── src/
│   ├── core.py                 # Main skill logic & stage management
│   ├── stages/
│   │   ├── stage1.py          # Self-assessment
│   │   ├── stage2.py          # Research direction
│   │   ├── stage3.py          # Advisor search & collection
│   │   ├── stage4.py          # Email tracking
│   │   └── stage5.py          # Offer evaluation
│   ├── tools/
│   │   ├── web_search.py      # Search journals, job boards
│   │   ├── data_collector.py  # Scrape advisor info
│   │   ├── data_processor.py  # Generate tables, summaries
│   │   └── file_manager.py    # Manage progress.md, tracker.md
│   └── prompts.py             # System prompts for Claude
├── tests/                      # Basic tests
├── skill.yaml                  # Skill definition
├── requirements.txt
└── README.md
```

## Usage Example

**User**: "Help me find a PhD advisor in machine learning"

**Claude**:
1. Understands you're starting from Stage 2-3 (already decided on PhD)
2. Asks about your research background → Stage 2
3. Builds search keywords
4. Searches journals + job boards → Stage 3 substage A
5. Collects advisor data → Stage 3 substage B
6. Generates advisor table with concrete dimensions (academic activity, student diversity, etc.)
7. Helps you prioritize and shortlist → Stage 3 substage D
8. Prepares for email outreach → Stage 4

At any point, you can save progress and resume later.

## Data Persistence

- **progress.md**: Cross-stage student profile (stays same across sessions)
  - Core motivation, constraints, research direction, advisor shortlist, final decision
  
- **stage4_tracker.md**: Independent email/application log
  - Advisor contact dates, follow-up schedule, application status

## Architecture Diagram

```
User Input → Claude (Intelligent Flow Manager)
              ↓
         [Stage Router]
              ↓
    ┌────────┴────────┬────────────┬──────────┬──────────┐
    ↓                 ↓            ↓          ↓          ↓
  Stage 1          Stage 2       Stage 3    Stage 4    Stage 5
  (Q&A)          (Q&A+Tool)   (Tool-heavy) (Tracking) (Decision)
    ↓                 ↓            ↓          ↓          ↓
  progress.md ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ → progress.md
                                                       +tracker.md
```

## Next Steps

- [ ] MVP local testing (all 5 stages basic version)
- [ ] Small-group user testing
- [ ] Feedback iteration
- [ ] Deploy to GitHub
- [ ] Integration with Claude Code

## Contributing

Feedback and contributions welcome! This is in active development.

---

**Status**: MVP in development (2026-05)
