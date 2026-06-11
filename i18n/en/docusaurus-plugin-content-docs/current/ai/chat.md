---
sidebar_position: 4
---

# AI Chat

Smart financial assistant - communicate with AI in natural language.

## Start a Chat

1. Tap the AI icon at the top right of the Home tab
2. Or long-press the app icon → "AI Assistant"

## Chat Examples

### Recording

```
User: Record a lunch expense of $15 today
AI: Got it! I've recorded an expense:
    - Amount: $15
    - Category: Food
    - Date: Today
    Confirm to save?
```

Since 3.2.3, AI Chat also supports **detecting multiple transactions in one message**:

```
User: Record: taxi 30 today, dinner 45, bubble tea 18
AI: I detected 3 transactions, please confirm:
    1. Expense / Transportation / $30 / today
    2. Expense / Food / $45 / today
    3. Expense / Food / $18 / today
    Save all? (you can deselect individual rows)
```

### Queries

```
User: How much did I spend this month?
AI: Your expenses this month:
    - Total: $1,256
    - Food: $420 (33.4%)
    - Transportation: $180 (14.3%)
    - ...
```

### Analysis

```
User: Are there any issues with my spending?
AI: Based on your records:
    1. Food expenses are relatively high, suggest...
    2. Entertainment spending is concentrated on weekends...
```

## Message Actions

Long-press a message in the chat to perform these actions:

- **Copy** - Copy message content
- **Delete** - Delete a single message

## Custom Prompts

In AI settings, you can customize prompts to make AI better match your usage habits.

## Web Text Recording

After signing in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web, the desktop browser can **paste text directly** for AI to convert into transactions:

1. On any page, press **⌘K / Ctrl+K** to open the command palette
2. **Paste a text block** — WeChat bill text, Excel selection, natural language like "Taxi yesterday 30 + lunch 25"
3. The default action becomes "AI bill (text)" → Enter
4. A dialog shows N transaction drafts to review, then save in batch

The server uses a chat LLM (Zhipu GLM-4-Flash / DeepSeek etc., bind it in [AI Config](./overview.md#web-ai-configuration)) to parse.

### Ask the docs from ⌘K

Type the `?xxx` prefix → the command palette default action switches to "Ask AI: xxx" → Enter → opens a RAG-powered Q&A dialog. It indexes the BeeCount-Website docs, so questions like "how to enable 2FA / Docker deploy / how do tags work" return answers grounded in the official documentation.
