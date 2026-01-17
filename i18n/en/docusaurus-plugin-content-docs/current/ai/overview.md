---
sidebar_position: 1
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

1. Go to "Me" → "Smart Recording" → "AI Assistant", or "Discover" → "Common Features" → "AI Settings"
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

1. Go to "Me" → "Smart Recording" → "AI Assistant"
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
