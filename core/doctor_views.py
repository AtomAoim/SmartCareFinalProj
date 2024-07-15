from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from dashboards.models import Appointment
from dashboards.forms import AppointmentForm
from dashboards.models import Prescription


@login_required()
def doctor_home(request):
    doctor = request.user.doctor
    past_completed_appointments = Appointment.objects.filter(doctor=doctor,
                                                             status='Completed', )
    # Loop through past completed appointments and get associated prescriptions
    for appointment in past_completed_appointments:
        appointment.prescription = Prescription.objects.filter(appointment=appointment).first()

    upcoming_appointments = Appointment.objects.filter(doctor=doctor,
                                                       status='Approved',
                                                       )
    pending_appointments = Appointment.objects.filter(doctor=doctor,
                                                      status='Waiting for approval')

    context = {
        'past_completed_appointments': past_completed_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
    }

    return render(request, 'doctor_home.html', context)


@login_required()
def approve_doctor_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            appointment.status = 'Approved'
            appointment.save()
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason')
            appointment.status = f'Rejected:- {rejection_reason}'
            appointment.save()
        return redirect('doctor_home')

    return render(request, 'doctor_home.html', {'appointment': appointment})


@login_required()
def reject_doctor_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        reason = request.POST.get('reason')

        # Set status to Rejected and add reason for rejection
        appointment.status = 'Rejected'
        appointment.rejection_reason = reason
        appointment.save()

        return redirect('doctor_home')  # Redirect to doctor's home page

    return render(request, 'doctor_reject_appointment.html', {'appointment': appointment})


@login_required()
def update_doctor_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    form = AppointmentForm(request.POST or None, instance=appointment)
    if form.is_valid():
        form.save()
        return redirect('doctor_home')

    return render(request, 'doctor_update_appointment.html', {'form': form, 'appointment': appointment})
