from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny

from .models import ProviderProfile, AvailableSlot, Appointment
from .serializers import (
    UserSerializer, ProviderProfileSerializer,
    AvailableSlotSerializer, AppointmentSerializer
)

class SignupUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=400)

        user = User.objects.create_user(username=username, password=password)

        login(request, user)

        return Response({
            'message': 'User account created.',
            'username': user.username,
            'role': 'user'
        }, status=201)


class SignupProviderView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        profession = request.data.get('profession')
        contact = request.data.get('contact')

        if not all([username, password, profession, contact]):
            return Response({'error': 'All provider fields are required.'}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken.'}, status=400)

        user = User.objects.create_user(username=username, password=password)
        ProviderProfile.objects.create(user=user, profession=profession, contact=contact)

        login(request, user)

        return Response({
            'message': 'Provider account created.',
            'username': user.username,
            'role': 'provider'
        }, status=201)



@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'message': 'CSRF cookie set'})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        selected_role = request.data.get('role')  # Comes from frontend

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check role mismatch
            is_provider = hasattr(user, 'providerprofile')
            if selected_role == 'provider' and not is_provider:
                return Response({'error': 'This user is not registered as a provider'}, status=403)
            if selected_role == 'user' and is_provider:
                return Response({'error': 'This account belongs to a provider'}, status=403)

            login(request, user)
            role = 'provider' if is_provider else 'user'
            return Response({
                'message': 'Login successful',
                'username': user.username,
                'role': role
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
    
class ProviderListView(generics.ListAPIView):
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer
    permission_classes = [permissions.AllowAny]

class SlotCreateView(generics.CreateAPIView):
    queryset = AvailableSlot.objects.all()
    serializer_class = AvailableSlotSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        provider = ProviderProfile.objects.get(user=self.request.user)
        serializer.save(provider=provider)

class SlotListView(generics.ListAPIView):
    serializer_class = AvailableSlotSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        provider_id = self.request.query_params.get('provider_id')
        now = timezone.now()
        return AvailableSlot.objects.filter(
            provider_id=provider_id,
            time__gte=now
        ).exclude(
            appointment__isnull=False
        )


class AppointmentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        slot_id = request.data.get('slot_id')
        try:
            slot = AvailableSlot.objects.get(id=slot_id)
            if Appointment.objects.filter(slot=slot).exists():
                return Response({'error': 'Slot already booked'}, status=400)
            Appointment.objects.create(user=request.user, provider=slot.provider, slot=slot)
            return Response({'message': 'Appointment booked successfully'}, status=201)
        except AvailableSlot.DoesNotExist:
            return Response({'error': 'Slot not found'}, status=404)

class AppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # If provider, return their appointments
        if hasattr(user, 'providerprofile'):
            return Appointment.objects.filter(provider__user=user)
        # Otherwise, return user's own appointments
        return Appointment.objects.filter(user=user)



class ProviderAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        provider = ProviderProfile.objects.get(user=self.request.user)
        return Appointment.objects.filter(provider=provider).order_by('slot__time')


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out'})
