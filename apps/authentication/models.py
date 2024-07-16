from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TEAM_CHOICES = [
        ('comptable', 'Équipe comptable'),
        ('commercial', 'Équipe commerciale'),
        ('direction', 'Équipe de direction'),
    ]
    team = models.CharField(max_length=20, choices=TEAM_CHOICES, blank=True, null=True)
    def __str__(self):
        return self.username