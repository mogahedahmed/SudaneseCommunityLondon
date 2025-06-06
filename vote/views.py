from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.template.response import TemplateResponse
from django.db.models import Count
from django.contrib.sessions.models import Session
from .models import VotingSession, VotingOption, Vote, Member, FamilyMember
from xhtml2pdf import pisa
import pandas as pd
from django.utils.timezone import now

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
            if member.is_rejected:
                messages.error(request, "❌ تم إيقاف حسابك. يرجى مراجعة إدارة الجالية.")
                return redirect('vote_login')
            if not member.is_approved:
                messages.error(request, "❌ حسابك قيد المراجعة. يرجى انتظار التفعيل من الإدارة.")
                return redirect('vote_login')
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            for session in sessions:
                try:
                    data = session.get_decoded()
                    if data.get('member_id') == member.member_id:
                        session.delete()
                except:
                    continue
            member.is_logged_in = True
            member.save()
            request.session.flush()
            request.session['member_id'] = member.member_id
            request.session['full_name'] = member.full_name
            request.session['phone'] = member.phone
            request.session['can_vote'] = member.can_vote
            return redirect('vote_page')
        except Member.DoesNotExist:
            messages.error(request, "❌ رقم العضوية أو كلمة المرور غير صحيحة.")
            return redirect('vote_login')
    return redirect('vote_login')

# صفحة التصويت لجميع الجلسات
def vote_page(request):
    member_id = request.session.get('member_id')
    full_name = request.session.get('full_name')
    phone = request.session.get('phone')
    can_vote = request.session.get('can_vote', 'لا')
    if not member_id or not phone:
        return redirect('vote_login')

    sessions = VotingSession.objects.all().order_by('expires_at')
    sessions_data = []

    if request.method == "POST":
        session_id = request.POST.get("session_id")
        option_id = request.POST.get("option")
        if not session_id or not option_id:
            messages.error(request, "يرجى تحديد خيار تصويت صالح.")
            return redirect('vote_page')
        try:
            session = VotingSession.objects.get(id=session_id)
        except VotingSession.DoesNotExist:
            messages.error(request, "جلسة التصويت غير موجودة.")
            return redirect('vote_page')
        if can_vote != "نعم":
            messages.error(request, "❌ لا يُسمح لك بالتصويت. يمكنك فقط مشاهدة النتائج.")
            return redirect('vote_page')
        if session.expires_at < now():
            messages.warning(request, f"⏰ انتهى وقت التصويت على {session.title}.")
            return redirect('vote_page')
        if session.start_at > now():
            messages.warning(request, f"⏰ لم يبدأ التصويت على {session.title} بعد.")
            return redirect('vote_page')
        already_voted = Vote.objects.filter(session=session, member_id=member_id).exists()
        if not already_voted:
            try:
                selected_option = VotingOption.objects.get(id=option_id, session=session)
                Vote.objects.create(session=session, option=selected_option, member_id=member_id, phone=phone)
                messages.success(request, f"✅ تم التصويت بنجاح في {session.title}")
            except VotingOption.DoesNotExist:
                messages.error(request, "الخيار المحدد غير صالح.")
        else:
            messages.info(request, f"✅ لقد قمت بالتصويت مسبقًا في {session.title}")
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
        'now': now(),
    })

# تسجيل الخروج
def logout_view(request):
    member_id = request.session.get('member_id')
    if member_id:
        try:
            member = Member.objects.get(member_id=member_id)
            member.is_logged_in = False
            member.save()
        except Member.DoesNotExist:
            pass
    session_key = request.session.session_key
    if session_key:
        try:
            Session.objects.get(session_key=session_key).delete()
        except Session.DoesNotExist:
            pass
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
    total = Vote.objects.filter(session=session).count()
    for r in results:
        r["percent"] = round((r["count"] / total) * 100, 2) if total > 0 else 0
    template = get_template("vote/pdf_template.html")
    html = template.render({'session': session, 'results': results})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vote_results.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

