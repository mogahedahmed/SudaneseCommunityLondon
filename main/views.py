from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def activities(request):
    return render(request, 'main/activities/activities.html')

def contact(request):
    return render(request, 'main/contact/contact.html')
