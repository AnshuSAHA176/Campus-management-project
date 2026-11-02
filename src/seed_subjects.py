
import random
from django.db import transaction
from apps.academics.models import Subject

SUBJECT_NAMES = [
    "Mathematics", "Physics", "Chemistry", "Biology",
    "English Literature", "English Communication", "History",
    "Political Science", "Economics", "Sociology",
    "Psychology", "Philosophy", "Geography", "Environmental Science",
    "Computer Fundamentals", "Programming in C", "Python Programming",
    "Java Programming", "Data Structures", "Algorithms",
    "Database Management Systems", "Operating Systems",
    "Computer Networks", "Software Engineering", "Web Development",
    "Artificial Intelligence", "Machine Learning", "Data Science",
    "Cloud Computing", "Cyber Security", "Computer Architecture",
    "Theory of Computation", "Compiler Design", "Discrete Mathematics",
    "Linear Algebra", "Calculus", "Statistics", "Numerical Methods",
    "Differential Equations", "Real Analysis", "Abstract Algebra",
    "Digital Electronics", "Microprocessors", "Embedded Systems",
    "Internet of Things", "Mobile Application Development",
    "Human Computer Interaction", "Computer Graphics",
    "Information Retrieval", "Big Data Analytics",
    "Distributed Systems", "Advanced Database Systems",
    "Information Security", "Cryptography", "Network Security",
    "Data Mining", "Deep Learning", "Natural Language Processing",
    "Computer Vision", "Robotics", "Research Methodology",
    "Technical Writing", "Business Communication", "Accounting",
    "Business Management", "Marketing Management", "Financial Management",
    "Organizational Behaviour", "Entrepreneurship", "Business Statistics",
    "Microeconomics", "Macroeconomics", "Public Administration",
    "Indian Constitution", "International Relations", "Modern Indian History",
    "Ancient Indian History", "Medieval Indian History",
    "World Geography", "Human Geography", "Social Psychology",
    "Educational Psychology", "Ethics", "Logic",
    "Sustainable Development", "Climate Change", "Biotechnology",
    "Microbiology", "Genetics", "Organic Chemistry",
    "Inorganic Chemistry", "Thermodynamics", "Mechanics",
    "Electromagnetism", "Optics", "Quantum Physics",
    "Scientific Computing", "Operations Research",
    "Project Management", "Digital Marketing",
]

assert len(SUBJECT_NAMES) == 100

departments = list(Subject._meta.get_field("department").remote_field.model.objects.all())
semesters = list(Subject._meta.get_field("semester").remote_field.model.objects.all())
Teacher = Subject._meta.get_field("teachers").remote_field.model
teachers = list(Teacher.objects.all())

if not departments:
    raise RuntimeError("Create at least one department first.")
if not semesters:
    raise RuntimeError("Create at least one semester first.")
if not teachers:
    raise RuntimeError("Create at least one teacher first.")

created = 0
skipped = 0

with transaction.atomic():
    for i, name in enumerate(SUBJECT_NAMES, start=1):
        code = f"LOADTEST-{i:03d}"

        if Subject.objects.filter(code=code).exists():
            skipped += 1
            continue

        subject = Subject.objects.create(
            name=name,
            code=code,
            department=departments[(i - 1) % len(departments)],
            semester=semesters[(i - 1) % len(semesters)],
            is_active=True,
        )

        # Associate one or more existing teachers.
        subject.teachers.set([
            teachers[(i - 1) % len(teachers)]
        ])

        created += 1

print(f"Subjects created: {created}")
print(f"Existing subjects skipped: {skipped}")
print(f"Total subjects with LOADTEST codes: "
      f"{Subject.objects.filter(code__startswith='LOADTEST-').count()}")
