from django.shortcuts import render, get_object_or_404
from .models import Activity

def activities_view(request):
    activities = Activity.objects.order_by('-date')
    return render(request, 'activities/activities.html', {'activities': activities})

def activity_detail_view(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, 'activities/activity_detail.html', {'activity': activity})
