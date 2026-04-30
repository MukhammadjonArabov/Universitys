from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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





class University(BaseModel):
    name = models.CharField(max_length=255)
    postal_address = models.TextField()
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

    def __str__(self):
        return self.name


class Direction(BaseModel):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Yo'nalish"
        verbose_name_plural = "Yo'nalishlar"

    def __str__(self):
        return self.name


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.user.username


class TestQuestion(BaseModel):
    text = models.TextField()

    class Meta:
        verbose_name = "Test savoli"
        verbose_name_plural = "Test savollari"

    def __str__(self):
        return self.text[:50]


class TestOption(BaseModel):
    question = models.ForeignKey(TestQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, null=True, blank=True)
    score = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Test varianti"
        verbose_name_plural = "Test variantlari"

    def __str__(self):
        return self.text


class UserTestResult(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="test_results")
    score_data = models.JSONField(default=dict)  # Stores scores per direction
    recommendation = models.TextField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Test natijasi"
        verbose_name_plural = "Test natijalari"

    def __str__(self):
        return f"{self.user.username} - {self.created_date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


class AdditionalResource(BaseModel):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    icon_class = models.CharField(max_length=100, default="fas fa-link", help_text="FontAwesome icon class (e.g. fas fa-globe)")

    class Meta:
        verbose_name = "Qo'shimcha manba"
        verbose_name_plural = "Qo'shimcha manbalar"

    def __str__(self):
        return self.title
