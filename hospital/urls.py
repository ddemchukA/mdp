from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'incident/', views.incident, name="incident"),
    path(r'lpu/', views.lpu, name="lpu"),
    path(r'expertins/', views.expertins, name="expertins"),
    path(r'study_insult/',views.studyins,name="studyins"),
    path('accounts/login/', views.LoginView, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('pac/', views.pac, name='pac'),
    path('findeva/', views.findeva, name='findeva'),
    path(r'data_ins/',views.datains,name="datains"),
    path(r'newevac/<int:pac_id>/',views.newevac,name='newevac'),
    path('new_pac/', views.new_pac, name='new_pac'),
    path('now_eva/', views.now_eva, name='now_eva'),
    path(r'new_bef/<int:case_id>/',views.new_bef,name='new_bef'),
    path(r'delbef/<int:caseid>/',views.delbef,name='delbef'),
    path(r'begin/<int:caseid>/',views.begin,name='begin'),
    path(r'delcase/<int:caseid>/',views.delcase,name='delcase'),
    path(r'newint/<int:case_id>/',views.newint,name='newint'),
    path(r'newaft/<int:case_id>/',views.newaft,name='newaft'),
    path(r'delint/<int:intid>/<int:caseid>',views.delint,name='delint'),
    path(r'newdost/<int:caseid>/',views.newdost,name='newdost'),
    path(r'showeva/<int:caseid>/<int:flag>/',views.showeva,name='showeva'),
    path(r'closecase/<int:caseid>/',views.closecase,name='closecase'),
    path(r'delaft/<int:caseid>/',views.delaft,name='delaft'),
    path(r'deldost/<int:dostid>/<int:caseid>/',views.deldost,name='deldost'),
    path(r'editpac/<int:pacid>/',views.editpac,name='editpac'),
    path(r'deadvputi/<int:caseid>/<int:pacid>/',views.deadvputi,name='deadvputi'),
    path(r'komglas',views.komglas,name='komglas'),
]
