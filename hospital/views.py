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
from .forms import insform, insformstudy,LoginForm,SearchForm, NP, NE, Dostav,SearchForm1,Priem
from .models import Insultik,patient,case, before, atributes, after, intime,intimetime,dostavlen,deadinroad
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Permission
from .bn import podg

def checkdelete():
    return True


@login_required
def riskan(request,csid):
    ak=podg(csid)
    f=ak.vivod()
    arg={}
    arg['vivod']=f
    return render(request,'riskan.html',arg)


@login_required
def editpac(request,pacid):
    if not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Данный процесс доступен ТОЛЬКО эвакуирующему врачу!</h1>')
    paci=patient.objects.get(pk=pacid)
    if request.method=='POST':
       form=NP(request.POST,instance=paci)
       if form.is_valid():
           ak=form.save()
           urla='/pac/'
           return redirect(urla)
    else:

        form=NP(instance=paci)
    args={}
    args['form']=form
    return render(request,'newpac.html',args)

@login_required
def closecase(request,caseid):
    ev=case.objects.filter(id=caseid)
    ek=dostavlen.objects.filter(case_id=caseid).latest('id')
    if ek.lpu_id != request.user.user_profile.lpu_id:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if ev[0].vputi!=4 or  not request.user.user_profile.is_commit_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
       form=Priem(request.POST)
       if form.is_valid():
           ev.update(vputi=5,active=0)
           mod=dostavlen()
           mod.timedeist=datetime.now()
           mod.case_id=caseid
           mod.whatis=1
           mod.lpu_id=request.user.user_profile.lpu_id
           mod.primech=request.POST.get('primech')
           mod.us_id=request.user.id
           mod.save()
           urla='/showeva/'+str(caseid)+'/0'
           return redirect(urla)
    else:
        form=Priem()
    args={}
    args['form']=form
    return render(request,'closecase.html',args)

