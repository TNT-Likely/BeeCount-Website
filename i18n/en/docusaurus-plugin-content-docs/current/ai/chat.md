---
sidebar_position: 4
---

# AI Chat

Smart financial assistant - communicate with AI in natural language.

## Start a Chat

1. Tap the AI icon at the top right of the Transactions tab
2. Or long-press the app icon → "AI Assistant"

## Chat Examples

### Recording

```
Record a lunch expense of $15 today
```

Since 3.2.3, AI Chat also supports **detecting multiple transactions in one message**:

```
Record: taxi 30 today, dinner 45, bubble tea 18
```

Writes follow your on-device tool permissions. Successful entries appear as transaction cards that you can review, edit, or undo. These examples show possible inputs, not fixed response wording.

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

### Agent conversations

The AI Assistant calls local ledger tools when needed:

- Totals and category, tag, or account breakdowns are aggregated locally, without the detail-list limit.
- Tool execution progress appears in the conversation before the final answer or transaction card.
- Memory and tool permissions are managed on the device; ledger writes follow the permission settings.
- Local history is retained for follow-up questions. Long conversations automatically summarize the context sent to the model without deleting the displayed messages.

## The 3.8.3 conversation experience

### Full-width reading and streaming replies

Answers use a full-width layout so avatars and action controls do not narrow the content. Compatible models stream their replies; providers without streaming tool support may use a non-streaming fallback, so not every model will display text incrementally.

Processing and tool progress appear together, with expandable, safe execution summaries. This is not the model's complete private reasoning. You can stop a running request without waiting for it to finish.

### Follow-up questions after an answer

A separate, theme-tinted section below the latest eligible answer shows two questions by default. Use the shuffle control to browse other candidates.

- Successful queries provide contextual follow-ups based on actual dates, categories, and tool results.
- Complete analysis prompts, such as spending summaries, category breakdowns, and budget suggestions, remain available. They go through the same assistant rather than injecting preloaded ledger data into a prompt.
- Candidate rotation happens locally without another model request. Suggested analysis questions are read-only and cannot automatically change budgets or transactions.
- Failed or canceled queries do not produce new follow-ups pretending to have query evidence.

### Automatic summaries for long conversations

When history length or the character budget reaches a threshold, the assistant continues with a summary of older messages plus recent original messages. Context usage and summarization status are visible; usage is a character-based estimate, not the provider's exact token count.

Summary caches are isolated by conversation and ledger and invalidated when older messages are edited or deleted. If summarization fails, bounded history is used instead. Summaries can omit details, are not current financial facts, and do not automatically become long-term memory. Ask for a fresh query when you need up-to-date figures.

### Useful questions

Try "Show monthly food spending this year", "What are this month's category shares?", or "How does that compare with last month?" Local tools compute totals and breakdowns; the model interprets the question and explains the results. It can still misunderstand the scope, so check important figures against your ledger statistics.

Unusual-spending analysis is limited to the data actually retrieved. Budget suggestions do not set budgets automatically or guarantee future spending.

## Model setup and data boundaries

Ledger queries require a text model with native tool calling. A successful plain-text test does not necessarily mean ledger tools are supported. Test the text model in provider management under [AI settings](./overview.md). On failure, inspect the provider's status code, error code, and message, then check the URL, key, balance, or model configuration.

Tools run on the device, but your question, necessary conversation history, and tool results are sent to your configured model provider. AI processing is not entirely offline. Context summaries can also generate model requests; costs and supported capabilities depend on the provider. Avoid unnecessary sensitive information in chats.

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
