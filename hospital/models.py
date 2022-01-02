from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime

# Create your models here.
class Insultik(models.Model):
    vozrast = models.IntegerField()
    pol = models.IntegerField()
    gip = models.IntegerField()
    heart = models.IntegerField()
    sem = models.IntegerField()
    pol = models.IntegerField()
    work = models.IntegerField()
    pro = models.IntegerField()
    sax = models.FloatField()
    kuru=models.IntegerField()
    rost = models.FloatField()
    ves = models.FloatField()
    rezult = models.IntegerField()
    use = models.CharField(max_length=20,default="NONE")

class lpubd(models.Model):
    name = models.CharField(max_length=150,default="NONE")

    def __str__(self):
        return str(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile", on_delete=models.CASCADE, null=True,)
    lpu = models.ForeignKey(lpubd,on_delete=models.CASCADE, null=True)
    is_list_doctor = models.BooleanField(default=False)
    is_commit_doctor = models.BooleanField(default=False)
    is_superman = models.BooleanField(default=False)

    def __str__(self):
        return 'Профиль пользователя: '+ self.user.last_name+' username: '+self.user.username+' ЛПУ: '+self.lpu.name
class sex(models.Model):
    sex=models.CharField(max_length=1,default="M")
    def __str__(self):
        return str(self.sex)

class patient(models.Model):
    f=models.CharField(max_length=150,default="NONE")
    i=models.CharField(max_length=150,default="NONE")
    o=models.CharField(max_length=150,default="NONE")
    dr=models.DateField(default=date.today)
    pol=models.ForeignKey(sex,on_delete=models.CASCADE, null=True)
    doc=models.CharField(max_length=150,default="NONE")
    polis=models.CharField(max_length=150,default="NONE")
    snils=models.CharField(max_length=150,default="NONE")
    telrod=models.CharField(max_length=150,default="NONE")
    prdead=models.IntegerField(default=0)
    def __str__(self):
        return str(self.f)+' '+str(self.i)+' '+str(self.o)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.f = self.f.upper()
        self.i = self.i.upper()
        self.o = self.o.upper()
        return super(patient, self).save(force_insert, force_update, using, update_fields)

class transport(models.Model):
    nazv=models.CharField(max_length=150,default="NONE")
    def __str__(self):
        return str(self.nazv)


class fromlpu(models.Model):
    nazv=models.CharField(max_length=150,default="NONE")
    roadoc=models.IntegerField(default=0)
    rast=models.IntegerField(default=0)
    roadrate=models.FloatField(default=0)
    def __str__(self):
        return str(self.nazv)
    def save(self, *args, **kwargs):
        self.roadrate=round(self.roadoc/((self.rast/750)+1),1)
        super(fromlpu, self).save(*args, **kwargs)

class srmp(models.Model):
    fio=models.CharField(max_length=150,default="NONE")
    def __str__(self):
        return str(self.fio)

class dostavlen(models.Model):
    timedeist=models.DateTimeField(default='datetime.now')
    lpu = models.ForeignKey(lpubd,on_delete=models.CASCADE, null=True)
    us = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    whatis = models.IntegerField(default=0)
    case=models.ForeignKey('case', on_delete=models.PROTECT)
    primech=models.CharField(max_length=150,default="NONE")

class case(models.Model):
    dateti=models.DateTimeField(default=datetime.now)
    dslpu=models.CharField(max_length=150,default="X00.X")
    dscons=models.CharField(max_length=150,default="X00.X")
    vzyat=models.DateTimeField(null=True,blank=True)
    id_pac=models.ForeignKey('patient', on_delete=models.PROTECT)
    id_trans=models.ForeignKey('transport', on_delete=models.PROTECT)
    id_vrach=models.ForeignKey(User, on_delete=models.PROTECT)
    id_srmp=models.ForeignKey(srmp, on_delete=models.PROTECT)
    fromlpu=models.ForeignKey(fromlpu, on_delete=models.PROTECT)
    active=models.IntegerField(default=1)
    vputi=models.IntegerField(default=-1)



class atributes(models.Model):
    nazv=models.CharField(max_length=150,default="NONE")
    valtype=models.IntegerField()
    root=models.IntegerField(default=0)
    ispotomok=models.IntegerField(default=0)
    potomki=models.CharField(max_length=150,default="0")
    roditel=models.IntegerField(default=0)
    antogon=models.CharField(max_length=150,default="0")
    umolch=models.CharField(max_length=150,default="",blank=True)
    fortab=models.CharField(max_length=150,default="before,after,intime")
    group=models.IntegerField(default=0)
    def __str__(self):
        return str(self.pk)+' '+str(self.nazv)

class before(models.Model):
    atrib=models.ForeignKey('atributes', on_delete=models.PROTECT)
    case=models.ForeignKey('case', on_delete=models.PROTECT)
    valtype=models.IntegerField(default=0)
    val_float=models.FloatField(default=-1000.0)
    val_text=models.CharField(max_length=150,default="NOT_VAL")
    def __str__(self):
        return str(self.atrib)

class after(models.Model):
    atrib=models.ForeignKey('atributes', on_delete=models.PROTECT)
    case=models.ForeignKey('case', on_delete=models.PROTECT)
    valtype=models.IntegerField(default=0)
    val_float=models.FloatField(default=-1000.0)
    val_text=models.CharField(max_length=150,default="NONE")
    def __str__(self):
        return str(self.atrib)

class deadinroad(models.Model):
    time=models.DateTimeField(default='datetime.now')
    case=models.ForeignKey('case', on_delete=models.PROTECT)
    primech=models.CharField(max_length=250,default="NONE")
    def __str__(self):
        return str(self.time)

class intimetime(models.Model):
    time=models.DateTimeField(default='datetime.now')
    case=models.ForeignKey('case', on_delete=models.PROTECT)
    def __str__(self):
        return str(self.time)

class intime(models.Model):
    intimetime=models.ForeignKey('intimetime', on_delete=models.PROTECT)
    atrib=models.ForeignKey('atributes', on_delete=models.PROTECT)
    valtype=models.IntegerField(default=0)
    val_float=models.FloatField(default=-1000.0)
    val_text=models.CharField(max_length=150,default="NONE")
    def __str__(self):
        return str(self.atrib)
