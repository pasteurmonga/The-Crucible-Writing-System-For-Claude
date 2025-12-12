# Context Management Guide

How to write a novel when AI context windows are limited.

## The Core Problem

A typical novel is 80,000-150,000 words. A typical AI context window is ~100,000 tokens. You cannot hold an entire novel plus all planning documents in context simultaneously.

**Solution:** Strategic loading and aggressive state-saving.

## The Context Budget

For each writing session, budget context approximately:

| Content | Token Estimate | Priority |
|---------|----------------|----------|
| System prompt + skill | ~5,000 | Required |
| Current scene outline | ~500 | Required |
| Style profile | ~1,000 | Required |
| Previous chapter summary | ~500 | Required |
| Character states | ~1,000 | Required |
| Relevant foreshadowing | ~500 | High |
| World details (if needed) | ~500 | Medium |
| **Working space for draft** | **~90,000** | Required |

**Never load:**
- Full text of previous chapters
- Full planning documents
- Multiple chapters at once
- Entire story bibles

## What to Load Per Scene

### Minimum Required Context

```
1. CURRENT SCENE OUTLINE
   - Goal, conflict, turn
   - Key moments
   - Plants/payoffs for this scene
   
2. STYLE PROFILE
   - The extracted voice characteristics
   - Any author-confirmed adjustments
   
3. PREVIOUS CHAPTER SUMMARY (not full text)
   - 100-200 word summary
   - Final character states
   - Ending hook to continue from
   
4. ACTIVE CHARACTER STATES
   - Who is present this scene
   - Their current emotional state
   - What they know at this point
```

### Load On-Demand Only

```
5. SPECIFIC WORLD DETAILS (if scene requires)
   - Only the location being written
   - Only the relevant magic/power rules
   
6. SPECIFIC CHARACTER DETAILS (if introducing)
   - Full bio only for characters appearing for first time
   - Abbreviated after that
   
7. FORESHADOWING TRACKER (specific threads)
   - Only threads being planted or paid off this scene
```

## The Story Bible Strategy

The story bible is your memory system. It tracks everything written so you don't need to hold it in context.

### Story Bible Structure

```json
{
  "book_title": "...",
  "current_chapter": 15,
  "current_scene": 2,
  "total_words": 45230,
  
  "chapters": {
    "1": {
      "title": "...",
      "word_count": 4523,
      "summary": "100-200 word summary...",
      "final_state": {
        "sonny": "location, emotional state, what he knows",
        "liu_ming": "...",
        ...
      }
    },
    ...
  },
  
  "character_states": {
    "sonny": {
      "current_location": "...",
      "emotional_state": "...",
      "knows": ["list of knowledge gained"],
      "relationships": {"liu_ming": "description"}
    },
    ...
  },
  
  "established_facts": [
    {"fact": "...", "established_in": "ch3"},
    ...
  ],
  
  "foreshadowing": {
    "planted": [
      {"thread": "...", "planted_in": "ch5, scene 2", "payoff_expected": "ch12"}
    ],
    "paid_off": [
      {"thread": "...", "planted_in": "ch3", "paid_in": "ch8"}
    ]
  },
  
  "timeline": {
    "ch1": "Year 1, Spring",
    "ch2": "Year 1, Spring (same day)",
    ...
  },
  
  "invented_details": [
    {"detail": "...", "chapter": "ch5", "reviewed": false}
  ]
}
```

### Updating the Story Bible

After EVERY scene:

1. Update character locations/states
2. Log any new established facts
3. Record any foreshadowing planted
4. Note any foreshadowing paid off
5. Update word count

After EVERY chapter:

1. Write chapter summary (100-200 words)
2. Record final character states
3. Update timeline
4. Flag any [INVENTED] details for review
5. Save full chapter text to file

## Resuming Work

When starting a new session:

### Quick Load Sequence

```
1. Load story bible (JSON) → ~2,000 tokens
2. Load style profile → ~1,000 tokens
3. Load current chapter outline → ~500 tokens
4. Load previous chapter summary (from bible) → ~200 tokens
5. Ready to write → ~95,000 tokens available for draft
```

### What NOT to Reload

- Don't re-read completed chapters
- Don't reload full planning documents
- Don't reload the entire outline (only current chapter)

## Emergency Recovery

If context is corrupted or session breaks:

### Recovery Protocol

```
1. Find last saved scene in draft/chapters/
2. Load story-bible.json
3. Identify last complete scene
4. Load ONLY that chapter's outline
5. Re-load style profile
6. Resume from last checkpoint
```

### Prevention

- Save after EVERY scene (not just chapters)
- Story bible updates are atomic (one change at a time)
- Never trust context alone—always verify against saved state

## Multi-Chapter Context

Sometimes you need awareness of multiple chapters:

### When Writing a Payoff Scene

```
Load:
- Current scene outline
- The original plant (from foreshadowing tracker)
- The plant scene SUMMARY (not full text)
- Style profile

Don't load:
- Full text of planting chapter
- Intervening chapters
```

### When Checking Continuity

```
Load:
- Current chapter outline
- Story bible character states
- Story bible established facts
- Last 3 chapter SUMMARIES

Don't load:
- Full text of any previous chapter
- Full planning documents
```

## Word Count Implications

Context limits affect word count targets:

| Scene Length | Can Write in One Pass |
|--------------|----------------------|
| 500-1,500 words | Yes, easily |
| 1,500-3,000 words | Yes, with care |
| 3,000-5,000 words | Consider splitting |
| 5,000+ words | Must split into multiple scenes |

**Strategy for long scenes:**
1. Write first half
2. Save checkpoint
3. Load summary of first half
4. Write second half
5. Merge in final compile

## Practical Commands

### Check Context Usage

Before writing, mentally audit:
- What's loaded?
- What's essential?
- What can be dropped?

### Force Context Clear

When switching chapters:
```
[CONTEXT SHIFT]
Saving Chapter X...
Clearing Chapter X context...
Loading Chapter X+1 outline...
Ready to continue.
```

### Emergency Context Dump

If context seems corrupted:
```
[CONTEXT EMERGENCY]
Saving current work immediately...
Dumping story bible state...
Session should be restarted.
All progress preserved in files.
```

## Summary

1. **Never hold full chapters** — Use summaries
2. **Story bible is memory** — Update it constantly
3. **Save after every scene** — Sessions break
4. **Load minimum needed** — Leave room for writing
5. **Verify against saved state** — Don't trust context alone
