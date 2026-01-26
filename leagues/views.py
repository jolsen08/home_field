import csv
from pathlib import Path
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from .models import League, Sport, Region, Season, AgeGroup, Registration
from .forms import LeagueSearchForm, RegistrationForm
from accounts.models import Student


def load_demo_leagues():
    """Load sample leagues from CSV for demo purposes."""
    csv_path = settings.BASE_DIR / 'data' / 'sample_leagues.csv'
    leagues = []

    if csv_path.exists():
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                leagues.append({
                    'name': row['name'],
                    'sport': row['sport'],
                    'city': row['city'],
                    'state': row['state'],
                    'age_group': f"{row['age_group_name']} (Ages {row['age_min']}-{row['age_max']})",
                    'fee': float(row['fee']),
                    'max_participants': int(row['max_participants']),
                    'spots_remaining': int(row['max_participants']) - 12,  # Simulate some signups
                    'schedule_info': row['schedule_info'],
                    'description': row['description'],
                })

    return leagues


def home(request):
    """Homepage view."""
    sports = Sport.objects.filter(is_active=True)[:6]
    featured_leagues = League.objects.filter(status='open')[:4]

    return render(request, 'leagues/home.html', {
        'sports': sports,
        'featured_leagues': featured_leagues
    })


def league_list(request):
    """Browse all available leagues."""
    form = LeagueSearchForm(request.GET)
    leagues = League.objects.filter(status='open')

    if request.GET.get('sport'):
        leagues = leagues.filter(sport_id=request.GET['sport'])
    if request.GET.get('region'):
        leagues = leagues.filter(region_id=request.GET['region'])
    if request.GET.get('season'):
        leagues = leagues.filter(season_id=request.GET['season'])
    if request.GET.get('age_group'):
        leagues = leagues.filter(age_group_id=request.GET['age_group'])

    return render(request, 'leagues/league_list.html', {
        'form': form,
        'leagues': leagues
    })


def league_detail(request, pk):
    """League detail view."""
    league = get_object_or_404(League, pk=pk)

    user_registrations = []
    if request.user.is_authenticated:
        user_registrations = Registration.objects.filter(
            league=league,
            parent=request.user
        ).select_related('student')

    return render(request, 'leagues/league_detail.html', {
        'league': league,
        'user_registrations': user_registrations
    })


@login_required
def register_for_league(request, pk):
    """Register a student for a league."""
    league = get_object_or_404(League, pk=pk)

    if league.status != 'open':
        messages.error(request, 'This league is not open for registration.')
        return redirect('leagues:league_detail', pk=pk)

    if not request.user.students.exists():
        messages.warning(request, 'Please add a child before registering for leagues.')
        return redirect('accounts:add_student')

    if request.method == 'POST':
        form = RegistrationForm(request.user, request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student']
            student = get_object_or_404(Student, pk=student_id, parent=request.user)

            if Registration.objects.filter(league=league, student=student).exists():
                messages.error(request, f'{student.full_name} is already registered for this league.')
                return redirect('leagues:league_detail', pk=pk)

            if student.age < league.age_group.min_age or student.age > league.age_group.max_age:
                messages.error(request, f'{student.full_name} does not meet the age requirements for this league.')
                return redirect('leagues:league_detail', pk=pk)

            status = 'waitlist' if league.is_full else 'confirmed'
            Registration.objects.create(
                league=league,
                student=student,
                parent=request.user,
                status=status,
                notes=form.cleaned_data.get('notes', '')
            )

            if status == 'waitlist':
                messages.info(request, f'{student.full_name} has been added to the waitlist.')
            else:
                messages.success(request, f'{student.full_name} has been registered for {league.name}!')

            return redirect('leagues:league_detail', pk=pk)
    else:
        form = RegistrationForm(request.user)

    return render(request, 'leagues/register.html', {
        'form': form,
        'league': league
    })


@login_required
def cancel_registration(request, pk):
    """Cancel a registration."""
    registration = get_object_or_404(Registration, pk=pk, parent=request.user)

    if request.method == 'POST':
        league = registration.league
        student_name = registration.student.full_name
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, f'Registration for {student_name} has been cancelled.')
        return redirect('leagues:league_detail', pk=league.pk)

    return render(request, 'leagues/cancel_registration.html', {
        'registration': registration
    })


@login_required
def dashboard(request):
    """Parent dashboard."""
    students = request.user.students.all()
    active_registrations = Registration.objects.filter(
        parent=request.user,
        status__in=['confirmed', 'pending', 'waitlist']
    ).select_related('league', 'student', 'league__sport', 'league__season')

    return render(request, 'leagues/dashboard.html', {
        'students': students,
        'registrations': active_registrations
    })


@login_required
def my_registrations(request):
    """View all registrations for the current user."""
    registrations = Registration.objects.filter(
        parent=request.user
    ).select_related('league', 'student', 'league__sport', 'league__season', 'league__region')

    return render(request, 'leagues/my_registrations.html', {
        'registrations': registrations
    })


def demo_leagues(request):
    """Demo page showing what leagues will look like."""
    leagues = load_demo_leagues()

    # Get unique values for filters
    sports = sorted(set(l['sport'] for l in leagues))
    locations = sorted(set(f"{l['city']}, {l['state']}" for l in leagues))

    # Apply filters if provided
    sport_filter = request.GET.get('sport', '')
    location_filter = request.GET.get('location', '')

    if sport_filter:
        leagues = [l for l in leagues if l['sport'] == sport_filter]
    if location_filter:
        leagues = [l for l in leagues if f"{l['city']}, {l['state']}" == location_filter]

    return render(request, 'leagues/demo_list.html', {
        'leagues': leagues,
        'sports': sports,
        'locations': locations,
        'sport_filter': sport_filter,
        'location_filter': location_filter,
    })


def demo_league_detail(request, index):
    """Demo page showing what a league detail page will look like."""
    leagues = load_demo_leagues()

    if 0 <= index < len(leagues):
        league = leagues[index]
        league['index'] = index
    else:
        league = None

    return render(request, 'leagues/demo_detail.html', {
        'league': league,
    })
