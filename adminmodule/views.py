from django.shortcuts import render, redirect
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
import re
import smtplib
from datetime import datetime, date, time
from keras.models import load_model
from pandas import read_csv, DataFrame, Series
import pandas as pd
import numpy as np
import keras
import h5py# грузим пкет отвечающий за файлы hdf5
from .forms import insform, insformstudy,LoginForm,SearchForm, NP, NE, Dostav,SearchForm1,Priem,newlp, newlpbdform, newsrmpf, nfus, chps
from .models import Insultik,patient,case, before, atributes, after, intime,intimetime,dostavlen,deadinroad, Profile, lpubd, fromlpu, srmp
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('/adminmodule')

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.user_profile.is_superman:
                        return redirect('/adminmodule/lpufrom')
                    else:
                        return HttpResponse('<h1 align=\"center\">Неизвестный профиль <a href=\"/adminmodule/logout\">НАЗАД</a></h1>')
                else:
                    return HttpResponse('Акаунт закрыт')
            else:
                return HttpResponse('Логин или пароль неверны!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def blcus(request,usid,deist):
    user=User.objects.get(pk=usid)
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if user.user_profile.is_superman or user.is_superuser:
        return HttpResponse('Недостаточно прав для блокировки этого пользователя!')
    if deist==1:
        user.is_active=False
        user.save()
    if deist==0:
        user.is_active=True
        user.save()
    return redirect('/adminmodule/us')

def checkin(p1,p2,us,ev,com,id):
    str='success'
    str1=''
    if p1 != p2:
        str1=str1+' '+'Введенные пароли не совпадают'
    if not re.match(r'[A-Za-z0-9]',us):
        str1=str1+' '+'Имя пользователя содержит недопустимые символы'
    if ev is None and com is None:
        str1=str1+' '+'Не выбрана ни одна категория'
    if id is None:
        str1=str1+' '+'Не выбрано ЛПУ'
    if str1 != '':
        str=str1
    return str

@login_required
def stat(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    arg={}
    return render(request, 'templadm/stat.html',arg)


@login_required
def chdata(request,idus):
    arg={}
    lp=User.objects.get(pk=idus)
    fl=0
    if lp.user_profile.is_list_doctor:
        ab=case.objects.filter(id_vrach_id=idus).count()
        if ab>0:
            fl=1
    if lp.user_profile.is_commit_doctor:
        aa=dostavlen.objects.filter(us_id=idus).count()
        if aa>0:
            fl=1
    if fl == 0:
        splpu=lpubd.objects.all().order_by('name')
        arg['splpu']=splpu
    if lp.user_profile.is_superman or lp.is_superuser:
        return HttpResponse('Недостаточно прав для смены пароля этому пользователю!')
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
        lp.first_name=str(request.POST.get('telefon'))
        lp.last_name=str(request.POST.get('familia'))
        if fl == 0:
            pk=Profile.objects.get(user_id=lp.pk)
            pk.lpu_id=int(request.POST.get('tipvr'))
            if request.POST.get('evac') is None:
                pk.is_list_doctor=False
            if request.POST.get('commit') is None:
                pk.is_commit_doctor=False
            if request.POST.get('evac') == 'on':
                pk.is_list_doctor=True
            if request.POST.get('commit') == 'on':
                pk.is_commit_doctor=True
            pk.save()
        lp.save()
        return redirect('/adminmodule/us')
    else:
        arg['lp']=lp
        arg['fl']=fl
        return render(request, 'templadm/chdata.html',arg)


@login_required
def chpass(request,idus):
    lp=User.objects.get(pk=idus)
    if lp.user_profile.is_superman or lp.is_superuser:
        return HttpResponse('Недостаточно прав для смены пароля этому пользователю!')
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
        if str(request.POST.get('password')) != str(request.POST.get('password1')):
            return HttpResponse('Введенные пароли не совпадают!')
        lp.set_password(str(request.POST.get('password')))
        lp.save()
        return redirect('/adminmodule/us')
    else:
        form=chps()
        arg={}
        arg['form']=form
        arg['lp']=lp
        return render(request, 'templadm/chps.html',arg)



@login_required
def newus(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
        if User.objects.filter(username=str(request.POST.get('nameus'))).exists():
            return HttpResponse('Пользователь '+str(request.POST.get('nameus'))+' уже создан')
        a=checkin(str(request.POST.get('password')),str(request.POST.get('password1')),
        str(request.POST.get('nameus')),request.POST.get('evac'),request.POST.get('commit'),
        request.POST.get('tipvr'))
        if a=='success':
            user = User.objects.create_user(username=str(request.POST.get('nameus')),
                                 password=str(request.POST.get('password')),last_name=str(request.POST.get('fio')))
            usid=User.objects.get(username=str(request.POST.get('nameus')))
            mod=Profile()
            mod.user_id=usid.pk
            mod.lpu_id=int(request.POST.get('tipvr'))
            if request.POST.get('evac')=='on':
                mod.is_list_doctor=True
            if request.POST.get('commit')=='on':
                mod.is_commit_doctor=True
            mod.save()
        else:
            return HttpResponse('<center>Выявлены ошибки:<br>'+a)
        return redirect('/adminmodule/us')
    lp=lpubd.objects.all().order_by('name')
    form=nfus()
    arg={}
    arg['form']=form
    arg['lp']=lp
    return render(request, 'templadm/newus.html',arg)

@login_required
def use(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    profiles = Profile.objects.filter()
    us={}
    us['use']=profiles
    return render(request, 'templadm/use.html',us)


@login_required
def index(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    return redirect('/adminmodule/lpufrom')

@login_required
def lpudost(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    arg={}
    froml=lpubd.objects.all().order_by('id')
    arg['froml']=froml
    return render(request, 'templadm/lpudost.html',arg)

@login_required
def lpufrom(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    arg={}
    froml=fromlpu.objects.all().order_by('nazv')
    arg['froml']=froml
    return render(request, 'templadm/lpufrom.html',arg)

@login_required
def srmpl(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    arg={}
    fr=srmp.objects.all().order_by('id')
    arg['froml']=fr
    return render(request, 'templadm/srmpl.html',arg)

@login_required
def newsrmp(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
       form=newsrmpf(request.POST)
       if form.is_valid():
           ak=form.save()
           urla='/adminmodule/srmpl/'
           return redirect(urla)
    else:
        arg={}
        form=newsrmpf()
        arg['form']=form
    return render(request, 'templadm/newsrmp.html',arg)

@login_required
def newlpfrom(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
       form=newlp(request.POST)
       if form.is_valid():
           ak=form.save()
           urla='/adminmodule/lpufrom/'
           return redirect(urla)
    else:
        arg={}
        form=newlp()
        arg['form']=form
    return render(request, 'templadm/newlpfrom.html',arg)

@login_required
def newlpbd(request):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    if request.method=='POST':
       form=newlpbdform(request.POST)
       if form.is_valid():
           ak=form.save()
           urla='/adminmodule/lpudost/'
           return redirect(urla)
    else:
        arg={}
        form=newlpbdform()
        arg['form']=form
    return render(request, 'templadm/newlpbd.html',arg)

@login_required
def evado(request):
    arg={}
    evd=case.objects.filter(active=1).order_by('id')
    for j in evd:
        a=User.objects.get(pk=j.id_vrach_id)
        j.vrf=a.last_name
        j.telef=a.first_name
        if j.vputi==-1:
            j.sost='Новая эвакуация'
        if j.vputi==0:
            j.sost='Готов к выезду'
        if j.vputi==1:
            j.sost='Выезд начат'
        if j.vputi==2:
            j.sost='Выезд идет.Есть срез состояния в пути'
        if j.vputi==3:
            j.sost='Оформлено состояние после эвакуации'
        if j.vputi==4:
            j.sost='Оформлена доставка в ЛПУ. Эвакуация закрыта'
        if j.vputi>=1:
            delta=datetime.now().replace(tzinfo=None)-j.vzyat.replace(tzinfo=None)
            dur=delta.total_seconds()
            hours = divmod(dur, 3600)[0]
            j.htime=hours
        else:
            j.htime='Выезд не начат'
    arg['evd']=evd
    arg['count']=evd.count()
    return render(request, 'templadm/evado.html',arg)

@login_required
def about(request,idev):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    arg={}
    poi=case.objects.get(pk=idev)
    bef=before.objects.filter(case_id=poi.id).order_by('id')
    qps=intime.objects.none()
    inti=intimetime.objects.filter(case_id=poi.id).order_by('id')
    for pl in inti:
        qps |= intime.objects.filter(intimetime_id=pl.pk).order_by('id')
    aft=after.objects.filter(case_id=poi.id).order_by('id')
    arg['aft']=aft
    arg['inti']=inti
    arg['qps']=qps
    arg['bef']=bef
    arg['poi']=poi
    return render(request, 'templadm/about.html',arg)



@login_required
def editflp(request,idlpu):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    lpui=fromlpu.objects.get(pk=idlpu)
    if request.method=='POST':
       form=newlp(request.POST,instance=lpui)
       if form.is_valid():
           ak=form.save()
           urla='/adminmodule/lpufrom/'
           return redirect(urla)
    else:
        arg={}
        form=newlp(instance=lpui)
        arg['form']=form
    return render(request, 'templadm/newlpfrom.html',arg)

@login_required
def editsrmp(request,idlpu):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    lpui=srmp.objects.get(pk=idlpu)
    if request.method=='POST':
       form=newsrmpf(request.POST,instance=lpui)
       if form.is_valid():
           ak=form.save()
           urla='/adminmodule/srmpl/'
           return redirect(urla)
    else:
        arg={}
        form=newsrmpf(instance=lpui)
        arg['form']=form
    return render(request, 'templadm/newsrmp.html',arg)

@login_required
def editlpbd(request,idlpu):
    if not  request.user.user_profile.is_superman:
        return HttpResponse('Доступ только для АДМИНИСТРАТОРОВ!')
    lpui=lpubd.objects.get(pk=idlpu)
    if request.method=='POST':
       form=newlpbdform(request.POST,instance=lpui)
       if form.is_valid():
           kompoc=a/(b/750)+1
           ak=form()
           ak.save()
           urla='/adminmodule/lpudost/'
           return redirect(urla)
    else:
        arg={}
        form=newlpbdform(instance=lpui)
        arg['form']=form
    return render(request, 'templadm/newlpfrom.html',arg)
