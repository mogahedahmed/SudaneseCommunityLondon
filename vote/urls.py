from django.urls import path
from . import views

urlpatterns = [
    path('', views.vote_login, name='vote_login'),
    path('access/', views.vote_access, name='vote_access'),
    path('page/', views.vote_page, name='vote_page'),
    path('logout/', views.logout_view, name='vote_logout'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('vote/snapshot/', views.vote_snapshot_view, name='vote_snapshot'),

    # ✅ عرض الأعضاء في صفحة HTML
    path('members/', views.members_list_view, name='members_list'),

    # ✅ تصدير الأعضاء إلى Excel
    path('members/export/', views.export_members_excel, name='export_members_excel'),
    path('members/print/', views.members_print_view, name='members_print'),
    path('admin/members/print/', views.members_print_view, name='members_print')

]
