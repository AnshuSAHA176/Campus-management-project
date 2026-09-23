from django.db import models

# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Semester(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="semesters"
    )

    number = models.PositiveSmallIntegerField()

    name = models.CharField(max_length=50)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["department", "number"],
                name="unique_department_semester"
            )
        ]



class Batch(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="batches"
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="batches"
    )

    name = models.CharField(max_length=100)

    section = models.CharField(
        max_length=20,
        blank=True
    )

    academic_year = models.CharField(
        max_length=20
    )

    capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Subject(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="subjects"
    )

    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name="subjects"
    )

    teachers = models.ManyToManyField(
        "account.Teacher",
        related_name="subjects",
        blank=True
    )
    name = models.CharField(max_length=150)

    code = models.CharField(max_length=30)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_subject_code"
            )
        ]


