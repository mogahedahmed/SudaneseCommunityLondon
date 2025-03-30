from django.urls import path
from . import views

urlpatterns = [
    # تسجيل الدخول والخروج
    path('', views.vote_login, name='vote_login'),
    path('access/', views.vote_access, name='vote_access'),
    path('page/', views.vote_page, name='vote_page'),
    path('logout/', views.logout_view, name='vote_logout'),

    # تصدير نتائج التصويت
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),

    # نسخة للطباعة من التصويت
    path('vote/snapshot/', views.vote_snapshot_view, name='vote_snapshot'),

    # إدارة الأعضاء
    path('members/', views.members_list_view, name='members_list'),
    path('members/export/', views.export_members_excel, name='export_members_excel'),
    path('members/print/', views.members_print_view, name='members_print'),

    # نسخة الطباعة للأعضاء من لوحة الإدارة
    path('admin/members/print/', views.members_print_view, name='admin_members_print'),
]
