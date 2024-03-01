from django.shortcuts import render
from .models import Message, Chat
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers



@login_required(login_url='/login/')#redirect if not logged in
def index(request):    
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        mychat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'] ,chat=mychat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages })

# def login_view(request):
#     redirect = request.GET.get('next')
#     if request.method == 'POST':
#         user = authenticate(username=request.POST.get('username') , password=request.POST.get('password'))
#         if user :
#             login(request , user)
#             return HttpResponseRedirect('/chat/')
#             # return HttpResponseRedirect(request.POST.get('redirect'))
#         else:
#             return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect' : redirect})
#     return render(request, 'auth/login.html', {'redirect' : redirect})

def login_view(request):
    redirect_to = request.GET.get('next', '/chat/')  # Default redirect URL after login

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == 'guest' and password == '123456789!':
            # Perform guest login
            user = authenticate(username=username, password=password)
        else:
            # Perform regular login
            user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(redirect_to)
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect_to})

    return render(request, 'auth/login.html', {'redirect': redirect_to})


def create_user_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if the username already exists
        if User.objects.filter(username=new_username).exists():
            return render(request, 'register/signup.html', {'usernameAlreadyExists': True})
        
        # Check if the email already exists
        if User.objects.filter(email=new_email).exists():
            return render(request, 'register/signup.html', {'emailAlreadyExists': True})
        
        # Check if the passwords match
        if new_password != confirm_password:
            return render(request, 'register/signup.html', {'passwordMismatch': True})

        # Create the new user
        user = User.objects.create_user(username=new_username, email=new_email, password=new_password, is_staff=True)
        if user:
            return render(request, 'register/signup.html', {'registrationSucceded': True})
    
    return render(request, 'register/signup.html')


def password_reset(request):
    if request.method == 'POST':
        password_reset_email = request.POST.get('email') 
        
        # Check if the email does not exist
        if not User.objects.filter(email=password_reset_email).exists():
            return render(request, 'register/password_reset.html', {'noExistingEmail': True})   
        # Check if the email already exists
        if User.objects.filter(email=password_reset_email).exists():
            return render(request, 'register/password_reset.html', {'newPassword': True})   
        
    return render(request, 'register/password_reset.html')

def sign_out(request):
    logout(request)
    return render(request, 'auth/sign_out.html')