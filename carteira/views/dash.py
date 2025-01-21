import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render




def desh(request):

    context = {
        
        
        }
    return render(request,'dash/dash.html', context)