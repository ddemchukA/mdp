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
import pyAgrum as gum

class podg:
    param={}

    def __init__(self,nom):
        self.nom=nom

    def __get_case(self):
        ak=case.objects.get(pk=self.nom)
        return ak

    def __get_bf(self):
        ak=before.objects.filter(case_id=self.nom)
        return ak

    def __get_glazgo(self,bf):
        sps=[]
        for kl in bf:
            if kl.atrib_id == 31:
                pv=kl.val_float
        if pv in range(0,9):
            self.param['glazg']=[1,0,0,0]
        if pv in range(9,12):
            self.param['glazg']=[0,1,0,0]
        if pv in range(11,14):
            self.param['glazg']=[0,0,1,0]
        if pv in range(13,16):
            self.param['glazg']=[0,0,0,1]

    def __get_dix(self,bf):
        for kl in bf:
            if kl.atrib_id == 40:
                self.param['dix']=[1,0,0]
            if kl.atrib_id == 41:
                self.param['dix']=[0,1,0]
            if kl.atrib_id == 47 or kl.atrib_id == 48:
                self.param['dix']=[0,0,1]

    def __get_satur(self,bf):
        for kl in bf:
            if kl.atrib_id == 58:
                pv=kl.val_float
        if pv in range(0,91):
            self.param['satur']=[1,0,0]
        if pv in range(91,94):
            self.param['satur']=[0,1,0]
        if pv in range(94,101):
            self.param['satur']=[0,0,1]

    def __get_transp(self,cs):
        if cs.id_trans_id == 1:
            self.param['transp']=[1,0]
        if cs.id_trans_id == 3:
            self.param['transp']=[0,1]

    def __get_road(self,cs):
        pv=cs.fromlpu.roadrate
        if pv >=0 and pv<=2:
            self.param['roadrate']=[1,0,0]
        if pv >2 and pv<=3:
            self.param['roadrate']=[0,1,0]
        if pv >3 and pv<=5:
            self.param['roadrate']=[0,0,1]


    def __formsp(self):
        cs=self.__get_case()
        bf=self.__get_bf()
        self.__get_glazgo(bf)
        self.__get_dix(bf)
        self.__get_satur(bf)
        self.__get_transp(cs)
        self.__get_road(cs)
        return self.param

    def vivod(self):
        kk=self.__formsp()
        bn1=gum.BayesNet('MedRisk')
        riskdix = bn1.add(gum.LabelizedVariable ( 'riskdix' , 'itogdix', 2))
        bn1.cpt(riskdix).fillWith([0.0,0.0])
        komgl=bn1.add('komgl',4)
        tipdix=bn1.add('tipdix',3)
        satur=bn1.add('satur',3)
        bn1=gum.fastBN("komgl[1,4]->riskdix[1,2];tipdix[1,3]->riskdix[1,2];satur[1,3]->riskdix[1,2]")
        bn1.cpt("komgl")[:] = kk['glazg']
        bn1.cpt("tipdix")[:] = kk['dix']
        bn1.cpt("satur")[:] = kk['satur']
        bn1.cpt("riskdix")[{'komgl':0, 'tipdix':2, 'satur':0}] = [0.99,0.01]
        ie=gum.LazyPropagation(bn1)
        ie.makeInference()
        resu=ie.posterior('riskdix')
        k=resu.tolist()
        k1={}
        k1['riskdix']={}
        k1['riskdix']['critical']=k[0]
        k1['riskdix']['non_critical']=k[1]
        return k1
