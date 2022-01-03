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
    def __get_sost(self,bf):
        sps=[]
        for kl in bf:
            sps.append(kl.atrib_id)
        if 2 in sps:
            self.param['sost']=[1,0,0]
        if 3 in sps:
            self.param['sost']=[0,1,0]
        if 4 in sps or 5 in sps or 6 in sps :
            self.param['sost']=[0,0,1]
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
                self.param['dix']=[1,0,0,0]
            if kl.atrib_id == 41:
                self.param['dix']=[0,1,0,0]
            if kl.atrib_id == 47:
                self.param['dix']=[0,0,1,0]
            if kl.atrib_id == 48:
                self.param['dix']=[0,0,0,1]

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
        self.__get_sost(bf)
        self.__get_glazgo(bf)
        self.__get_dix(bf)
        self.__get_dix(bf)
        self.__get_satur(bf)
        self.__get_transp(cs)
        self.__get_road(cs)
        return self.param

    def vivod(self):
        kk=self.__formsp()
        return kk
