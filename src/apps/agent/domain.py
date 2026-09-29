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

    prompt = """
You are the domain classifier for CampusAI.

Classify the user's request into exactly one of:

- campus
- unknown

Return ONLY valid JSON:

{"domain": "campus"}

or

{"domain": "unknown"}

CLASSIFY AS "campus" if the question is about ANY of the following:

- university
- campus
- department
- students
- teachers
- batches
- subjects
- classrooms
- rooms
- schedules
- timetables
- classes
- exams
- attendance
- admission
- academic programs
- curriculum
- courses
- research
- regulations
- rules
- policies
- procedures
- notices
- institutional information
- uploaded documents
- PDFs
- the knowledge base
- information contained in a document

IMPORTANT:
If the user says:
- "the document"
- "this document"
- "the PDF"
- "this PDF"
- "the uploaded document"
- "according to the document"
- "what does the document say"
- "according to the PDF"

classify the request as "campus".

Also classify questions containing academic terms such as:
- curriculum
- program objectives
- course structure
- academic focus
- research focus
- eligibility
- admission requirements

as "campus" when they could refer to institutional information.

Examples:

User: What does the document say about the applied curriculum?
{"domain": "campus"}

User: What does the document say about the curriculum?
{"domain": "campus"}

User: What does the PDF say about admission?
{"domain": "campus"}

User: What are the program objectives?
{"domain": "campus"}

User: What is the academic and research focus?
{"domain": "campus"}

User: What classes do I have tomorrow?
{"domain": "campus"}

User: What rooms are available tomorrow?
{"domain": "campus"}

User: What is the weather today?
{"domain": "unknown"}

User: Write a Python program.
{"domain": "unknown"}

User: Tell me a joke.
{"domain": "unknown"}

User: Explain quantum physics.
{"domain": "unknown"}

User message:
{message}
"""
    model = get_model()
    response = model.invoke(prompt)

    data = json.loads(response.content)
    result = Domain.model_validate(data)

    return result.domain
