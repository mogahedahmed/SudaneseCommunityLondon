from django.db import models

class ContactInfo(models.Model):
    email = models.EmailField("البريد الإلكتروني")
    phone = models.CharField("الهاتف", max_length=20)
    whatsapp_link = models.URLField("رابط واتساب")
    address = models.CharField("العنوان", max_length=255)
    facebook = models.URLField("رابط فيسبوك", blank=True, null=True)
    twitter = models.URLField("رابط تويتر", blank=True, null=True)
    instagram = models.URLField("رابط إنستغرام", blank=True, null=True)

    def __str__(self):
        return "معلومات التواصل"
