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
    
    # if request.path.endswith('/chat/'):
    #     return redirect('/chat/django')
    # get url name
    print('request.path:', request.path)
    index_chat = request.path.find("/chat/")
    if index_chat != -1: # Extract the substring after "/chat/"
        chat_name = request.path[index_chat + len("/chat/"):]

    else:
        print("Not found in the path.")
        chat_name = ''
    
    if chat_name == '':
        chat_name == 'django'
    
    
    print('chat_name:' , chat_name)  # Output: python
    
    chat_object = 'default object'
    
    if chat_name == 'django':
        chat_object = 1
    elif chat_name == 'news':
        chat_object = 2
    elif chat_name == 'introduction':
        chat_object = 3
    elif chat_name == 'help':
        chat_object = 4
    else:
        chat_object = 1  # Default to 'django' if no chat room is specified
    
    print("Chat object:", chat_object)
        
    
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        mychat = Chat.objects.get(id=chat_object)
        print('mychat' , mychat)
        new_message = Message.objects.create(text=request.POST['textmessage'] ,chat=mychat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=chat_object)
    return render(request, 'chat/index.html', {'messages': chatMessages, 'chat_name' : chat_name })

def login_view(request):
    redirect_to = request.GET.get('next', '/chat/django')  # Default redirect URL after login
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'guest' and password == '123456789!': # Perform guest login
            user = authenticate(username=username, password=password)
        else:
            user = authenticate(request, username=username, password=password) # Perform regular login
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
        if User.objects.filter(username=new_username).exists(): # Check if the username already exists
            return render(request, 'register/signup.html', {'usernameAlreadyExists': True})
        if User.objects.filter(email=new_email).exists(): # Check if the email already exists
            return render(request, 'register/signup.html', {'emailAlreadyExists': True})
        if new_password != confirm_password: # Check if the passwords match
            return render(request, 'register/signup.html', {'passwordMismatch': True})
        user = User.objects.create_user(username=new_username, email=new_email, password=new_password, is_staff=True) # Create the new user
        if user:
            return render(request, 'register/signup.html', {'registrationSucceded': True})
    return render(request, 'register/signup.html')


def password_reset(request):
    if request.method == 'POST':
        password_reset_email = request.POST.get('email') 
        if not User.objects.filter(email=password_reset_email).exists(): # Check if the email does not exist
            return render(request, 'register/password_reset.html', {'noExistingEmail': True})   
        if User.objects.filter(email=password_reset_email).exists(): # Check if the email already exists
            return render(request, 'register/password_reset.html', {'newPassword': True})   
    return render(request, 'register/password_reset.html')

def sign_out(request):
    logout(request)
    return render(request, 'auth/sign_out.html')