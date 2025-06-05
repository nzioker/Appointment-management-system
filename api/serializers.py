from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Provider, Appointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['id', 'name']

class AppointmentSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.name', read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'provider', 'provider_name', 'time']