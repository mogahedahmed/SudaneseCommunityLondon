
from django.contrib import admin
from django.http import HttpResponse
from .models import Member, VotingSession, VotingOption, Vote, FamilyMember
from django.db.models import Count
import pandas as pd
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors
from io import BytesIO
from django.urls import path, reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1


class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'member_id', 'full_name', 'email', 'phone', 'gender',
        'age', 'marital_status', 'family_members', 'can_vote',
        'is_logged_in', 'is_approved', 'is_rejected', 'print_button'
    )
    search_fields = ('member_id', 'full_name', 'email', 'phone')
    list_filter = ('gender', 'marital_status', 'can_vote', 'is_logged_in', 'is_approved', 'is_rejected')
    inlines = [FamilyMemberInline]
    readonly_fields = ('member_id',)

    def print_button(self, obj):
        url = reverse('members_print')
        return format_html('<a class="button" href="{}" target="_blank">🖨️ طباعة</a>', url)
    print_button.short_description = "طباعة الأعضاء"


class VotingOptionInline(admin.TabularInline):
    model = VotingOption
    extra = 1


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    readonly_fields = ('member_id', 'get_member_name', 'option', 'timestamp')
    can_delete = False

    def get_member_name(self, obj):
        try:
            member = Member.objects.get(member_id=obj.member_id)
            return member.full_name
        except Member.DoesNotExist:
            return obj.member_id
    get_member_name.short_description = "اسم العضو"


@admin.action(description="📄 تصدير الأصوات المحددة إلى PDF")
def export_votes_pdf(modeladmin, request, queryset):
    pdfmetrics.registerFont(TTFont('ArabicFont', 'static/fonts/Amiri-Regular.ttf'))

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = 'ArabicFont'
    style.fontSize = 12
    style.alignment = TA_RIGHT

    data = [[
        Paragraph("اسم العضو", style),
        Paragraph("الخيار", style),
        Paragraph("الجلسة", style),
        Paragraph("التاريخ", style)
    ]]

    for vote in queryset:
        try:
            member = Member.objects.get(member_id=vote.member_id)
            name = member.full_name
        except Member.DoesNotExist:
            name = vote.member_id

        row = [
            Paragraph(str(name), style),
            Paragraph(str(vote.option), style),
            Paragraph(str(vote.session), style),
            Paragraph(vote.timestamp.strftime("%Y-%m-%d %H:%M"), style)
        ]
        data.append(row)

    table = Table(data, colWidths=[120, 160, 160, 100])
    table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'ArabicFont'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#d32f2f")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ]))

    doc.build([table])
    buffer.seek(0)

    return HttpResponse(buffer, content_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="selected_votes_table.pdf"'
    })


@admin.action(description="📄 تصدير الأصوات المحددة إلى Excel")
def export_votes_excel(modeladmin, request, queryset):
    rows = []
    for vote in queryset:
        try:
            member = Member.objects.get(member_id=vote.member_id)
            name = member.full_name
        except Member.DoesNotExist:
            name = vote.member_id

        rows.append({
            "اسم العضو": name,
            "الخيار": str(vote.option),
            "الجلسة": str(vote.session),
            "التاريخ": vote.timestamp.strftime("%Y-%m-%d %H:%M"),
        })

    df = pd.DataFrame(rows)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="selected_votes.xlsx"'
    df.to_excel(response, index=False)
    return response


@admin.action(description="❌ إلغاء التصويت المحدد")
def cancel_vote(modeladmin, request, queryset):
    count = queryset.count()
    queryset.delete()
    modeladmin.message_user(request, f"✅ تم إلغاء {count} تصويت/ات بنجاح.")


class VotingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_at', 'expires_at', 'view_results_link')
    inlines = [VotingOptionInline, VoteInline]

    def view_results_link(self, obj):
        url = reverse('admin:vote_voting-session-results', args=[obj.id])
        return format_html('<a class="button" href="{}" target="_blank">📄 عرض النتائج للطباعة</a>', url)

    view_results_link.short_description = "نتائج الطباعة"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:session_id>/results/', self.admin_site.admin_view(self.session_results_view), name='vote_voting-session-results'),
        ]
        return custom_urls + urls

    def session_results_view(self, request, session_id):
        session = VotingSession.objects.get(id=session_id)
        votes = Vote.objects.filter(session=session)

        for vote in votes:
            try:
                vote.member_name = Member.objects.get(member_id=vote.member_id).full_name
            except:
                vote.member_name = vote.member_id

        return TemplateResponse(request, "vote/session_results.html", {
            'session': session,
            'votes': votes,
        })


class VoteAdmin(admin.ModelAdmin):
    list_display = ('member_name_display', 'option', 'session', 'timestamp')
    list_filter = ('session',)
    search_fields = ('member_id', 'option__text', 'session__title')
    actions = [export_votes_excel, export_votes_pdf, cancel_vote]

    def member_name_display(self, obj):
        try:
            member = Member.objects.get(member_id=obj.member_id)
            return member.full_name
        except Member.DoesNotExist:
            return obj.member_id
    member_name_display.short_description = "اسم العضو"


admin.site.register(Member, MemberAdmin)
admin.site.register(VotingSession, VotingSessionAdmin)
admin.site.register(Vote, VoteAdmin)
