# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

def index(request):
  return HttpResponse('<h1>Cтраница приложения с опросами</h1>')

def questionnaires(request, queid):
  if int(queid) > 10:
    return redirect('home', permanent = False)

  return HttpResponse(f'<h1>Голосование по опросникам</h1><p>{queid}</p>')

def error_404(request, exception):
  return HttpResponseNotFound(f'<h1>Cтраница не найдена</h1>')
