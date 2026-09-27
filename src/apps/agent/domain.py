from pydantic import BaseModel
from typing import Literal
from .llm import get_model
import json

from typing import Literal
import json
from pydantic import BaseModel


class Domain(BaseModel):
    domain: Literal["campus", "unknown"]


def domain_classifier(message: str):

    prompt = f"""
You are a strict domain classifier for a Campus Management System.

Classify the user's message into exactly one of:

- "campus"
- "unknown"

Return ONLY valid JSON:
{{"domain": "campus"}}
or
{{"domain": "unknown"}}

========================
CAMPUS DOMAIN
========================

Classify as "campus" if the user asks about ANYTHING related to
campus management, including:

- today's schedule
- today's schedules
- today's classes
- today classes
- today's timetable
- timetable
- class schedule
- class schedules
- tomorrow's classes
- classes on a specific date
- weekly schedule
- teacher schedule
- student schedule
- batch schedule
- room schedule
- available rooms
- room availability
- teachers
- students
- subjects
- batches
- classrooms
- departments
- class creation
- class cancellation
- class rescheduling
- scheduling conflicts
- teacher conflicts
- room conflicts
- batch conflicts

Examples:

"Show me all of today's schedules"
→ {{"domain": "campus"}}

"show me all of today schedules"
→ {{"domain": "campus"}}

"What classes do I have today?"
→ {{"domain": "campus"}}

"Show my timetable"
→ {{"domain": "campus"}}

"What classes are tomorrow?"
→ {{"domain": "campus"}}

"Is room 204 available at 10 AM?"
→ {{"domain": "campus"}}

"Show me Bikash's schedule"
→ {{"domain": "campus"}}

"Can I schedule a class tomorrow?"
→ {{"domain": "campus"}}

========================
UNKNOWN DOMAIN
========================

Classify as "unknown" if the request is unrelated to campus management.

Examples:

"What is the weather today?"
→ {{"domain": "unknown"}}

"Explain Python decorators"
→ {{"domain": "unknown"}}

"Write a poem"
→ {{"domain": "unknown"}}

"Who is Elon Musk?"
→ {{"domain": "unknown"}}

========================
IMPORTANT
========================

- Focus on the user's INTENT, not perfect grammar.
- Small spelling or grammar mistakes must NOT change the classification.
- "today schedules", "today's schedules", and "today schedule" all mean
  the same campus scheduling intent.
- Never return anything except the JSON object.
- Never add explanations.

USER MESSAGE:
{message}
"""

    model = get_model()
    response = model.invoke(prompt)

    data = json.loads(response.content)
    result = Domain.model_validate(data)

    return result.domain
