from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Member(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('VOID CHEQUE', 'VOID CHEQUE'),
        ('E-TRANSFER', 'E-TRANSFER'),
        ('CASH', 'CASH'),
    ]

    PAYMENT_PERIOD_CHOICES = [
        ('شهري', 'شهري'),
        ('سنوي', 'سنوي'),
    ]

    member_id = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('ذكر', 'ذكر'), ('أنثى', 'أنثى')])
    address = models.CharField(max_length=255, blank=True)
    age = models.PositiveIntegerField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=50)

    marital_status = models.CharField(max_length=20, choices=[
        ('أعزب', 'أعزب'),
        ('متزوج', 'متزوج'),
        ('طالب', 'طالب')
    ])
    family_members = models.PositiveIntegerField(default=0)
    can_vote = models.CharField(max_length=5, choices=[('نعم', 'نعم'), ('لا', 'لا')], default='نعم')

    # 🔻 الحقول الجديدة لطريقة الدفع
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    payment_period = models.CharField(max_length=10, choices=PAYMENT_PERIOD_CHOICES, blank=True)
    institution_number = models.CharField(max_length=20, blank=True)
    transit_number = models.CharField(max_length=20, blank=True)
    account_number = models.CharField(max_length=20, blank=True)
    bank_name = models.CharField(max_length=100, blank=True)
    account_name = models.CharField(max_length=100, blank=True)

    is_logged_in = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False, verbose_name="تمت الموافقة؟")
    is_rejected = models.BooleanField(default=False, verbose_name="تم الرفض؟")

    def __str__(self):
        return f"{self.full_name} ({self.member_id})"

@receiver(pre_save, sender=Member)
def generate_member_id(sender, instance, **kwargs):
    if not instance.member_id:
        last_member = Member.objects.order_by('-id').first()
        last_number = int(last_member.member_id.replace("M", "")) if last_member and last_member.member_id else 0
        instance.member_id = f"M{last_number + 1:04d}"

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
    start_at = models.DateTimeField(default=timezone.now, verbose_name="وقت بداية التصويت")
    expires_at = models.DateTimeField(verbose_name="وقت انتهاء التصويت")

    def is_active(self):
        return self.start_at <= timezone.now() < self.expires_at

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