@login_required
def newdost(request,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=3 or  not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
       ev.update(vputi=4)
       form=Dostav(request.POST)
       if form.is_valid():
           a=case.objects.get(pk=caseid)
           a.save()
           mod=dostavlen()
           mod.timedeist=datetime.now()
           mod.case_id=caseid
           mod.whatis=0
           mod.lpu_id=request.POST.get('lpu')
           mod.primech=request.POST.get('primech')
           mod.us_id=request.user.id
           mod.save()
           urla='/now_eva'
           return redirect(urla)
    else:
        form=Dostav()
    args={}
    args['form']=form
    return render(request,'newdost.html',args)

@login_required
def findeva(request):
    if not request.user.user_profile.is_commit_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие</h1>')
    a=int(request.user.user_profile.lpu.pk)
    r=case.objects.filter(lpudost=a)
    args={}
    args['results']=r
    return render(request,'nfeva.html',args )

@login_required
def pac(request):
    if not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие</h1>')
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results=patient.objects.filter(f__icontains=query)
    args={}
    args['query']=query
    args['form']=form
    args['results']=results
    return render(request,'nf.html',args )


def logout_view(request):
    logout(request)
    return redirect('/')

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.user_profile.is_list_doctor:
                        return redirect('/')
                    elif user.user_profile.is_commit_doctor:
                        return redirect('/findeva')
                    elif user.user_profile.is_superman:
                        return redirect('/adminmodule')
                    else:
                        return HttpResponse('<h1 align=\"center\">Неизвестный профиль <a href=\"/logout\">НАЗАД</a></h1>')
                else:
                    return HttpResponse('Акаунт закрыт')
            else:
                return HttpResponse('Логин или пароль неверны или акаунт закрыт!')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def datains(request):
    if request.user.is_staff:
        adin=1
    else:
        adin=0
    arg={}
    arg['adin']=adin
    spi = Insultik.objects.all().order_by('id')
    arg['spi']=spi
    return render(request, 'datains.html',arg)

@login_required
def studyins(request):
    if request.user.is_staff:
        adin=1
    else:
        adin=0
    arg={}
    arg['adin']=adin
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if request.method=='POST':
       form=insformstudy(request.POST)
       if form.is_valid():
           vozrast=int(request.POST.get('vozrast'))
           pol=int(request.POST.get('pol'))
           if request.POST.get('gip')=='on':
               gip=1
           else:
               gip=0
           if request.POST.get('heart')=='on':
               heart=1
           else:
               heart=0
           if request.POST.get('sem')=='on':
               sem=1
           else:
               sem=0
           work=int(request.POST.get('work'))
           if request.POST.get('pro')=='on':
               pro=1
           else:
               pro=0
           kuru=int(request.POST.get('kuru'))
           sax=float(request.POST.get('sax'))
           ves=float(request.POST.get('ves'))
           rost=float(request.POST.get('rost'))
           rezulta=int(request.POST.get('rezult'))
           mod=Insultik()
           mod.vozrast=vozrast
           mod.pol=pol
           mod.gip=gip
           mod.heart=heart
           mod.sem=sem
           mod.work=work
           mod.pro=pro
           mod.kuru=kuru
           mod.sax=sax
           mod.ves=ves
           mod.rost=rost
           mod.rezult=rezulta
           if request.user.is_authenticated:
               use=request.user
           mod.use=use
           mod.save()
           return redirect('/data_ins/')
    else:
        arg['form']=insformstudy()
        arg['ip']=ip
        return render(request, 'studyins.html',arg)
@login_required
def index(request):
    arg={}
    if request.user.user_profile.is_list_doctor:
        return redirect('/pac/')
    if request.user.user_profile.is_commit_doctor:
        return redirect('/findeva/')
    if user.user_profile.is_superman:
        return redirect('/adminmodule')

def komglas(request):
    return render(request, 'komgl.html')

@login_required
def incident(request):
    arg={}
    return render(request, 'incident.html',arg)

@login_required
def lpu(request):
    arg={}
    return render(request, 'lpu.html',arg)

def raschet(argu):
    sx = int(argu['sx'])# ПОЛ
    ag = float(argu['ag']) # ВОЗРАСТ
    hyp = int(argu['hyp']) # НАЛИЧИЕ ГИПЕРТОНИ
    heart =int(argu['heart']) # БОЛЕЗНИ СЕРДЦА
    evert =int(argu['evert']) # СЕМЬЯ/НЕТ
    work =int(argu['work']) # ТИП РАБОТЫ
    resid =int(argu['resid']) # ТИП ПРОЖИВАНИЯ
    gluk =float(argu['gluk']) # УРОВЕНЬ САХАРА
    smok =int(argu['smok']) # ОТНОШЕНИЕ К КУРЕНИЮ
    w=float(argu['w']) # ВЕС
    h=float(argu['h'])/100#РОСТ
    bmi = w/(h**2) #рассчитываем индекс массы тела
    pr=(sx,ag,hyp,heart,evert,work,resid,gluk,smok,bmi)
    pr=pd.DataFrame(pr).T
    loaded_model=load_model("insult11.h5")# загружаем модель
    res = loaded_model.predict(pr)*100# делаем прогноз инсульта
    return res

@login_required
def new_pac(request):
    if request.method=='POST':
       form=NP(request.POST)
       if form.is_valid():
           ak=form.save()
           urla='/pac/'
           return redirect(urla)
    else:
        form=NP()
    args={}
    args['form']=form
    return render(request,'newpac.html',args)

def checkdatainbef(a):
    tp=''
    mk=0
    for i in range(1,100):
        if i == 7:
            b=a.POST.get(str(i)+':'+'2')
            if len(b)!=0:
                if float(b)<20 or float(b)>43:
                    tp=tp+'Неверное значение температуры,'
                    mk=mk+1
        if i == 68:
            b=a.POST.get(str(i)+':'+'4')
            if re.match(r'\d{2,3}\/\d{2,3}',b) is None and len(b)!=0:
                tp=tp+'Неверное значение давления справа, '
                mk=mk+1
        if i == 69:
            b=a.POST.get(str(i)+':'+'4')
            if re.match(r'\d{2,3}\/\d{2,3}',b) is None and len(b)!=0:
                tp=tp+'Неверное значение давления слева,'
                mk=mk+1
        if i == 31:
            b=a.POST.get(str(i)+':'+'2')
            if len(b)!=0:
                if float(b)<0 or float(b)>15:
                    tp=tp+'Неверное значение комы Глазго,'
                    mk=mk+1
        if i == 58:
            b=a.POST.get(str(i)+':'+'2')
            if len(b)!=0:
                if float(b)<0 or float(b)>100:
                    tp=tp+'Неверное значение сатурации,'
                    mk=mk+1
        if i == 67:
            b=a.POST.get(str(i)+':'+'2')
            if len(b)!=0:
                if float(b)<0 or float(b)>300:
                    tp=tp+'Неверное значение пульса,'
                    mk=mk+1
        if i == 75:
            b=a.POST.get(str(i)+':'+'2')
            if len(b)!=0:
                if float(b)<0 or float(b)>100:
                    tp=tp+'Неверное значение диуреза,'
                    mk=mk+1
    if mk == 0:
        tp='OK'
    return tp

@login_required
def new_bef(request,case_id):
    ev=case.objects.filter(id=case_id)
    if ev[0].vputi!=-1 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    a=''
    if request.method=='POST':
        b=checkdatainbef(request)
        if b != 'OK':
            return HttpResponse('<h1 align=\"center\">'+b+'</h1>')
        ev.update(vputi=0)
        for i in range(1,100):
            if request.POST.get(str(i)+':'+'1') is not None:
                model=before()
                model.atrib_id=i
                model.valtype=1
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'2') is not None:
                if len(str(request.POST.get(str(i)+':'+'2')))>0:
                    model=before()
                    model.atrib_id=i
                    model.valtype=2
                    model.val_float=float(request.POST.get(str(i)+':'+'2'))
                    model.case_id=case_id
                    model.save()
            if request.POST.get(str(i)+':'+'3') is not None and str(request.POST.get(str(i)+':'+'3')):
                model=before()
                model.atrib_id=i
                model.valtype=3
                model.val_text=str(request.POST.get(str(i)+':'+'3'))
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'4') is not None and str(request.POST.get(str(i)+':'+'4')):
                model=before()
                model.atrib_id=i
                model.valtype=4
                model.val_text=str(request.POST.get(str(i)+':'+'4'))
                model.case_id=case_id
                model.save()
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="before").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)

