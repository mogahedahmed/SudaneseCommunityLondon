from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Member

@receiver(post_delete, sender=Session)
def session_ended(sender, instance, **kwargs):
    data = instance.get_decoded()
    member_id = data.get('member_id')
    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            member.is_logged_in = False
            member.save()
        except Member.DoesNotExist:
            pass
