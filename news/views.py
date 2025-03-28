# news/views.py
from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request, category=None):
    if category:
        news = News.objects.filter(category=category).order_by('-created_at')
    else:
        news = News.objects.all().order_by('-created_at')

    return render(request, 'news/news_list.html', {
        'news': news,
        'category': category
    })  # ← تم إغلاق القوس هنا

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})
