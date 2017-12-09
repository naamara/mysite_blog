# -*- coding: utf-8 -*-
from django.shortcuts import render


# Create your views here.
def index(request):
 	return render(request, "personal/home.html")

def contact(request):
	return render(request, "personal/basic.html", {'hannington': ['If you want to text me, send a message here', 'naamarahannz@gmail.com']})

