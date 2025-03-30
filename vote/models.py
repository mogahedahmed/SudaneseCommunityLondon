from django.db import models
from django.utils import timezone

class Member(models.Model):
    member_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')])
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20, choices=[('أعزب', 'أعزب'), ('متزوج', 'متزوج')])
    family_members = models.PositiveIntegerField(default=0)

    # ✅ حقل أحقية التصويت
    CAN_VOTE_CHOICES = [('نعم', 'نعم'), ('لا', 'لا')]
    can_vote = models.CharField(max_length=5, choices=CAN_VOTE_CHOICES, default='نعم', verbose_name="أحقية التصويت")

    def __str__(self):
        return f"{self.full_name} ({self.member_id})"


class FamilyMember(models.Model):
    member = models.ForeignKey(Member, related_name='family_members_data', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')])
    age = models.PositiveIntegerField()
    relationship = models.CharField(max_length=50, verbose_name='صلة القرابة')

    def __str__(self):
        return f"{self.full_name} ({self.relationship})"


class VotingSession(models.Model):
    CATEGORY_CHOICES = [
        ('منصب إداري', 'منصب إداري'),
        ('قرار', 'قرار'),
        ('استبيان', 'استبيان'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, verbose_name="نوع التصويت (اكتب يدويًا)")
    
    # ✅ تم إضافة هذا الحقل لعرض تاريخ بداية التصويت
    created_at = models.DateTimeField(auto_now_add=True)
    
    expires_at = models.DateTimeField()

    def is_active(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.title} ({self.category})"


class VotingOption(models.Model):
    session = models.ForeignKey(VotingSession, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.text} ({self.session.title})"


class Vote(models.Model):
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE)
    option = models.ForeignKey(VotingOption, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'member_id')

    def __str__(self):
        return f"عضو {self.member_id} صوت لـ {self.option.text}"
