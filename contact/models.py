from django.db import models

class ContactInfo(models.Model):
    email = models.EmailField("البريد الإلكتروني")
    phone = models.CharField("الهاتف", max_length=20)
    whatsapp_link = models.URLField(verbose_name="رابط واتساب")  # ✅ يجب أن يكون URL
    address = models.CharField("العنوان", max_length=255)

    def __str__(self):
        return "معلومات التواصل"
