from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Region, University, Direction,
    Profile, TestQuestion, TestOption, UserTestResult
)


class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 4

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)
    inlines = [TestOptionInline]

@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'created_date')
    list_filter = ('user', 'created_date')
    readonly_fields = ('user', 'score_data', 'recommendation', 'created_date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'phone_number', 'verification_code')
    search_fields = ('user__username', 'telegram_id', 'phone_number')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_filter = ('region',)
    search_fields = ('name', 'email', 'phone_number')
    readonly_fields = ('created_date', 'updated_date')


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    readonly_fields = ('created_date', 'updated_date')

