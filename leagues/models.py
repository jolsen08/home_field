from django.db import models
from django.conf import settings


class Sport(models.Model):
    """Sport types available in the platform."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Region(models.Model):
    """Geographic regions for organizing leagues."""
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_codes = models.TextField(help_text="Comma-separated list of zip codes in this region")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['state', 'city']
        unique_together = ['city', 'state']

    def __str__(self):
        return f"{self.name} ({self.city}, {self.state})"

    def get_zip_code_list(self):
        return [z.strip() for z in self.zip_codes.split(',')]


class Season(models.Model):
    """Season for organizing leagues by time period."""
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
    ]

    name = models.CharField(max_length=10, choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    registration_open = models.DateField()
    registration_close = models.DateField()

    class Meta:
        ordering = ['-year', 'name']
        unique_together = ['name', 'year']

    def __str__(self):
        return f"{self.get_name_display()} {self.year}"

    @property
    def is_registration_open(self):
        from datetime import date
        today = date.today()
        return self.registration_open <= today <= self.registration_close


class AgeGroup(models.Model):
    """Age divisions for leagues."""
    name = models.CharField(max_length=50)
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['min_age']

    def __str__(self):
        return f"{self.name} (Ages {self.min_age}-{self.max_age})"


class League(models.Model):
    """A league for a specific sport, region, season, and age group."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open for Registration'),
        ('closed', 'Registration Closed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=200)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='leagues')
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='leagues')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='leagues')
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE, related_name='leagues')

    description = models.TextField(blank=True)
    max_participants = models.PositiveIntegerField(default=50)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    location = models.CharField(max_length=200, blank=True)
    schedule_info = models.TextField(blank=True, help_text="Practice days/times and game schedule info")

    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='coordinated_leagues'
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['season', 'sport', 'age_group']

    def __str__(self):
        return f"{self.name} - {self.season}"

    @property
    def spots_remaining(self):
        return max(0, self.max_participants - self.registrations.filter(status='confirmed').count())

    @property
    def is_full(self):
        return self.spots_remaining == 0


class Registration(models.Model):
    """Registration of a student for a league."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('waitlist', 'Waitlist'),
        ('cancelled', 'Cancelled'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, related_name='registrations')
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='registrations')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ['league', 'student']

    def __str__(self):
        return f"{self.student} - {self.league}"
