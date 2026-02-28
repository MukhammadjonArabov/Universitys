import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from university.models import Profile
from .serializers import TelegramUserSerializer

class BotSyncUserView(APIView):
    def post(self, request):
        serializer = TelegramUserSerializer(data=request.data)
        if serializer.is_valid():
            telegram_id = serializer.validated_data['telegram_id']
            phone_number = serializer.validated_data['phone_number']
            first_name = serializer.validated_data.get('first_name', '')
            last_name = serializer.validated_data.get('last_name', '')
            username = serializer.validated_data.get('username', f"user_{telegram_id}")

            # Try to find user by telegram_id first
            profile = Profile.objects.filter(telegram_id=telegram_id).first()
            
            if not profile:
                # If not found, try to find by phone number
                # Strip '+' if present for matching
                clean_phone = phone_number.replace('+', '')
                # Note: This is an assumption, adjust if phone storage format differs
                profile = Profile.objects.filter(phone_number__icontains=clean_phone).first()

            if profile:
                user = profile.user
            else:
                # Create user if not exists
                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username)
                else:
                    user = User.objects.get(username=username)
                profile = user.profile

            # Update profile info
            profile.telegram_id = telegram_id
            profile.phone_number = phone_number
            
            # Generate 4-digit code
            code = str(random.randint(1000, 9999))
            profile.verification_code = code
            profile.save()

            # Update user info if provided
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            user.save()

            return Response({
                "status": "success",
                "verification_code": code,
                "username": user.username
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
