import re #for user validation
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from app1.middleware import RestrictAdminUserMiddleware
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
# from django.http import HttpResponse


# Create your views here.

###################### USER SIGNUP PAGE ####################


@never_cache
def signup(request):
    # result=HttpResponse("this is a new page ",status=200)
    # return result
    if request.user.is_authenticated:#authenticated user is only on home page
        return redirect('home')
    if request.POST:
        name=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
    
        # Name validation,below...
        if not name or not name.isalpha():
            return render(request, 'signup.html', {'name_error': 'Please enter a valid name with alphabetic characters only.'})
        #Email validation,below...
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'signup.html', {'error_message': 'Please enter a valid email address.'})

        #password validation,below...
        if pass1 != pass2:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match.'})
        elif len(pass1) < 6:
            return render(request, 'signup.html', {'error_message': 'Password must be at least 6 characters long.'})
        
        elif not re.search(r'[A-Z]', pass1):
            return render(request, 'signup.html', {'error_message': 'Password must contain at least one uppercase letter.'})
        
        # Check for at least one lowercase letter
        elif not re.search(r'[a-z]', pass1):
            return render(request, 'signup.html', {'error_message': 'Password must contain at least one lowercase letter.'})
        
        # Check for at least one digit
        elif not re.search(r'\d', pass1):
            return render(request, 'signup.html', {'error_message': 'Password must contain at least one digit.'})
        
        # Check for at least one special character
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', pass1):
            return render(request, 'signup.html', {'error_message': 'Password must contain at least one special character.'})
        
        else:
            user=User.objects.create_user(username=name,email=email,password=pass1)
            user.save()

        return redirect('login')
    return render(request,'signup.html')

###################### USER LOGIN PAGE  ####################

@never_cache
def loginPage(request):
    if request.user.is_authenticated:#current user ,Uermodel,Anonymous user
        return redirect('home')
    if request.POST:#query dict object
        name=request.POST.get('name')#get inside query set class
        pass1=request.POST.get('pass')
        user=authenticate(request,username=name,password=pass1)
        if user is not None:
            if user.is_superuser:
                #super user entry was restricted to the home page...
                return render(request ,'login.html',{'error_message':'Super-user not found...!'})
            else:
                login(request,user)
                return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'password or username is incorrect.'})
    return render(request,'login.html')

###################### USER HOME PAGE ####################

@login_required(login_url='login')
@never_cache
def home(request):
    return render(request,'home.html')

###################### LOGOUT ####################

def logoutPage(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('adminlogin')
    else:
        logout(request)
        return redirect('login')
    
###################### ADMIN LOGIN ####################

@never_cache
def AdminLogin(request):
    if request.user.is_authenticated:
        return redirect('adminhome')
    if request.POST :
        name=request.POST.get('name')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=name,password=pass1)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect('adminhome')
            else:
                return render(request,'admin_login.html',{'error_message':'Normal-user not found...!'})
        else:
            return render(request, 'admin_login.html', {'error_message': 'password or username is incorrect.'})
    return render(request,'admin_login.html')

###################### ADMIN HOME ####################

@never_cache
@login_required(login_url='adminlogin')
@RestrictAdminUserMiddleware
def AdminHome(request):
    #user is a query set object 
    user=User.objects.filter(is_superuser=False) # To avoid the super user data...
    return render(request,'admin_home.html',{'user':user}) 

###################### ADD USER DATA ####################

def add(request):
    if request.POST:
        name=request.POST.get('name')
        email=request.POST.get('email')
        user=User(username=name,email=email)
        user.save()
    return redirect('adminhome')

###################### EDIT USER DATA ###################


def edit(request):
    user=User.objects.all()
    return redirect(request,'admin_home.html',{'user':user})

#################### UPDATE USER DATA ####################

def update(request,id):
    if request.POST:
        name=request.POST.get('name')
        email=request.POST.get('email')  
        user=User(id=id,username=name,email=email)
        user.save()
        return redirect('adminhome')
    return redirect(request,'admin_home.html')

#################### DELETE USER DATA ####################

def delete(request,id):
    user=User.objects.filter(id=id)
    user.delete()
    return redirect('adminhome')

#################### USER SEARCH ####################

#searching algorithm implimentation...

def search(request):
    if request.method == 'POST':
        query = request.POST.get('query-search')
        user = User.objects.filter(username__icontains=query).order_by('-date_joined')
        return render(request, 'admin_home.html',{'user':user})
    return redirect('adminhome')