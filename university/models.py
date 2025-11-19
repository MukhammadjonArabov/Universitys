from django.db import models

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Region(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"

    def __str__(self):
        return self.name


class AcademicDegree(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Akademik daraja"
        verbose_name_plural = "Akademik daraja"

    def __str__(self):
        return self.name


class PositionDegree(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"

    def __str__(self):
        return self.name


class Employee(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    degree = models.ForeignKey(AcademicDegree, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(PositionDegree, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="employees/", null=True, blank=True)

    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class University(BaseModel):
    name = models.CharField(max_length=255)
    postal_address = models.TextField()
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    employee = models.ManyToManyField(Employee, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    image = models.ImageField(upload_to="universities/", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Universitet"
        verbose_name_plural = "Universitetlar"

    def __str__(self):
        return self.name


class Faculty(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="faculties/", null=True, blank=True)

    class Meta:
        verbose_name = "Fakultet"
        verbose_name_plural = "Fakultetlar"

    def __str__(self):
        return self.name


class Kafedra(BaseModel):
    name = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Kafedra"
        verbose_name_plural = "Kafedralar"

    def __str__(self):
        return self.name


class Direction(BaseModel):
    name = models.CharField(max_length=255)
    kafedra = models.ForeignKey(Kafedra, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"

    def __str__(self):
        return self.name


class Subject(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Fan"
        verbose_name_plural = "Fanlar"

    def __str__(self):
        return self.name

class EmployeeSubject(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Hodim va fan"
        verbose_name_plural = "Hodimlar va fanlar"
        unique_together = ("employee", "subject")

    def __str__(self):
        return f"{self.employee} — {self.subject}"


class DirectionSubject(BaseModel):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Yo'nalish va fan"
        verbose_name_plural = "Yo'nalishlar va fanlar"
        unique_together = ("direction", "subject")

    def __str__(self):
        return f"{self.direction} — {self.subject}"
