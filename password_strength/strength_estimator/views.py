from django.shortcuts import render,redirect
from django.http import HttpResponse
from .strength import *
# Create your views here.

def home(request):
    return render(request,'strength_estimator/home.html')
    #return redirect(request.META['HTTP_REFERER'])
def index(request):
    name=request.POST["name"]
    passhash=hash(name)
    et,fg=dictionary_attack(passhash)
    result=strength(name,fg)
    context={'renderdict':result}
    return render(request,'strength_estimator/home.html',context)
   # return redirect(request.META['HTTP_REFERER'],context)
def about(request):
    return render(request,'strength_estimator/about.html')
'''
def simple_function(request):
    print("Hi")
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

'''
