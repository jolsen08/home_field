from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Student


class ParentRegistrationForm(UserCreationForm):
    """Form for parent registration."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone',
                  'city', 'state', 'zip_code', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'parent'
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form with styling."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'state', 'zip_code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StudentForm(forms.ModelForm):
    """Form for adding/editing student profiles."""
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'date_of_birth', 'gender',
                  'grade_level', 'sport_interests', 'medical_notes',
                  'emergency_contact', 'emergency_phone']
        widgets = {
            'sport_interests': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'date_of_birth':
                continue
            elif field_name == 'sport_interests':
                field.label = "What sports is your child interested in?"
            else:
                field.widget.attrs['class'] = 'form-control'
