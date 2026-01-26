from django import forms
from .models import Registration


class LeagueSearchForm(forms.Form):
    """Form for searching/filtering leagues."""
    sport = forms.ChoiceField(choices=[('', 'All Sports')], required=False)
    region = forms.ChoiceField(choices=[('', 'All Regions')], required=False)
    season = forms.ChoiceField(choices=[('', 'All Seasons')], required=False)
    age_group = forms.ChoiceField(choices=[('', 'All Age Groups')], required=False)

    def __init__(self, *args, **kwargs):
        from .models import Sport, Region, Season, AgeGroup
        super().__init__(*args, **kwargs)

        self.fields['sport'].choices = [('', 'All Sports')] + [
            (s.id, s.name) for s in Sport.objects.filter(is_active=True)
        ]
        self.fields['region'].choices = [('', 'All Regions')] + [
            (r.id, str(r)) for r in Region.objects.filter(is_active=True)
        ]
        self.fields['season'].choices = [('', 'All Seasons')] + [
            (s.id, str(s)) for s in Season.objects.all()[:8]
        ]
        self.fields['age_group'].choices = [('', 'All Age Groups')] + [
            (a.id, str(a)) for a in AgeGroup.objects.all()
        ]

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-select'


class RegistrationForm(forms.ModelForm):
    """Form for registering a student for a league."""
    student = forms.ChoiceField(choices=[])

    class Meta:
        model = Registration
        fields = ['student', 'notes']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].choices = [
            (s.id, str(s)) for s in user.students.all()
        ]
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