@login_required
def newint(request,case_id):
    k=[1,2]
    ev=case.objects.filter(id=case_id)
    if ev[0].vputi not in k or  not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    a=''
    tn=datetime.now()
    if request.method=='POST':
        if ev[0]!=2:
            ev.update(vputi=2)
        mod1=intimetime()
        mod1.case_id=case_id
        mod1.time=tn
        mod1.save()
        idu=mod1.id
        for i in range(1,100):
            if request.POST.get(str(i)+':'+'1') is not None:
                model=intime()
                model.intimetime_id=idu
                model.atrib_id=i
                model.valtype=1
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'2') is not None:
                model=intime()
                model.intimetime_id=idu
                model.atrib_id=i
                model.valtype=2
                model.val_float=float(request.POST.get(str(i)+':'+'2'))
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'3') is not None:
                model=intime()
                model.intimetime_id=idu
                model.atrib_id=i
                model.valtype=3
                model.val_text=str(request.POST.get(str(i)+':'+'3'))
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'4') is not None:
                model=intime()
                model.intimetime_id=idu
                model.atrib_id=i
                model.valtype=3
                model.val_text=str(request.POST.get(str(i)+':'+'4'))
                model.case_id=case_id
                model.save()
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="intime").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)


@login_required
def newaft(request,case_id):
    ev=case.objects.filter(id=case_id)
    if ev[0].vputi!=2 or  not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    a=''
    if request.method=='POST':
        ev.update(vputi=3)
        for i in range(1,100):
            if request.POST.get(str(i)+':'+'1') is not None:
                model=after()
                model.atrib_id=i
                model.valtype=1
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'2') is not None:
                model=after()
                model.atrib_id=i
                model.valtype=2
                model.val_float=float(request.POST.get(str(i)+':'+'2'))
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'3') is not None and str(request.POST.get(str(i)+':'+'3')):
                model=after()
                model.atrib_id=i
                model.valtype=3
                model.val_text=str(request.POST.get(str(i)+':'+'3'))
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'4') is not None and str(request.POST.get(str(i)+':'+'4')):
                model=after()
                model.atrib_id=i
                model.valtype=3
                model.val_text=str(request.POST.get(str(i)+':'+'4'))
                model.case_id=case_id
                model.save()
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="after").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)


