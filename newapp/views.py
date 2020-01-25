from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import *
import bcrypt
def index(request):
    return render(request,"index.html")
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors)> 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register')
        return redirect('/')
    else:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        passwords=request.POST['password']
        pw_hash=bcrypt.hashpw(passwords.encode(),bcrypt.gensalt()).decode()
        loggedin = User.objects.create(firstname=firstname,lastname=lastname,email=email,password=pw_hash)
        request.session['id']=loggedin.id
        return redirect('/book')
def login(request):
    user=User.objects.filter(email=request.POST['email_login'])
    if user:
        loggin_user=user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),loggin_user.password.encode()):
            request.session['id']=loggin_user.id
            return redirect('/book')
    messages.error(request, "you have entered an invalid username or password", extra_tags="login")
    return redirect('/')

def show(request):
    if 'id' in request.session:
        context={
             'book':Book.objects.all(),
            'result':User.objects.get(id= request.session["id"])}
        return render(request,"book.html",context)
    else:
        return redirect("/")

def addbook(request):
    errors=Book.objects.basic_validator(request.POST)
    if len(errors)> 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book')
    else:
        user=User.objects.get(id=request.session["id"])
        title=request.POST["title"]
        desc=request.POST["desc"]
        book= Book.objects.create(title=title ,desc=desc,uploaded=user)
        book.userslike.add(user)
        return redirect("/book")

def logout(request):
    del request.session['id']
    return redirect("/")
def showbook(request,id): 
    context={
        "bookdetail":Book.objects.get(id=id),
        "user":User.objects.get(id=request.session["id"])
    }
    return render(request,"bookdetail.html",context)

def addfavorite(request,id):
    book=Book.objects.get(id=id)
    user=User.objects.get(id=request.session["id"])
    book.userslike.add(user)
    return redirect(f'/bookshow/{id}')
def removefavorite(request,id):
    book=Book.objects.get(id=id)
    user=User.objects.get(id=request.session["id"])
    book.userslike.remove(user)
    return redirect(f'/bookshow/{id}')
def delete(request,id):
      deletebook=book=Book.objects.get(id=id)
      deletebook.delete()
      return redirect('/book')
def update(request,id):
    errors=Book.objects.basic_validator(request.POST)
    if len(errors)> 0:
       for key, value in errors.items():
            messages.error(request, value)
       return redirect(f'/bookshow/{id}')
    else:
        updatebook=book=Book.objects.get(id=id)
        updatebook.title=request.POST['title']
        updatebook.desc=request.POST["desc"]
        updatebook.user=updatebook.uploaded
        updatebook.save()
        return redirect("/book")

    
