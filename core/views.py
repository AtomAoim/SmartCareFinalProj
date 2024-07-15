from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
# Create your views here.
from django.shortcuts import render

from .doctor_views import *
from .patient_views import *
from .nurse_view import *
from .prescription import *


def home(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'patient'):
            return redirect('patient_home')
        elif hasattr(request.user, 'doctor'):
            return redirect('doctor_home')
        elif hasattr(request.user, 'nurse'):
            return redirect('nurse_home')
        else:
            return render(request, 'home.html')

    return render(request, 'home.html')
