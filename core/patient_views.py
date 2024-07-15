from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboards.models import Appointment
from loginAndRegistration.models import Doctor, Nurse
from dashboards.models import Prescription

@login_required()
def patient_home(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        nurse_id = request.POST.get('nurse')
        appointment_datetime = request.POST.get('appointment_datetime')
        status = "Waiting for approval"

        if doctor_id != '':
            doctor = Doctor.objects.filter(id=doctor_id)[0]
            Appointment.objects.create(doctor=doctor,
                                       patient=request.user.patient,
                                       appointment_datetime=appointment_datetime,
                                       status=status)
        else:
            nurse = Nurse.objects.filter(id=nurse_id)[0]
            Appointment.objects.create(
                nurse=nurse,
                patient=request.user.patient,
                appointment_datetime=appointment_datetime,
                status=status
            )

    # Retrieve past appointments
    past_appointments = Appointment.objects.filter(patient=request.user.patient,
                                                   status='Completed',
                                                   )
    # Loop through past completed appointments and get associated prescriptions
    for appointment in past_appointments:
        appointment.prescription = Prescription.objects.filter(appointment=appointment).first()

    # Retrieve upcoming appointments
    upcoming_approved_appointments = Appointment.objects.filter(patient=request.user.patient,
                                                                status='Approved',
                                                                )

    # Retrieve appointments needing approval
    pending_appointments = Appointment.objects.filter(patient=request.user.patient,
                                                      status='Waiting for approval',
                                                      )
    doctors = Doctor.objects.all()
    nurses = Nurse.objects.all()
    context = {
        'past_appointments': past_appointments,
        'upcoming_approved_appointments': upcoming_approved_appointments,
        'pending_appointments': pending_appointments,
        'doctors': doctors,
        'nurses': nurses,
    }

    return render(request, 'patient_home.html', context)


@login_required()
def repeat_appointment(request):
    from datetime import datetime
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        nurse_id = request.POST.get('nurse')
        appointment_datetime = datetime.strptime(request.POST.get('appointment_datetime').replace('.', ''), "%B %d, %Y, %I:%M %p")
        # Create a new appointment with the same details
        Appointment.objects.create(
            doctor_id=doctor_id,
            nurse_id=nurse_id,
            patient=request.user.patient,
            appointment_datetime=appointment_datetime,
            status="Waiting for approval"
        )
    return redirect('patient_home')