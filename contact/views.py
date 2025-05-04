from django.shortcuts import render
from .models import ContactInfo

def contact_view(request):
    contact = ContactInfo.objects.first()
    
    social_links = {
        'facebook': contact.facebook if contact else '',
        'twitter': contact.twitter if contact else '',
        'instagram': contact.instagram if contact else '',
    }

    return render(request, 'contact/contact.html', {
        'contact': contact,
        'social_links': social_links,
    })
