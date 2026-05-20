from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ['-created_date']


class Region(BaseModel):
    # Uzbek
    name_uz = models.CharField(max_length=255, verbose_name="Viloyat nomi (O'zbekcha)")
    # Russian
    name_ru = models.CharField(max_length=255, default="", verbose_name="Название провинции (Русский)")
    # English
    name_en = models.CharField(max_length=255, default="", verbose_name="Province Name (English)")

    class Meta:
        verbose_name = "Viloyat"
        verbose_name_plural = "Viloyatlar"
        ordering = ['name_uz']

    def __str__(self):
        return self.name_uz

    @property
    def name(self):
        return self.get_name(get_language())

    def get_name(self, lang='uz'):
        if lang == 'ru':
            return self.name_ru or self.name_uz
        elif lang == 'en':
            return self.name_en or self.name_uz
        return self.name_uz


class University(BaseModel):
    # Uzbek
    name_uz = models.CharField(max_length=255, verbose_name="Universitet nomi (O'zbekcha)")
    postal_address_uz = models.TextField(verbose_name="Pochtali manzil (O'zbekcha)")
    # Russian
    name_ru = models.CharField(max_length=255, default="", verbose_name="Название университета (Русский)")
    postal_address_ru = models.TextField(default="", verbose_name="Почтовый адрес (Русский)")
    # English
    name_en = models.CharField(max_length=255, default="", verbose_name="University Name (English)")
    postal_address_en = models.TextField(default="", verbose_name="Postal Address (English)")
    
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.CharField(max_length=255)
    image = models.ImageField(upload_to="universities/", null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "Universitet"
        verbose_name_plural = "Universitetlar"
        ordering = ['name_uz']

    def __str__(self):
        return self.name_uz

    @property
    def name(self):
        return self.get_name(get_language())

    @property
    def postal_address(self):
        return self.get_address(get_language())

    def get_name(self, lang='uz'):
        if lang == 'ru':
            return self.name_ru or self.name_uz
        elif lang == 'en':
            return self.name_en or self.name_uz
        return self.name_uz

    def get_address(self, lang='uz'):
        if lang == 'ru':
            return self.postal_address_ru or self.postal_address_uz
        elif lang == 'en':
            return self.postal_address_en or self.postal_address_uz
        return self.postal_address_uz


class Direction(BaseModel):
    # Uzbek
    name_uz = models.CharField(max_length=255, verbose_name="Yo'nalish nomi (O'zbekcha)")
    # Russian
    name_ru = models.CharField(max_length=255, default="", verbose_name="Название направления (Русский)")
    # English
    name_en = models.CharField(max_length=255, default="", verbose_name="Direction Name (English)")

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"
        ordering = ['name_uz']

    def __str__(self):
        return self.name_uz

    @property
    def name(self):
        return self.get_name(get_language())

    def get_name(self, lang='uz'):
        if lang == 'ru':
            return self.name_ru or self.name_uz
        elif lang == 'en':
            return self.name_en or self.name_uz
        return self.name_uz


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


class TestQuestion(BaseModel):
    # Uzbek
    text_uz = models.TextField(verbose_name="Test savoli (O'zbekcha)")
    # Russian
    text_ru = models.TextField(default="", verbose_name="Вопрос теста (Русский)")
    # English
    text_en = models.TextField(default="", verbose_name="Test Question (English)")

    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"
        ordering = ['-created_date']

    def __str__(self):
        return self.text_uz[:50]

    def get_text(self, lang='uz'):
        if lang == 'ru':
            return self.text_ru or self.text_uz
        elif lang == 'en':
            return self.text_en or self.text_uz
        return self.text_uz


class TestOption(BaseModel):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name="options")
    # Uzbek
    text_uz = models.CharField(max_length=255, verbose_name="Test varianti (O'zbekcha)")
    # Russian
    text_ru = models.CharField(max_length=255, default="", verbose_name="Вариант теста (Русский)")
    # English
    text_en = models.CharField(max_length=255, default="", verbose_name="Test Option (English)")
    
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Test varianti"
        verbose_name_plural = "Test variantlari"
        ordering = ['question', 'id']

    def __str__(self):
        return self.text_uz

    def get_text(self, lang='uz'):
        if lang == 'ru':
            return self.text_ru or self.text_uz
        elif lang == 'en':
            return self.text_en or self.text_uz
        return self.text_uz


class UserTestResult(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results")
    score_data = models.JSONField(default=dict)  # Stores scores per direction
    recommendation = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.username} - {self.created_date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)


class AdditionalResource(BaseModel):
    # Uzbek
    title_uz = models.CharField(max_length=255, verbose_name="Sarlavha (O'zbekcha)")
    description_uz = models.TextField(blank=True, null=True, verbose_name="Tavsif (O'zbekcha)")
    # Russian
    title_ru = models.CharField(max_length=255, default="", verbose_name="Название (Русский)")
    description_ru = models.TextField(blank=True, default="", verbose_name="Описание (Русский)")
    # English
    title_en = models.CharField(max_length=255, default="", verbose_name="Title (English)")
    description_en = models.TextField(blank=True, default="", verbose_name="Description (English)")
    
    url = models.URLField()
    icon_class = models.CharField(max_length=100, default="fas fa-link", help_text="FontAwesome icon class (e.g. fas fa-globe)")

    class Meta:
        verbose_name = "Qo'shimcha manba"
        verbose_name_plural = "Qo'shimcha manbalar"
        ordering = ['title_uz']

    def __str__(self):
        return self.title_uz

    def get_title(self, lang='uz'):
        if lang == 'ru':
            return self.title_ru or self.title_uz
        elif lang == 'en':
            return self.title_en or self.title_uz
        return self.title_uz

    def get_description(self, lang='uz'):
        if lang == 'ru':
            return self.description_ru or self.description_uz
        elif lang == 'en':
            return self.description_en or self.description_uz
        return self.description_uz
