from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for HomeField platform."""
    ROLE_CHOICES = [
        ('parent', 'Parent'),
        ('admin', 'League Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=50, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    @property
    def is_parent(self):
        return self.role == 'parent'

    @property
    def is_league_admin(self):
        return self.role == 'admin'


class Student(models.Model):
    """Student/child profile linked to a parent user."""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grade_level = models.CharField(max_length=20, blank=True)
    sport_interests = models.ManyToManyField(
        'leagues.Sport',
        blank=True,
        related_name='interested_students',
        help_text="Sports this child is interested in"
    )
    medical_notes = models.TextField(blank=True, help_text="Any allergies or medical conditions")
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
