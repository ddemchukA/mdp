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

    def __formsp(self):
        cs=self.__get_case()
        bf=self.__get_bf()
        self.__get_sost(bf)
        self.__get_glazgo(bf)
        return self.param

    def vivod(self):
        kk=self.__formsp()
        return kk
