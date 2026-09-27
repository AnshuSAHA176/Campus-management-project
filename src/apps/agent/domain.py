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
You are a domain classifier for a Campus Management System.

Your task is to classify the user's message into exactly one of these domains:

1. "campus"
   Use this when the user is asking about anything related to the
   campus management system, including:

   - Class schedules
   - Timetables
   - Teachers
   - Students
   - Subjects
   - Batches or sections
   - Classrooms or rooms
   - Room availability
   - Class creation
   - Class cancellation
   - Class rescheduling
   - Schedule conflicts
   - Teacher schedules
   - Student schedules
   - Room schedules
   - Department schedules
   - Campus notifications
   - Campus activities
   - Any other functionality or information directly related to
     the campus management system.

2. "unknown"
   Use this when the message is unrelated to the campus management
   system.

Examples:

User: "What classes do I have today?"
Output:
{{"domain": "campus"}}

User: "Is Room 204 free tomorrow at 10 AM?"
Output:
{{"domain": "campus"}}

User: "Show me the BCA-3B timetable."
Output:
{{"domain": "campus"}}

User: "Can Bikash take a class tomorrow at 2 PM?"
Output:
{{"domain": "campus"}}

User: "What's the weather today?"
Output:
{{"domain": "unknown"}}

User: "Explain Python decorators."
Output:
{{"domain": "unknown"}}

User: "Write me a poem."
Output:
{{"domain": "unknown"}}

IMPORTANT RULES:
- Return ONLY valid JSON.
- The JSON must contain exactly one field: "domain".
- The value must be exactly "campus" or "unknown".
- Do not include markdown.
- Do not include explanations.
- Do not include additional fields.

User message:
{message}
"""

    model = get_model()

    response = model.invoke(prompt)

    data = json.loads(response.content)

    result = Domain.model_validate(data)

    return result.domain