@login_required
def showeva(request,caseid,flag):
    if not request.user.user_profile.is_commit_doctor:
        return HttpResponse('<h1 align=\"center\">Данный процесс доступен ТОЛЬКО принимающему врачу!</h1>')
    poi=case.objects.filter(id=caseid)
    if poi[0].lpudost != int(request.user.user_profile.lpu.id):
        return HttpResponse('<h1 align=\"center\">Просмотр эвакуации запрещен</h1>')
    if poi.count()==1:
        pp=poi[0].vputi
        args={}
        args['poi']=poi[0]
        args['vputi']=pp
        qps=intime.objects.none()
        if pp>-1:
            bef=before.objects.filter(case_id=poi[0].id).order_by('id')
            args['bef']=bef
        if pp>1:
            qps=intime.objects.none()
            inti=intimetime.objects.filter(case_id=poi[0].id).order_by('id')
            for pl in inti:
                qps |= intime.objects.filter(intimetime_id=pl.pk).order_by('id')
            args['inti']=inti
            args['qps']=qps
        if pp>2:
            aft=after.objects.filter(case_id=poi[0].id).order_by('id')
            args['aft']=aft
        if pp>=3:
            dostk=dostavlen.objects.filter(case_id=poi[0].id).order_by('id')
            args['dostk']=dostk
        if flag == 0:
            return render(request,'evacomm.html',args)
        else:
            return render(request,'itog.html',args)
    else:
        osh={}
        osh['osh']='Нет активных эвакуаций!'
        return render(request,'osh.html',osh)


@login_required
def now_eva(request):
    if not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Данный процесс доступен ТОЛЬКО эвакуирующему врачу!</h1>')
    poi=case.objects.filter(id_vrach=request.user.pk).filter(active=1)
    if poi.count()==1:
        pp=poi[0].vputi
        args={}
        args['poi']=poi[0]
        args['vputi']=pp
        qps=intime.objects.none()
        if pp>-1:
            bef=before.objects.filter(case_id=poi[0].id).order_by('id')
            args['bef']=bef
        if pp>1:
            qps=intime.objects.none()
            inti=intimetime.objects.filter(case_id=poi[0].id).order_by('id')
            for pl in inti:
                qps |= intime.objects.filter(intimetime_id=pl.pk).order_by('id')
            args['inti']=inti
            args['qps']=qps
        if pp>2:
            aft=after.objects.filter(case_id=poi[0].id).order_by('id')
            args['aft']=aft
        if pp>=3:
            dostk=dostavlen.objects.filter(case_id=poi[0].id).order_by('id')
            args['dostk']=dostk
        return render(request,'noweva.html',args)
    else:
        osh={}
        osh['osh']='Нет активных эвакуаций!'
        return render(request,'osh.html',osh)

@login_required
def delcase(request,caseid):
    ev=case.objects.get(id=caseid)
    if ev.vputi!=-1 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        case.objects.filter(id=caseid).delete()
        return redirect('/')
    else:
        ppp=case.objects.filter(id=caseid)
        args={}
        args['ppp']=ppp[0]
        args['number']=caseid
        return render(request,'delcase.html',args)

