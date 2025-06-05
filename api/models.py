from django.db import models
from django.contrib.auth.models import User

class Provider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username} with {self.provider.name} at {self.time}'
