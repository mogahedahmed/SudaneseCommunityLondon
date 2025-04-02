from django.contrib import admin
from .models import News, NewsImage

# ✅ عرض الصور داخل صفحة الخبر
class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1  # عدد الحقول الفارغة الجاهزة للإضافة

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)
    inlines = [NewsImageInline]  # ✅ ربط الصور

admin.site.register(News, NewsAdmin)