@login_required
def delint(request,intid,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=2 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        intime.objects.filter(intimetime_id=intid).delete()
        intimetime.objects.filter(id=intid).delete()
        if intimetime.objects.filter(case_id=caseid).count()==0:
            ev.update(vputi=1)
        return redirect('/now_eva')
    else:
        ppp=intimetime.objects.filter(id=intid)
        args={}
        args['ppp']=ppp[0]
        return render(request,'delint.html',args)

@login_required
def deldost(request,dostid,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=4 or  not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        ev.update(vputi=3)
        dostavlen.objects.filter(pk=dostid).delete()
        return redirect('/now_eva')
    else:
        ppp=dostavlen.objects.filter(pk=dostid)
        args={}
        args['ppp']=ppp
        args['number']=dostid
        return render(request,'deldost.html',args)



@login_required
def delaft(request,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=3 or  not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        ev.update(vputi=2)
        after.objects.filter(case_id=caseid).delete()
        return redirect('/now_eva')
    else:
        ppp=after.objects.filter(case_id=caseid)
        args={}
        args['ppp']=ppp
        args['number']=caseid
        return render(request,'delaft.html',args)

@login_required
def delbef(request,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=0 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        ev.update(vputi=-1)
        before.objects.filter(case_id=caseid).delete()
        return redirect('/now_eva')
    else:
        ppp=before.objects.filter(case_id=caseid)
        args={}
        args['ppp']=ppp
        args['number']=caseid
        return render(request,'delbef.html',args)

@login_required
def deadvputi(request,caseid,pacid):
    k=[1,2]
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi not in k or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        a=datetime.now()
        mod=deadinroad()
        mod.case_id=caseid
        mod.time=a
        mod.primech=str(request.POST.get('textar'))
        mod.save()
        ev.update(vputi=6,active=0)
        patient.objects.filter(id=pacid).update(prdead=1)
        return redirect('/pac')
    else:
        args={}
        args['ppp']=ev[0]
        args['number']=caseid
        return render(request,'deadvputi.html',args)


@login_required
def begin(request,caseid):
    ev=case.objects.filter(id=caseid)
    if ev[0].vputi!=0 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или состояние эвакуации = error</h1>')
    if request.method=='POST':
        a=datetime.now()
        ev.update(vputi=1,vzyat=a)
        return redirect('/now_eva')
    else:
        args={}
        args['ppp']=ev[0]
        args['number']=caseid
        return render(request,'begin.html',args)

@login_required
def newevac(request,pac_id):
    ev=patient.objects.filter(id=pac_id)
    if ev[0].prdead!=0 or not request.user.user_profile.is_list_doctor:
        return HttpResponse('<h1 align=\"center\">Ошибка по процессу: врач не имеет право на данное действие или пациент мертв</h1>')
    poi=case.objects.filter(id_vrach=request.user.pk)
    fl=0
    for k in poi:
        if k.active==1:
            fl=1;
    poi=case.objects.filter(id_pac=pac_id)
    for k in poi:
        if k.active==1:
            fl=1;
    if fl==1:
        osh={}
        osh['osh']='у данного врача и/или пациента уже есть активная эвакуация!'
        return render(request,'osh.html',osh)
    if request.method=='POST':
       form=NE(request.POST)
       if form.is_valid():
           ak=form.save(commit=False)
           ak.id_pac_id=pac_id
           ak.id_vrach_id=request.user.pk
           ak.save()
           urla='/now_eva'
           return redirect(urla)
    else:
        p1=patient.objects.get(id=pac_id)
        form=NE()
        args={}
        args['pac']=p1
        args['form']=form
        return render(request,'newevac.html',args)

def expertins(request):
    if request.method=='POST':
       form=insform(request.POST)
       if form.is_valid():
           ag=request.POST.get('vozrast')
           sx=request.POST.get('pol')
           if request.POST.get('gip')=='on':
               hyp=1
           else:
               hyp=0
           if request.POST.get('heart')=='on':
               heart=1
           else:
               heart=0
           if request.POST.get('sem')=='on':
               evert=1
           else:
               evert=0
           work=request.POST.get('work')
           if request.POST.get('pro')=='on':
               resid=1
           else:
               resid=0
           smok=request.POST.get('kuru')
           gluk=request.POST.get('sax')
           w=request.POST.get('ves')
           h=request.POST.get('rost')
           ar={}
           ar['sx']=sx
           ar['ag']=ag
           ar['hyp']=hyp
           ar['heart']=heart
           ar['evert']=evert
           ar['work']=work
           ar['resid']=resid
           ar['smok']=smok
           ar['gluk']=gluk
           ar['w']=w
           ar['h']=h
           insu={}
           ri1=raschet(ar)
           ri2=round(ri1[0][0],2)
           if ri2>=0 and ri2<=10:
               aa="Все нормально. Еще поживете!"
           elif ri2>=10 and ri2<=50:
               aa="Пора задуматься о здоровье!"
           elif ri2>50:
               aa="Ничего хорошего. По краю ходим!"
           insu['tex']=aa
           insu['res']=str(ri2)
           return render(request, 'rezult.html',insu)
    else:
        form=insform()
        args={}
        args['form']=form
    return render(request, 'expert.html',args)
