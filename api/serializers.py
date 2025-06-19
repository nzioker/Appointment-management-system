from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProviderProfile, AvailableSlot, Appointment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProviderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProviderProfile
        fields = ['id', 'user', 'profession', 'contact']

class AvailableSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableSlot
        fields = ['id', 'time', 'provider']
        read_only_fields = ['provider']


from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    slot_time = serializers.DateTimeField(source='slot.time', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'slot_time']

