from django import forms
from hospital.models import patient,case,dostavlen
from django.forms import ModelForm

class NP(ModelForm):
     class Meta:
         model = patient
         fields = ['f', 'i', 'o', 'dr','pol','doc','polis','snils','telrod']
         labels = {'f':'Фамилия','i':'Имя','o':'Отчество','dr':'Дата рождения','pol':'Пол','doc':'Документ','polis':'Полис','snils':'СНИЛС','telrod':'Контакт родственника'}

class NE(ModelForm):
     class Meta:
         model = case
         fields = ['fromlpu','dateti','dslpu', 'dscons', 'id_trans','id_srmp']
         labels = {'fromlpu':'Взят из ЛПУ','dateti':'Дата/время прибытия к больному','dslpu':'Диагноз ЛПУ','dscons':'Диагноз консультанта','id_trans':'Транспорт','id_srmp':'Средний медперсонал'}

class Dostav(ModelForm):
    class Meta:
        model = dostavlen
        fields = ['lpu','primech']
        labels = {'lpu':'Доставлен в ЛПУ','primech':'Замечания'}

class Priem(ModelForm):
    class Meta:
        model = dostavlen
        fields = ['primech']
        labels = {'primech':'Замечания'}

class insform(forms.Form):
    vozrast = forms.ChoiceField(label='Ваш возраст:', choices=[(x,x) for x in range(0, 120)])
    pol = forms.ChoiceField(label='Ваш пол (0-Ж, 1-М):', choices=[(x,x) for x in range(0, 2)])
    gip = forms.BooleanField(label='Гипертония',required = False)
    heart = forms.BooleanField(label='Болезни сердца',required = False)
    sem = forms.BooleanField(label='Семейный(ая)',required = False)
    work = forms.ChoiceField(label='Тип работы (0 ребенок, 1 бюджетник, 2 безработный, 3 фирма, 4 частный предприниматель):', choices=[(x,x) for x in range(0, 5)])
    pro = forms.BooleanField(label='Городской(ая)',required = False)
    sax= forms.CharField(label='Уровень сахара (через точку)')
    kuru = forms.ChoiceField(label='Отношение к курению (0-Ранее курил, 1-Курит, 2-Никогда не курил, 3-Неизвестно):', choices=[(x,x) for x in range(0, 4)])
    ves= forms.CharField(label='Вес (целое число)')
    rost= forms.CharField(label='Рост (целое)')

class insformstudy(forms.Form):
    vozrast = forms.ChoiceField(label='Ваш возраст:', choices=[(x,x) for x in range(0, 120)])
    pol = forms.ChoiceField(label='Ваш пол (0-Ж, 1-М):', choices=[(x,x) for x in range(0, 2)])
    gip = forms.BooleanField(label='Гипертония',required = False)
    heart = forms.BooleanField(label='Болезни сердца',required = False)
    sem = forms.BooleanField(label='Семейный(ая)',required = False)
    work = forms.ChoiceField(label='Тип работы (0 ребенок, 1 бюджетник, 2 безработный, 3 фирма, 4 частный предприниматель):', choices=[(x,x) for x in range(0, 5)])
    pro = forms.BooleanField(label='Городской(ая)',required = False)
    sax= forms.CharField(label='Уровень сахара (через точку)')
    kuru = forms.ChoiceField(label='Отношение к курению (0-Ранее курил, 1-Курит, 2-Никогда не курил, 3-Неизвестно):', choices=[(x,x) for x in range(0, 4)])
    ves= forms.CharField(label='Вес (целое число)')
    rost= forms.CharField(label='Рост (целое)')
    rezult = forms.ChoiceField(label='Результат (1/0)',choices=[(x,x) for x in range(0, 2)])

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm1(forms.Form):
    query = forms.IntegerField(label='Введите номер эвакуации: ')

class SearchForm(forms.Form):
    query = forms.CharField(label='Введите фамилию пациента: ')
