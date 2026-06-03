from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Region, University, Direction,
    Profile, TestQuestion, TestOption, UserTestResult,
    AdditionalResource
)


class TestOptionInline(admin.TabularInline):
    model = TestOption
    extra = 4
    fields = ('text_uz', 'text_ru', 'text_en', 'direction', 'score')

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_text_preview',)
    fieldsets = (
        ('O\'zbekcha (Uzbek)', {
            'fields': ('text_uz',)
        }),
        ('Русский (Russian)', {
            'fields': ('text_ru',)
        }),
        ('English', {
            'fields': ('text_en',)
        }),
    )
    
    def get_text_preview(self, obj):
        return obj.text_uz[:50]
    get_text_preview.short_description = 'Text'
    
    inlines = [TestOptionInline]

@admin.register(UserTestResult)
class UserTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'recommendation', 'created_date')
    list_filter = ('user', 'created_date')
    readonly_fields = ('user', 'score_data', 'recommendation', 'created_date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')
    fieldsets = (
        ('O\'zbekcha (Uzbek)', {
            'fields': ('name_uz',)
        }),
        ('Русский (Russian)', {
            'fields': ('name_ru',)
        }),
        ('English', {
            'fields': ('name_en',)
        }),
    )
    search_fields = ('name_uz', 'name_ru', 'name_en')


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'region', 'faculties_count', 'directions_count', 'students_count', 'professors_count')
    list_filter = ('region',)
    search_fields = ('name_uz', 'name_ru', 'name_en', 'email', 'phone_number')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('Basic Information', {
            'fields': ('region', 'phone_number', 'email', 'website', 'image', 'latitude', 'longitude')
        }),
        ('Counts', {
            'fields': ('faculties_count', 'directions_count', 'students_count', 'professors_count')
        }),
        ('O\'zbekcha (Uzbek)', {
            'fields': ('name_uz', 'postal_address_uz')
        }),
        ('Русский (Russian)', {
            'fields': ('name_ru', 'postal_address_ru')
        }),
        ('English', {
            'fields': ('name_en', 'postal_address_en')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date')
        }),
    )


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name_uz', 'name_ru', 'name_en')
    search_fields = ('name_uz', 'name_ru', 'name_en')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        ('O\'zbekcha (Uzbek)', {
            'fields': ('name_uz',)
        }),
        ('Русский (Russian)', {
            'fields': ('name_ru',)
        }),
        ('English', {
            'fields': ('name_en',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date')
        }),
    )


@admin.register(AdditionalResource)
class AdditionalResourceAdmin(admin.ModelAdmin):
    list_display = ('title_uz', 'title_ru', 'title_en', 'url')
    search_fields = ('title_uz', 'title_ru', 'title_en', 'description_uz', 'description_ru', 'description_en')
    fieldsets = (
        ('Basic Information', {
            'fields': ('url', 'icon_class')
        }),
        ('O\'zbekcha (Uzbek)', {
            'fields': ('title_uz', 'description_uz')
        }),
        ('Русский (Russian)', {
            'fields': ('title_ru', 'description_ru')
        }),
        ('English', {
            'fields': ('title_en', 'description_en')
        }),
    )


