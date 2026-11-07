import json
from pydantic import BaseModel, ValidationError
from typing import Literal
from .llm import get_model


class Domain(BaseModel):
    domain: Literal["campus", "unknown"]


async def domain_classifier(conversation: str) -> str:

    prompt = """
You are a conversation-aware domain classifier for a Campus Management AI.

Classify the CURRENT USER MESSAGE as either:
- campus
- unknown

Rules:

1. Classify the latest user message, not the entire conversation.
2. Short replies like "12-13", "tomorrow", and "yes" inherit campus context when appropriate.
3. New unrelated requests must be classified as unknown.
4. Follow-ups like "tell me one more" inherit the immediate conversational context.
5. Never classify based only on older campus keywords.
6. If context is insufficient, return unknown.

Return ONLY valid JSON:

{{"domain": "campus"}}

or

{{"domain": "unknown"}}

Conversation:
{conversation}
"""

    model = get_model(model="openai/gpt-oss-20b")

    response = await model.ainvoke(
        prompt.format(conversation=conversation)
    )

    try:
        content = response.content

        if isinstance(content, str):
            content = content.strip()

            if content.startswith("```"):
                content = content.split("\n", 1)[1]
                content = content.rsplit("```", 1)[0].strip()

        data = json.loads(content)
        result = Domain.model_validate(data)

        return result.domain

    except (json.JSONDecodeError, ValidationError, TypeError):
        return "unknown"