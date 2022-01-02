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
from .forms import insform, insformstudy,LoginForm,SearchForm, NP, NE
from .models import Insultik,patient,case, before, atributes, after, intime,intimetime
from django.contrib.auth.decorators import login_required

@login_required
def pac(request):
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
                    return redirect('/')
                else:
                    return HttpResponse('Акаунт закрыт')
            else:
                return HttpResponse('Логин или пароль неверны!')
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
    return redirect('/pac/')

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

@login_required
def new_bef(request,case_id):
    a=''
    if request.method=='POST':
        for i in range(1,100):
            if request.POST.get(str(i)+':'+'1') is not None:
                model=before()
                model.atrib_id=i
                model.valtype=1
                model.case_id=case_id
                model.save()
            if request.POST.get(str(i)+':'+'2') is not None:
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
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="before").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)

@login_required
def newint(request,case_id):
    a=''
    tn=datetime.now()
    if request.method=='POST':
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
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="intime").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)


@login_required
def newaft(request,case_id):
    a=''
    if request.method=='POST':
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
        return redirect('/now_eva')
    else:
        atr=atributes.objects.filter(fortab__icontains="after").order_by('id')
        args={}
        args['case_id']=case_id
        args['atr']=atr
        return render(request,'newbef.html',args)


@login_required
def now_eva(request):
    poi=case.objects.filter(id_vrach=request.user.pk).filter(active=1)
    if poi.count()==1:
        args={}
        qps=intime.objects.none()
        args['poi']=poi[0]
        bef=before.objects.filter(case_id=poi[0].id).order_by('id')
        inti=intimetime.objects.filter(case_id=poi[0].id).order_by('id')
        aft=after.objects.filter(case_id=poi[0].id).order_by('id')
        aftr=aft.count()
        if aftr!=0:
            args['aft']=aft
            args['aft_k']=aftr
        else:
            args['aft_k']=0
        for pl in inti:
            qps |= intime.objects.filter(intimetime_id=pl.pk)
        if bef.count()!=0:
            args['bef_is']="1"
            args['bef']=bef
            if inti.count()!=0:
                args['inti']=inti
                args['inti_is']="1"
                args['qps']=qps
            else:
                args['inti_is']="0"
            return render(request,'noweva.html',args)
        else:
            args['bef_is']="0"
            args['inti_is']="-1"
            return render(request,'noweva.html',args)
    else:
        osh={}
        osh['osh']='Нет активных эвакуаций!'
        return render(request,'osh.html',osh)

@login_required
def delcase(request,caseid):
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
def delint(request,intid):
    if request.method=='POST':
        intime.objects.filter(intimetime_id=intid).delete()
        intimetime.objects.filter(id=intid).delete()
        return redirect('/now_eva')
    else:
        ppp=intimetime.objects.filter(id=intid)
        args={}
        args['ppp']=ppp[0]
        return render(request,'delint.html',args)


@login_required
def delbef(request,caseid):
    if request.method=='POST':
        before.objects.filter(case_id=caseid).delete()
        return redirect('/now_eva')
    else:
        ppp=before.objects.filter(case_id=caseid)
        args={}
        args['ppp']=ppp
        args['number']=caseid
        return render(request,'delbef.html',args)

@login_required
def begin(request,caseid):
    if request.method=='POST':
        a=datetime.now()
        ppp1=case.objects.filter(id=caseid).update(vputi=1,vzyat=a)
        return redirect('/now_eva')
    else:
        ppp=case.objects.filter(id=caseid)
        args={}
        args['ppp']=ppp[0]
        args['number']=caseid
        return render(request,'begin.html',args)

@login_required
def newevac(request,pac_id):
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
