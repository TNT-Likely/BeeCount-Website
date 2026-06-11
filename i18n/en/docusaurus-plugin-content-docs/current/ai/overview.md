---
sidebar_position: 1
description: "BeeCount integrates AI for smart recording: chat-based input, image recognition, and voice recording — making expense tracking effortless."
keywords: [AI expense tracker, smart finance app, voice budgeting, image expense recognition, BeeCount AI]
---

# AI Assistant Overview

BeeCount integrates AI features to make recording smarter and easier.

## Features

| Feature | Description |
|---------|-------------|
| [Voice Recording](./voice) | Record with just a sentence |
| [Image Recognition](./image) | Take a photo to auto-recognize bills |
| [AI Chat](./chat) | Smart financial assistant |

## Supported AI Services

- **Zhipu GLM** - Available in China, recommended
- **Custom Providers** - Any OpenAI-compatible provider
- **Local Model** - Offline capable (in development)

## Model Selection

Zhipu GLM offers multiple models to choose from:

| Model | Features | Recommended For |
|-------|----------|-----------------|
| GLM-4-Flash | Free, fast | Daily recording, recommended |
| GLM-4-Air | Balanced performance and cost | Better comprehension needed |
| GLM-4-AirX | Stronger reasoning | Complex scenarios |
| GLM-4-FlashX | Enhanced free model | Free but better results needed |
| GLM-4-Plus | Flagship model | Best performance |
| GLM-4-Long | Ultra-long context | Long conversation scenarios |

> Recommended: Use **GLM-4-Flash** - it's free and sufficient for daily recording needs.

## Configure AI

1. Go to "Me" → "Smart Billing" → "AI Assistant"
2. Select AI service provider
3. Enter API Key
4. Save configuration

## Custom AI Providers

In addition to the built-in Zhipu GLM, you can add any OpenAI-compatible provider:

### Supported Providers

- **SiliconFlow** - Available in China, affordable pricing
- **DeepSeek** - Chinese LLM, great value
- **OpenAI** - Requires overseas network access
- **Other Compatible Services** - Any service providing OpenAI-compatible API

### Add Custom Provider

1. Go to "Me" → "Smart Billing" → "AI Assistant"
2. Tap "Add Provider"
3. Fill in provider details:
   - **Name** - Custom name for easy identification
   - **API URL** - API endpoint provided by the service
   - **API Key** - Your API key
   - **Model Names** - Configure text/vision/speech models as needed

### Capability Binding

You can bind different providers to different AI capabilities:

| Capability | Description | Example |
|------------|-------------|---------|
| Text Understanding | Voice-to-bill, AI chat | Use DeepSeek |
| Image Recognition | Photo bill recognition | Use Zhipu GLM |
| Speech Recognition | Voice to text | Use Zhipu GLM |

This allows you to leverage each provider's strengths for the best experience.

## Get API Key

### Zhipu AI

<video width="100%" controls>
  <source src="/img/zhipu-register-tutorial.mp4" type="video/mp4" />
  Your browser does not support video playback
</video>

1. Visit [Zhipu Open Platform](https://open.bigmodel.cn/)
2. Register an account
3. Go to "API Keys" page and create a new API Key
4. Copy the API Key to BeeCount

> 💡 New users typically have free credits available after registration. GLM-4-Flash model is completely free.

### SiliconFlow

1. Visit [SiliconFlow](https://siliconflow.cn/)
2. Register and complete identity verification
3. Get API Key from the console
4. API URL: `https://api.siliconflow.cn/v1`

### DeepSeek

1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Register an account
3. Create an API Key
4. API URL: `https://api.deepseek.com/v1`

## Web AI Configuration

Sign in to [BeeCount Cloud](../cloud-sync/beecount-cloud.md) on the web → avatar menu → **AI Config**:

- **Provider CRUD** — add, edit, or delete custom providers. The built-in "Zhipu GLM" cannot be deleted (matches mobile constraint); deleting a provider that's currently bound to a capability automatically falls back to the built-in.
- **Capability binding** — three Select dropdowns (text chat / vision / speech), one per capability; providers that lack the relevant model are disabled.
- **Test buttons** — every model input has a **[Test]** button on the right that runs a real LLM call through the server (CORS-free); a "Test all" button at the bottom runs all configured capabilities serially and shows server-returned errors inline on failure.
- **Cross-device sync** — web changes push to mobile in real time via `profile_change` WS, and vice versa.

API keys are shown in plain text by default (matching mobile); be mindful when sharing your screen. Deep parameters (custom_prompt / strategy / bill_extraction_enabled / use_vision) remain on mobile and are not exposed on the web.
