from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('category', 'created_at')
    ordering = ('-created_at',)

admin.site.register(News, NewsAdmin)
