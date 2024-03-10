from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from shop.models import Category, Product
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

# Create your views here.

def allcategories(request):
    c = Category.objects.all()
    return render(request, 'category.html', {'c': c})

def allproducts(request, p):
    c = Category.objects.get(name=p)
    p = Product.objects.filter(category=c)
    return render(request, 'product.html', {'c': c, 'p': p})

def details(request, c):
    p = Product.objects.get(name=c)
    return render(request, "details.html", {'p': p})

#@login_required
def register(request):
    if request.method == "POST":
        u = request.POST['u']
        p = request.POST['p']
        c = request.POST['c']
        e = request.POST['e']
        f = request.POST['f']
        l = request.POST['l']

        # Check if a user with the given username already exists
        if User.objects.filter(username=u).exists():
            return HttpResponse("Username already exists. Please choose a different one.")

        # Check if passwords match
        if p == c:
            # Create a new user
            b = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
            b.save()
            return redirect('shop:allcat')
        else:
            return HttpResponse("Passwords do not match")

    return render(request, "register.html")
def user_login(request):
    if request.method == "POST":
        u = request.POST.get('u')
        p = request.POST.get('p')
        user = authenticate(username=u, password=p)
        if user:
            auth_login(request, user)
            return redirect('shop:allcat')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('shop:allcat')






