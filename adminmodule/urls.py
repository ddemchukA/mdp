from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('lpufrom/', views.lpufrom, name='lpufrom'),
    path('lpudost/', views.lpudost, name='lpudost'),
    path('newlpfrom/', views.newlpfrom, name='newlpfrom'),
    path('newlpbd/', views.newlpbd, name='newlpbd'),
    path('newsrmp/', views.newsrmp, name='newsrmp'),
    path('editflp/<int:idlpu>/', views.editflp, name='editflp'),
    path('editlpbd/<int:idlpu>/', views.editlpbd, name='editlpbd'),
    path('editsrmp/<int:idlpu>/', views.editsrmp, name='editsrmp'),
    path('srmpl/', views.srmpl, name='srmpl'),
    path('evado/', views.evado, name='evado'),
    path('about/<int:idev>/', views.about, name='about'),
    path('us/', views.use, name='use'),
    path('newus/', views.newus, name='newus'),
    path('blcus/<int:usid>/<int:deist>/', views.blcus, name='blcus'),
    path('chpass/<int:idus>/', views.chpass, name='chpass'),
    path('chdata/<int:idus>/', views.chdata, name='chdata'),
    path('stat/', views.stat, name='stat'),
    path('statotch/<int:idotch>/', views.statotch, name='statotch'),
]
