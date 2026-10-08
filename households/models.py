from django.db import models
from django.contrib.auth.models import User
import secrets

class Household(models.Model):
    name = models.CharField(max_length=255)
    invite_code = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

               
    def __str__(self):
        return self.name


class HouseholdMember(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Member'),
    ]

    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='household_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('household', 'user')  # prevents joining the same household twice

    def __str__(self):
        return f"{self.user.username} in {self.household.name} ({self.role})"