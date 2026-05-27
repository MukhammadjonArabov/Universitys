"""
Utility functions for the university app.
Handles multi-language support, localization, and common business logic.
"""

from django.utils.translation import get_language as django_get_language
from django.utils.translation import gettext_lazy as _


def get_current_language(request) -> str:
    """
    Get the current language code from request or Django settings.
    Returns a valid language code: 'uz', 'ru', or 'en'
    """
    lang = getattr(request, 'LANGUAGE_CODE', None) or django_get_language()
    return lang if lang in ('uz', 'ru', 'en') else 'uz'


def get_localized_field(base_name: str, lang: str = None) -> str:
    """
    Generate the localized field name for a model.
    Example: get_localized_field('name', 'ru') -> 'name_ru'
    """
    if lang is None:
        lang = django_get_language()
    return f"{base_name}_{lang}"


def get_localized_value(obj, field_name: str, lang: str = None) -> str:
    """
    Get localized value from a model instance.
    Tries localized field first, falls back to default (uz) if needed.
    """
    if lang is None:
        lang = django_get_language()
    
    # Try the localized field
    localized_field = get_localized_field(field_name, lang)
    if hasattr(obj, localized_field):
        value = getattr(obj, localized_field, '')
        if value:
            return value
    
    # Fallback to Uzbek
    uz_field = get_localized_field(field_name, 'uz')
    if hasattr(obj, uz_field):
        return getattr(obj, uz_field, '')
    
    return ''


# Translation dictionary for common UI strings
COMMON_TRANSLATIONS = {
    'uz': {
        'loading': 'Kutilmoqda...',
        'analyzing': 'Gemini AI javoblaringizni tahlil qilmoqda...',
        'analyzing_detail': 'Javoblaringiz Gemini AI tomonidan qayta ishlanmoqda, iltimos kuting.',
        'congratulations': 'Tabriklaymiz!',
        'test_completed': 'Test muvaffaqiyatli yakunlandi. Sizning natijangiz tahlil qilinmoqda.',
        'error_title': 'Xato yuz berdi',
        'try_again': 'Qayta urinib ko\'ring',
        'back_home': 'Bosh sahifaga qaytish',
        'view_universities': 'Tavsiya etilgan universitetlarni ko\'rish',
        'previous': 'Oldingisi',
        'next': 'Keyingisi',
        'finish': 'Yakunlash',
        'personality_analysis': 'Shaxsiyat va Qobiliyatlar Tahlili',
        'recommended_directions': 'Tavsiya Etilgan Kasbiy Yo\'nalishlar',
        'university_majors': 'O\'zbekistondagi Universitetlarda Tavsiya Etilgan Mutaxassisliklar',
        'preparation_roadmap': 'Universitetga Tayyorlash Yo\'li Xaritasi',
        'action_plan': 'Harakat Rejasi',
        'motivation': 'Motivatsion Xulosa',
        'no_data': 'Ma\'lumot mavjud emas',
        'service_unavailable': 'Gemini xizmati hozir band. Iltimos, birozdan keyin qayta urinib ko\'ring.',
        'api_error': 'Gemini API xatosi yuz berdi. Iltimos, sahifani yangilang.',
        'no_valid_answers': "Javoblar topilmadi. Iltimos, test savollariga javob bering.",
        'invalid_json': "So'rov formati noto'g'ri.",
    },
    'ru': {
        'loading': 'Загрузка...',
        'analyzing': 'Gemini AI анализирует ваши ответы...',
        'analyzing_detail': 'Ваши ответы обрабатываются Gemini AI, пожалуйста, подождите.',
        'congratulations': 'Поздравляем!',
        'test_completed': 'Тест завершен успешно. Ваши результаты анализируются.',
        'error_title': 'Произошла ошибка',
        'try_again': 'Попробуйте еще раз',
        'back_home': 'На главную',
        'view_universities': 'Посмотреть рекомендуемые университеты',
        'previous': 'Назад',
        'next': 'Далее',
        'finish': 'Завершить',
        'personality_analysis': 'Анализ личности и способностей',
        'recommended_directions': 'Рекомендуемые профессиональные направления',
        'university_majors': 'Рекомендуемые специальности в университетах Узбекистана',
        'preparation_roadmap': 'Дорожная карта подготовки к университету',
        'action_plan': 'План действий',
        'motivation': 'Мотивационное резюме',
        'no_data': 'Данные отсутствуют',
        'service_unavailable': 'Сервис Gemini сейчас недоступен. Пожалуйста, повторите позже.',
        'api_error': 'Произошла ошибка API Gemini. Пожалуйста, обновите страницу.',
        'no_valid_answers': 'Ответы не найдены. Пожалуйста, ответьте на вопросы теста.',
        'invalid_json': 'Неверный формат запроса.',
    },
    'en': {
        'loading': 'Loading...',
        'analyzing': 'Gemini AI is analyzing your answers...',
        'analyzing_detail': 'Your answers are being processed by Gemini AI, please wait.',
        'congratulations': 'Congratulations!',
        'test_completed': 'Test completed successfully. Your results are being analyzed.',
        'error_title': 'An error occurred',
        'try_again': 'Try again',
        'back_home': 'Back to home',
        'view_universities': 'View recommended universities',
        'previous': 'Previous',
        'next': 'Next',
        'finish': 'Finish',
        'personality_analysis': 'Personality & Abilities Analysis',
        'recommended_directions': 'Recommended Career Directions',
        'university_majors': 'Recommended Majors in Uzbek Universities',
        'preparation_roadmap': 'University Preparation Roadmap',
        'action_plan': 'Action Plan',
        'motivation': 'Motivation Summary',
        'no_data': 'No data available',
        'service_unavailable': 'Gemini service is currently unavailable. Please try again later.',
        'api_error': 'Gemini API error occurred. Please refresh the page.',
        'no_valid_answers': 'No answers were found. Please answer the test questions.',
        'invalid_json': 'Invalid request format.',
    }
}


def get_translation(key: str, lang: str = None) -> str:
    """
    Get translated string from the common translations dictionary.
    Example: get_translation('loading', 'uz') -> 'Kutilmoqda...'
    """
    if lang is None:
        lang = django_get_language()
    
    return COMMON_TRANSLATIONS.get(lang, {}).get(key, key)


def get_language_name(lang_code: str) -> str:
    """Get the display name for a language code."""
    names = {
        'uz': "O'zbekcha",
        'ru': 'Русский',
        'en': 'English',
    }
    return names.get(lang_code, lang_code)
