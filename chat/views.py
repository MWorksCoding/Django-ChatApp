from django.shortcuts import render
from .models import Message, Chat
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

# wichtig:  09 - Datenbank Objekt erstellen
# Create your views here.
@login_required(login_url='/login/')#redirect if not logged in
def index(request):    
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        mychat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'] ,chat=mychat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages })

def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username') , password=request.POST.get('password'))
        if user :
            login(request , user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect' : redirect})
    return render(request, 'auth/login.html', {'redirect' : redirect})