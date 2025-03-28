from django.db import models
from django.utils import timezone  # ✅ استيراد timezone بشكل صحيح

class Activity(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان النشاط")
    description = models.TextField(verbose_name="تفاصيل النشاط")
    image = models.ImageField(upload_to='activities/', blank=True, null=True, verbose_name="صورة النشاط")
    date = models.DateField(default=timezone.now, verbose_name="تاريخ النشاط")  # ✅ التاريخ الافتراضي هو الآن

    def __str__(self):
        return self.title
