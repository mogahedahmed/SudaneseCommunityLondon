from django.db import models
from django.urls import reverse  # ← مهم لإرجاع رابط التفاصيل

class News(models.Model):
    CATEGORY_CHOICES = [
        ('فرص عمل', 'فرص عمل'),
        ('أخبار الوفيات', 'أخبار الوفيات'),
        ('أخبار رياضية', 'أخبار رياضية'),
        ('أخبار الجالية', 'أخبار الجالية'),
    ]

    title = models.CharField(max_length=200, verbose_name='العنوان')
    content = models.TextField(verbose_name='المحتوى')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='الفئة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ النشر')

    def __str__(self):
        return f"{self.title} - {self.category}"

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.pk)])


# ✅ نموذج صور متعددة مرتبطة بالخبر
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images', verbose_name='الخبر')
    image = models.ImageField(upload_to='news_images/', verbose_name='صورة')

    def __str__(self):
        return f"صورة للخبر: {self.news.title}"
