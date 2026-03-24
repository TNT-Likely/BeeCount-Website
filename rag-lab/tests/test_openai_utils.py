from api.openai_types import OpenAIChatMessage
from api.openai_utils import estimate_usage, extract_query_and_system, split_answer_chunks


def test_extract_query_and_system() -> None:
    messages = [
        OpenAIChatMessage(role='system', content='你是助手'),
        OpenAIChatMessage(role='user', content='第一问'),
        OpenAIChatMessage(role='assistant', content='回答'),
        OpenAIChatMessage(role='user', content='最终问题'),
    ]

    query, system_prompt = extract_query_and_system(messages)
    assert query == '最终问题'
    assert system_prompt == '你是助手'


def test_extract_query_from_content_parts() -> None:
    messages = [
        OpenAIChatMessage(
            role='user',
            content=[
                {'type': 'text', 'text': 'hello'},
                {'type': 'text', 'text': 'world'},
            ],
        )
    ]

    query, system_prompt = extract_query_and_system(messages)
    assert query == 'hello\nworld'
    assert system_prompt is None


def test_split_and_usage() -> None:
    chunks = split_answer_chunks('Hello world from rag')
    assert ''.join(chunks) == 'Hello world from rag'

    messages = [OpenAIChatMessage(role='user', content='How to sync?')]
    prompt, completion, total = estimate_usage(messages, 'Do this.')
    assert prompt > 0
    assert completion > 0
    assert total == prompt + completion
