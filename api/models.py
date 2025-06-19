from django.db import models
from django.contrib.auth.models import User

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.profession})"

class AvailableSlot(models.Model):
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='slots')
    time = models.DateTimeField()

    class Meta:
        unique_together = ('provider', 'time')

    def __str__(self):
        return f"{self.provider} - {self.time}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    provider = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE)
    slot = models.OneToOneField(AvailableSlot, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} with {self.provider} at {self.slot.time}"
