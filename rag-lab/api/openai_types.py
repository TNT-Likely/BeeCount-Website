from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class OpenAIChatMessage(BaseModel):
    role: Literal['system', 'user', 'assistant', 'tool', 'developer']
    content: str | list[dict[str, Any]] | None = None
    name: str | None = None

    model_config = ConfigDict(extra='allow')


class OpenAIChatCompletionRequest(BaseModel):
    model: str = 'beecount-rag'
    messages: list[OpenAIChatMessage]
    stream: bool = False
    temperature: float | None = None
    top_p: float | None = None
    max_tokens: int | None = None

    model_config = ConfigDict(extra='allow')


class OpenAIChoiceMessage(BaseModel):
    role: Literal['assistant'] = 'assistant'
    content: str


class OpenAIChoice(BaseModel):
    index: int = 0
    message: OpenAIChoiceMessage
    finish_reason: Literal['stop'] = 'stop'


class OpenAIUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class OpenAIChatCompletionResponse(BaseModel):
    id: str
    object: Literal['chat.completion'] = 'chat.completion'
    created: int
    model: str
    choices: list[OpenAIChoice]
    usage: OpenAIUsage


class OpenAIStreamDelta(BaseModel):
    role: Literal['assistant'] | None = None
    content: str | None = None


class OpenAIStreamChoice(BaseModel):
    index: int = 0
    delta: OpenAIStreamDelta
    finish_reason: Literal['stop'] | None = None


class OpenAIStreamChunk(BaseModel):
    id: str
    object: Literal['chat.completion.chunk'] = 'chat.completion.chunk'
    created: int
    model: str
    choices: list[OpenAIStreamChoice]


class OpenAIModelObject(BaseModel):
    id: str
    object: Literal['model'] = 'model'
    created: int
    owned_by: str = 'beecount-rag-lab'
    metadata: dict[str, str] = Field(default_factory=dict)


class OpenAIModelListResponse(BaseModel):
    object: Literal['list'] = 'list'
    data: list[OpenAIModelObject]