# نسخة الطباعة
def vote_snapshot_view(request):
    return render(request, 'vote/vote_snapshot.html')

# عرض الأعضاء في صفحة HTML
def members_list_view(request):
    members = Member.objects.all().order_by('full_name')
    return TemplateResponse(request, 'vote/members_list.html', {'members': members})

# تصدير الأعضاء إلى Excel
# تصدير الأعضاء إلى Excel (نسخة النهائية الصحيحة فقط)
def export_members_excel(request):
    members = Member.objects.all().order_by('full_name')
    data = []
    for member in members:
        data.append({
            "رقم العضوية": member.member_id,
            "الاسم الكامل": member.full_name,
            "الجنس": member.gender,
            "العمر": member.age,
            "الهاتف": member.phone,
            "البريد": member.email,
            "العنوان": member.address,
            "الحالة الاجتماعية": member.marital_status,
            "عدد أفراد العائلة": member.family_members,
            "أحقية التصويت": member.can_vote,
            "طريقة الدفع": member.payment_method,
            "فترة السداد": member.payment_period,
            "Institution Number": member.institution_number,
            "Transit Number": member.transit_number,
            "Account Number": member.account_number,
            "Bank Name": member.bank_name,
            "Account Name": member.account_name,
            "تمت الموافقة؟": "نعم" if member.is_approved else "لا",
            "تم الرفض؟": "نعم" if member.is_rejected else "لا",
            "تسجيل الدخول": "نعم" if member.is_logged_in else "لا",
        })

    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="members_list_full.xlsx"'
    df.to_excel(response, index=False)
    return response
    

# صفحة طباعة الأعضاء
def members_print_view(request):
    members = Member.objects.all()
    return render(request, 'vote/members_print.html', {'members': members})

# تسجيل عضوية جديدة
def register_member_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        if Member.objects.filter(email=email).exists():
            messages.error(request, "❌ البريد الإلكتروني مستخدم مسبقًا. يرجى مراجعة الإدارة.")
            return redirect('register_member')

        if Member.objects.filter(phone=phone).exists():
            messages.error(request, "❌ رقم الهاتف مستخدم مسبقًا. يرجى مراجعة الإدارة.")
            return redirect('register_member')

        member = Member.objects.create(
            member_id=request.POST.get('member_id'),
            full_name=request.POST.get('full_name'),
            gender=request.POST.get('gender'),
            address=request.POST.get('address'),
            age=request.POST.get('age'),
            email=email,
            phone=phone,
            password=request.POST.get('password'),
            marital_status=request.POST.get('marital_status'),
            family_members=request.POST.get('family_members') or 0,
            can_vote=request.POST.get('can_vote'),

            # ✅ الحقول الجديدة المضافة
            payment_method=request.POST.get('payment_method'),
            payment_period=request.POST.get('payment_period'),
            institution_number=request.POST.get('institution_number'),
            transit_number=request.POST.get('transit_number'),
            account_number=request.POST.get('account_number'),
            bank_name=request.POST.get('bank_name'),
            account_name=request.POST.get('account_name'),

            is_approved=False,
            is_rejected=False
        )

        # ✅ أفراد العائلة
        children_names = request.POST.getlist('child_name[]')
        children_genders = request.POST.getlist('child_gender[]')
        children_ages = request.POST.getlist('child_age[]')
        children_relations = request.POST.getlist('child_relation[]')

        for name, gender, age, relation in zip(children_names, children_genders, children_ages, children_relations):
            FamilyMember.objects.create(
                member=member,
                full_name=name,
                gender=gender,
                age=int(age),
                relationship=relation
            )

        messages.success(request, "✅ تم التسجيل بنجاح وسيتم تزويدك برقم العضوية عبر رسالة نصية أو البريد الإلكتروني، ومن ثم يمكنك تسجيل الدخول وممارسة حقوقك في التصويت.")
        return redirect('vote_login')

    return render(request, 'vote/register_member.html')
