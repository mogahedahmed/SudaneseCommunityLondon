from django.utils.deprecation import MiddlewareMixin
from .models import Member

class LogoutOnBrowserCloseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        member_id = request.session.get('member_id')
        if member_id and not request.session.session_key:
            try:
                member = Member.objects.get(member_id=member_id)
                member.is_logged_in = False
                member.save()
            except Member.DoesNotExist:
                pass

    def process_response(self, request, response):
        # لو الجلسة انتهت أو لا تحتوي على بيانات، نسجل الخروج
        if not request.session.get('member_id') and hasattr(request, 'user') and not request.user.is_authenticated:
            member_id = request.COOKIES.get('member_id')
            if member_id:
                try:
                    member = Member.objects.get(member_id=member_id)
                    member.is_logged_in = False
                    member.save()
                except Member.DoesNotExist:
                    pass
        return response
