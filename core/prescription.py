from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from dashboards.models import Appointment
from dashboards.forms import PrescriptionForm
from dashboards.models import Prescription


@login_required
def create_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    if request.method == 'POST':
        Prescription.objects.create(
            appointment=appointment,
            issue_datetime=appointment.appointment_datetime,
            medication_details=request.POST.get('medication_details', 'No Prescription required')
        )

        # Mark the appointment as completed
        appointment.status = 'Completed'
        appointment.save()
        return redirect('home')
    else:
        form = PrescriptionForm()
    return render(request, 'create_prescription.html', {'form': form})


@login_required
def update_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('view_prescription', prescription_id=prescription_id)
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'update_prescription.html', {'form': form, 'prescription': prescription})


@login_required
def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, pk=prescription_id)
    return render(request, 'view_prescription.html', {'prescription': prescription})
