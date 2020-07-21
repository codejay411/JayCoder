from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('this is home page')

def about(request):
    return render(request, 'home/about.html')
    # return HttpResponse('this is about page')

def contact(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        # print(name, email, phone, message)

        # for message framework
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(message)<4:
            messages.error(request, "Please fill the form correctly !")
        else:
            messages.success(request, "Your message has been sent !")

        # send data from form o database
        contact=Contact(name=name, email=email, phone=phone, message=message)
        contact.save()

    return render(request, 'home/contact.html')
    # return HttpResponse('this is contact page')


def search(request):
    query=request.GET['query']
    if len(query)>78:
        allposts=Post.objects.none()
    else:
        allpoststitle=Post.objects.filter(title__icontains=query)
        allpostscontent=Post.objects.filter(content__icontains=query)
        allposts=allpoststitle.union(allpostscontent)

    params={'allposts':allposts, 'query':query}
    return render(request, 'home/search.html', params)
    # return HttpResponse("this is serch")

def handlesignup(request):
    if request.method=='POST':
        username=request.POST['username']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        # check for errorneous input
        if len(username)>10:
            messages.error(request, "username must be 10 character !")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "username should omly contain letter and numbers !")
            return redirect('home')

        if password1 != password2:
            messages.error(request, "password donot match !")
            return redirect('home')


        # create the user
        myuser=User.objects.create_user(username, email, password1)
        myuser.first_name=firstname
        myuser.last_name=lastname
        myuser.save()
        messages.success(request, "your acoount is succesfully created !")
        return redirect('home')
    else:
        return HttpResponse("404 not found !")

def handlelogin(request):
    if request.method=='POST':
        # get the post parameter
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request, "Successfully logged in !")
            return redirect('home')
        else:
            messages.error(request, "invalid credential....please try again !")
            return redirect('home')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out !")
    return redirect('home')


