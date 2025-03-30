from django.utils.deprecation import MiddlewareMixin
from .models import Member

class LogoutOnBrowserCloseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.session.session_key:
            return

        member_id = request.session.get('member_id')
        if member_id and not request.session.exists(request.session.session_key):
            try:
                member = Member.objects.get(member_id=member_id)
                member.is_logged_in = False
                member.save()
            except Member.DoesNotExist:
                pass
