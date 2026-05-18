from django.test import TestCase
from django.contrib.auth.models import User
from .models import (
    Region, University, Direction, Profile, 
    TestQuestion, TestOption, UserTestResult, AdditionalResource
)


class RegionModelTest(TestCase):
    """Test cases for Region model"""
    
    def setUp(self):
        self.region = Region.objects.create(
            name_uz="Toshkent",
            name_ru="Ташкент",
            name_en="Tashkent"
        )
    
    def test_region_creation(self):
        """Test Region object creation"""
        self.assertEqual(self.region.name_uz, "Toshkent")
        self.assertEqual(str(self.region), "Toshkent")
    
    def test_region_get_name_uzbek(self):
        """Test get_name method with Uzbek language"""
        self.assertEqual(self.region.get_name('uz'), "Toshkent")
    
    def test_region_get_name_russian(self):
        """Test get_name method with Russian language"""
        self.assertEqual(self.region.get_name('ru'), "Ташкент")
    
    def test_region_get_name_english(self):
        """Test get_name method with English language"""
        self.assertEqual(self.region.get_name('en'), "Tashkent")
    
    def test_region_get_name_fallback(self):
        """Test get_name falls back to Uzbek if translation missing"""
        region = Region.objects.create(name_uz="Samarqand")
        self.assertEqual(region.get_name('ru'), "Samarqand")


class UniversityModelTest(TestCase):
    """Test cases for University model"""
    
    def setUp(self):
        self.region = Region.objects.create(name_uz="Toshkent")
        self.university = University.objects.create(
            name_uz="TDTU",
            postal_address_uz="Toshkent",
            name_ru="ТДТУ",
            postal_address_ru="Ташкент",
            region=self.region,
            phone_number="+998712525950",
            email="info@tdtu.uz",
            website="www.tdtu.uz"
        )
    
    def test_university_creation(self):
        """Test University object creation"""
        self.assertEqual(self.university.name_uz, "TDTU")
        self.assertEqual(self.university.email, "info@tdtu.uz")
    
    def test_university_get_name(self):
        """Test get_name method"""
        self.assertEqual(self.university.get_name('uz'), "TDTU")
        self.assertEqual(self.university.get_name('ru'), "ТДТУ")
    
    def test_university_get_address(self):
        """Test get_address method"""
        self.assertEqual(self.university.get_address('uz'), "Toshkent")
        self.assertEqual(self.university.get_address('ru'), "Ташкент")
    
    def test_university_region_relationship(self):
        """Test University-Region relationship"""
        self.assertEqual(self.university.region, self.region)


class DirectionModelTest(TestCase):
    """Test cases for Direction model"""
    
    def setUp(self):
        self.direction = Direction.objects.create(
            name_uz="Axborot texnologiyalari",
            name_ru="Информационные технологии",
            name_en="Information Technology"
        )
    
    def test_direction_creation(self):
        """Test Direction object creation"""
        self.assertEqual(self.direction.name_uz, "Axborot texnologiyalari")
    
    def test_direction_get_name(self):
        """Test get_name method"""
        self.assertEqual(self.direction.get_name('uz'), "Axborot texnologiyalari")
        self.assertEqual(self.direction.get_name('ru'), "Информационные технологии")


class ProfileModelTest(TestCase):
    """Test cases for Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_auto_creation(self):
        """Test that Profile is automatically created when User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.user, self.user)
    
    def test_profile_telegram_id(self):
        """Test Profile telegram_id field"""
        self.user.profile.telegram_id = 123456789
        self.user.profile.save()
        self.assertEqual(self.user.profile.telegram_id, 123456789)
    
    def test_profile_verification_code(self):
        """Test Profile verification_code field"""
        self.user.profile.verification_code = "1234"
        self.user.profile.save()
        self.assertEqual(self.user.profile.verification_code, "1234")


class TestQuestionModelTest(TestCase):
    """Test cases for TestQuestion model"""
    
    def setUp(self):
        self.question = TestQuestion.objects.create(
            text_uz="Savol?",
            text_ru="Вопрос?",
            text_en="Question?"
        )
    
    def test_question_creation(self):
        """Test TestQuestion object creation"""
        self.assertEqual(self.question.text_uz, "Savol?")
    
    def test_question_get_text(self):
        """Test get_text method"""
        self.assertEqual(self.question.get_text('uz'), "Savol?")
        self.assertEqual(self.question.get_text('ru'), "Вопрос?")


class TestOptionModelTest(TestCase):
    """Test cases for TestOption model"""
    
    def setUp(self):
        self.direction = Direction.objects.create(name_uz="IT")
        self.question = TestQuestion.objects.create(text_uz="Savol?")
        self.option = TestOption.objects.create(
            question=self.question,
            text_uz="Variant",
            direction=self.direction,
            score=2
        )
    
    def test_option_creation(self):
        """Test TestOption object creation"""
        self.assertEqual(self.option.text_uz, "Variant")
        self.assertEqual(self.option.score, 2)
    
    def test_option_direction_relationship(self):
        """Test TestOption-Direction relationship"""
        self.assertEqual(self.option.direction, self.direction)
    
    def test_option_question_relationship(self):
        """Test TestOption-Question relationship"""
        self.assertEqual(self.option.question, self.question)


class UserTestResultModelTest(TestCase):
    """Test cases for UserTestResult model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_result_creation(self):
        """Test UserTestResult object creation"""
        result = UserTestResult.objects.create(
            user=self.user,
            recommendation="Tavsiya",
            is_completed=True
        )
        self.assertEqual(result.user, self.user)
        self.assertTrue(result.is_completed)
    
    def test_result_score_data(self):
        """Test UserTestResult score_data field"""
        result = UserTestResult.objects.create(
            user=self.user,
            recommendation="Tavsiya",
            score_data={"IT": 10, "Medicine": 5}
        )
        self.assertEqual(result.score_data['IT'], 10)
    
    def test_result_default_score_data(self):
        """Test UserTestResult default score_data"""
        result1 = UserTestResult.objects.create(
            user=self.user,
            recommendation="Test"
        )
        result1.save()
        
        user2 = User.objects.create_user(username='user2', password='pass123')
        result2 = UserTestResult.objects.create(
            user=user2,
            recommendation="Test2"
        )
        result2.save()
        
        # Ensure they don't share the same dict
        self.assertIsNot(result1.score_data, result2.score_data)


class AdditionalResourceModelTest(TestCase):
    """Test cases for AdditionalResource model"""
    
    def setUp(self):
        self.resource = AdditionalResource.objects.create(
            title_uz="Manba",
            url="https://example.com",
            icon_class="fas fa-link"
        )
    
    def test_resource_creation(self):
        """Test AdditionalResource object creation"""
        self.assertEqual(self.resource.title_uz, "Manba")
        self.assertEqual(self.resource.url, "https://example.com")
    
    def test_resource_get_title(self):
        """Test get_title method"""
        self.assertEqual(self.resource.get_title('uz'), "Manba")
    
    def test_resource_icon_class_default(self):
        """Test default icon_class"""
        resource = AdditionalResource.objects.create(
            title_uz="Test",
            url="https://test.com"
        )
        self.assertEqual(resource.icon_class, "fas fa-link")
