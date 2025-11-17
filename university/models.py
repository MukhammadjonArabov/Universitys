from django.db import models

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AcademicDegree(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PositionDegree(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    degree = models.ForeignKey(AcademicDegree, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(PositionDegree, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="employees/", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class University(BaseModel):
    name = models.CharField(max_length=255)
    postal_address = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    image = models.ImageField(upload_to="universities/", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="faculties/", null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(BaseModel):
    name = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Direction(BaseModel):
    name = models.CharField(max_length=255)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EmployeeSubject(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("employee", "subject")

    def __str__(self):
        return f"{self.employee} — {self.subject}"


class DirectionSubject(BaseModel):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("direction", "subject")

    def __str__(self):
        return f"{self.direction} — {self.subject}"
from django.db import models

# Create your models here.
