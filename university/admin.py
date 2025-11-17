from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Region, AcademicDegree, PositionDegree, Employee,
    University, Faculty, Kafedra, Direction,
    Subject, EmployeeSubject, DirectionSubject
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'degree', 'position', 'image_tag')
    list_filter = ('degree', 'position')
    search_fields = ('first_name', 'last_name')
    readonly_fields = ('created_date', 'updated_date')
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"

    image_tag.short_description = 'Rasm'


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(AcademicDegree)
class AcademicDegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PositionDegree)
class PositionDegreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'employee', 'phone_number', 'email')
    list_filter = ('region',)
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'employee')
    list_filter = ('university',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Kafedra)
class KafedraAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee')
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'kafedra')
    list_filter = ('kafedra',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')


@admin.register(EmployeeSubject)
class EmployeeSubjectAdmin(admin.ModelAdmin):
    list_display = ('employee', 'subject')
    list_filter = ('subject',)
    search_fields = ('employee__first_name', 'employee__last_name', 'subject__name')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(DirectionSubject)
class DirectionSubjectAdmin(admin.ModelAdmin):
    list_display = ('direction', 'subject')
    list_filter = ('direction',)
    search_fields = ('direction__name', 'subject__name')
    readonly_fields = ('created_date', 'updated_date')
