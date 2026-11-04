
import json
from pydantic import BaseModel, ValidationError
from typing import Literal
from .llm import get_model


class Domain(BaseModel):
    domain: Literal["campus", "unknown"]


async def domain_classifier(message: str) -> str:

    prompt = """
You are the domain classifier for CampusAI.

Classify the request into exactly one category:
- campus
- unknown

Return ONLY valid JSON:
{{"domain": "campus"}}
or
{{"domain": "unknown"}}

Classify as campus for:
- University, departments, students, teachers.
- Batches, subjects, classrooms, rooms.
- Schedules, timetables, classes, attendance.
- Exams, admissions, curriculum, courses, research.
- Regulations, policies, procedures, notices.
- Institutional information and uploaded documents.
- PDFs and knowledge-base questions.

Document references such as "this document", "the PDF",
or "according to the document" are campus requests.

Classify as unknown for unrelated topics such as:
- Weather
- General programming questions
- Jokes
- General science questions

User message:
{message}
"""

    model = get_model(model="openai/gpt-oss-20b")

    response = await model.ainvoke(
        prompt.format(message=message)
    )

    try:
        content = response.content

        # Handle possible Markdown JSON fences
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
