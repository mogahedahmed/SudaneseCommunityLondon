from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.utils.encoding import smart_str
from django.db.models import Count
from .models import VotingSession, VotingOption, Vote, Member
from xhtml2pdf import pisa
import pandas as pd

# صفحة تسجيل الدخول
def vote_login(request):
    return render(request, 'vote/vote_login.html')

# التحقق من العضو وتخزين معلومات الجلسة
def vote_access(request):
    if request.method == "POST":
        member_id = request.POST.get('member_id')
        password = request.POST.get('password')

        try:
            member = Member.objects.get(member_id=member_id, password=password)
            request.session['member_id'] = member.member_id
            request.session['full_name'] = member.full_name
            request.session['phone'] = member.phone
            request.session['can_vote'] = member.can_vote
            return redirect('vote_page')
        except Member.DoesNotExist:
            return render(request, 'vote/vote_login.html', {'error': 'رقم العضوية أو كلمة المرور غير صحيحة!'})
    return redirect('vote_login')

# صفحة التصويت لجميع الجلسات النشطة
def vote_page(request):
    member_id = request.session.get('member_id')
    full_name = request.session.get('full_name')
    phone = request.session.get('phone')
    can_vote = request.session.get('can_vote', 'لا')

    if not member_id or not phone:
        return redirect('vote_login')

    sessions = VotingSession.objects.filter(expires_at__gt=timezone.now()).order_by('expires_at')
    sessions_data = []

    # منع التصويت يدويًا في حالة عدم الأهلية
    if request.method == "POST":
        if can_vote != "نعم":
            messages.error(request, "❌ لا يُسمح لك بالتصويت. يمكنك فقط مشاهدة النتائج.")
            return redirect('vote_page')

        session_id = request.POST.get("session_id")
        option_id = request.POST.get("option")
        session = VotingSession.objects.get(id=session_id)
        already_voted = Vote.objects.filter(session=session, member_id=member_id).exists()

        if not already_voted:
            selected_option = VotingOption.objects.get(id=option_id, session=session)
            Vote.objects.create(session=session, option=selected_option, member_id=member_id, phone=phone)
            messages.success(request, f"✅ تم التصويت بنجاح في {session.title}")
            return redirect('vote_page')

    for session in sessions:
        options = session.options.all()
        already_voted = Vote.objects.filter(session=session, member_id=member_id).exists()
        total_votes = Vote.objects.filter(session=session).count()

        results = (
            Vote.objects.filter(session=session)
            .values('option__text')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        for r in results:
            r["percent"] = round((r["count"] / total_votes) * 100, 2) if total_votes > 0 else 0

        sessions_data.append({
            'session': session,
            'options': options,
            'already_voted': already_voted,
            'results': results,
            'total_votes': total_votes,
        })

    return render(request, 'vote/vote.html', {
        'sessions_data': sessions_data,
        'full_name': full_name,
        'can_vote': can_vote,
    })

# تسجيل الخروج
def logout_view(request):
    request.session.flush()
    messages.info(request, "تم تسجيل الخروج بنجاح.")
    return redirect('vote_login')

# تصدير نتائج أول جلسة نشطة إلى Excel
def export_excel(request):
    session = VotingSession.objects.filter(expires_at__gt=timezone.now()).order_by('expires_at').first()
    if not session:
        return HttpResponse("لا توجد جلسة تصويت حالياً.")

    votes = (
        Vote.objects.filter(session=session)
        .values('option__text')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    df = pd.DataFrame(votes)
    df.rename(columns={"option__text": "الخيار", "count": "عدد الأصوات"}, inplace=True)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="vote_results.xlsx"'
    df.to_excel(response, index=False)
    return response

# تصدير النتائج إلى PDF
def export_pdf(request):
    session = VotingSession.objects.filter(expires_at__gt=timezone.now()).order_by('expires_at').first()
    if not session:
        return HttpResponse("لا توجد جلسة تصويت حالياً.")

    results = (
        Vote.objects.filter(session=session)
        .values('option__text')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    for r in results:
        total = Vote.objects.filter(session=session).count()
        r["percent"] = round((r["count"] / total) * 100, 2) if total > 0 else 0

    template = get_template("vote/pdf_template.html")
    html = template.render({'session': session, 'results': results})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vote_results.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

# عرض النسخة القابلة للطباعة من التصويت
def vote_snapshot_view(request):
    return render(request, 'vote/vote_snapshot.html')

# ✅ عرض الأعضاء في صفحة HTML
def members_list_view(request):
    members = Member.objects.all().order_by('full_name')
    return TemplateResponse(request, 'vote/members_list.html', {'members': members})

# ✅ تصدير الأعضاء إلى Excel
def export_members_excel(request):
    members = Member.objects.all().order_by('full_name')
    data = []

    for member in members:
        data.append({
            "رقم العضوية": member.member_id,
            "الاسم الكامل": member.full_name,
            "الهاتف": member.phone,
            "البريد": member.email,
            "الجنس": member.gender,
            "العمر": member.age,
            "الحالة الاجتماعية": member.marital_status,
            "عدد أفراد العائلة": member.family_members,
            "أحقية التصويت": member.can_vote,
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="members_list.xlsx"'
    df.to_excel(response, index=False)
    return response

def members_print_view(request):
    members = Member.objects.all()
    return render(request, 'vote/members_print.html', {'members': members})
