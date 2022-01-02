from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    args={}
    args['new']=0
    args['zak']=0
    return render(request, 'main.html',args)

def contacts(request):
    return render(request, 'conta.html')
