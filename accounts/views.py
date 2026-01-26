from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ParentRegistrationForm, UserProfileForm, StudentForm
from .models import Student


def register(request):
    """Parent registration view."""
    if request.user.is_authenticated:
        return redirect('leagues:dashboard')

    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to HomeField! Add your children to get started.')
            return redirect('accounts:add_student')
    else:
        form = ParentRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'accounts/profile.html', {
        'form': form,
        'students': request.user.students.all()
    })


@login_required
def add_student(request):
    """Add a new student/child."""
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.parent = request.user
            student.save()
            messages.success(request, f'{student.full_name} has been added.')
            if 'add_another' in request.POST:
                return redirect('accounts:add_student')
            return redirect('accounts:profile')
    else:
        form = StudentForm()

    return render(request, 'accounts/student_form.html', {
        'form': form,
        'title': 'Add Child'
    })


@login_required
def edit_student(request, pk):
    """Edit an existing student."""
    student = get_object_or_404(Student, pk=pk, parent=request.user)

    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'{student.full_name} has been updated.')
            return redirect('accounts:profile')
    else:
        form = StudentForm(instance=student)

    return render(request, 'accounts/student_form.html', {
        'form': form,
        'title': 'Edit Child',
        'student': student
    })


@login_required
def delete_student(request, pk):
    """Delete a student."""
    student = get_object_or_404(Student, pk=pk, parent=request.user)

    if request.method == 'POST':
        name = student.full_name
        student.delete()
        messages.success(request, f'{name} has been removed.')
        return redirect('accounts:profile')

    return render(request, 'accounts/student_confirm_delete.html', {
        'student': student
    })
