from django.contrib import admin
from .models import (
    Region, AcademicDegree, PositionDegree, Employee,
    University, Faculty, Kafedra, Direction,
    Subject, EmployeeSubject, DirectionSubject
)


# -----------------------------
# Employee admin
# -----------------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'degree', 'position')
    list_filter = ('degree', 'position')
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# Region, AcademicDegree, PositionDegree
# -----------------------------
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AcademicDegree)
class AcademicDegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PositionDegree)
class PositionDegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


# -----------------------------
# University admin
# -----------------------------
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'employee', 'phone_number', 'email')
    list_filter = ('region',)
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# Faculty admin
# -----------------------------
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'employee')
    list_filter = ('university',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# Kafedra admin
# -----------------------------
@admin.register(Kafedra)
class KafedraAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee')
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# Direction admin
# -----------------------------
@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'kafedra')
    list_filter = ('kafedra',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# Subject admin
# -----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# EmployeeSubject admin
# -----------------------------
@admin.register(EmployeeSubject)
class EmployeeSubjectAdmin(admin.ModelAdmin):
    list_display = ('employee', 'subject')
    list_filter = ('subject',)
    search_fields = ('employee__first_name', 'employee__last_name', 'subject__name')
    readonly_fields = ('created_date', 'updated_date')


# -----------------------------
# DirectionSubject admin
# -----------------------------
@admin.register(DirectionSubject)
class DirectionSubjectAdmin(admin.ModelAdmin):
    list_display = ('direction', 'subject')
    list_filter = ('direction',)
    search_fields = ('direction__name', 'subject__name')
    readonly_fields = ('created_date', 'updated_date')
