---
sidebar_position: 2
---

# Voice Recording

Say a sentence, and AI automatically recognizes and completes the record.

## How to Use

1. Long-press the microphone icon on home or recording page
2. Speak your transaction
3. AI automatically recognizes and fills in details
4. Confirm and save

## Trigger Modes (since 3.5.5)

Choose how recording starts and stops in **Settings → Smart Billing → Voice trigger mode**:

- **Auto-detect pause** (default): recording starts as soon as the dialog opens and ends automatically after a pause. The pause threshold is adjustable (0.5–4s, default 1.5s) — if longer sentences keep getting cut off, simply increase it
- **Hold to talk**: like sending a voice message — hold the microphone to record, release to recognize. Best for longer entries; presses shorter than 0.5s are treated as accidental and discarded

Both modes are protected by a 60-second recording cap. The trigger mode and pause duration sync across devices via cloud sync.

## Voice Examples

```
"Spent $15 on lunch today"
→ Type: Expense | Category: Food | Amount: $15 | Date: Today

"Took a taxi home yesterday for $12"
→ Type: Expense | Category: Transportation | Amount: $12 | Date: Yesterday

"Received salary of $5,000"
→ Type: Income | Category: Salary | Amount: $5,000

"Bought groceries for $45.80"
→ Type: Expense | Category: Shopping | Amount: $45.80
```

## Supported Expressions

- Amount: Numbers, spoken amounts
- Time: Today, yesterday, last week, etc.
- Category: Common spending scenarios auto-matched

## Multiple Transactions in One Sentence

Since 3.2.3, voice recording supports **multiple transactions per utterance** (previously only the first one was kept). For example:

```
"Taxi 30 today, dinner 45, bubble tea 18"
→ Three transaction drafts, confirm row-by-row and save in one go
```

Great for catch-up entries: on the way home, dictate the few things you spent on today in one breath — no need to long-press the mic three times.

## Notes

- Microphone permission required
- Network connection needed (uses cloud AI)
- Best used in quiet environments

## Auto Tag

When using voice recording, the system automatically adds a "Voice Recording" tag to the transaction for easy filtering and statistics.
