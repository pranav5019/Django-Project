from django.shortcuts import render,redirect
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

# Create your views here.
# def gun(request):
#     return render(request,'army.html')



def home(request):
    return render(request,'home.html')



def contact(request):
    return render(request,'contact.html')



def myorder(request):
    return render(request,'myorder.html')



# def order(request):
#     return render(request,'order.html')



def aei(request):
    return render(request,'aei.html')



def tshirt(request):
    return render(request,'tshirt.html')



def pant(request):
    return render(request,'pant.html')



def shoes(request):
    return render(request,'shoes.html')



def watch(request):
    return render(request,'watch.html')



def jacket(request):
    return render(request,'jacket.html')



def bags(request):
    return render(request,'bags.html')


def registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            mf = RegistrationForm(request.POST)
            if mf.is_valid():
                mf.save()
                return redirect('registration')    
        else:
            mf  = RegistrationForm()
        return render(request,'registration.html',{'mf':mf})
    else:
        return redirect('profile')

def log_in(request):
    if not request.user.is_authenticated: 
        if request.method == 'POST':      
            mf = AuthenticateForm(request,request.POST)
            if mf.is_valid():
                name = mf.cleaned_data['username']
                pas = mf.cleaned_data['password']
                user = authenticate(username=name, password=pas)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            mf = AuthenticateForm()
        return render(request,'login.html',{'mf':mf})
    else:
        return redirect('profile')

def profile(request):
    if request.user.is_authenticated:  
        if request.method == 'POST':
            if request.user.is_superuser == True:
                mf = AdminProfileForm(request.POST,instance=request.user)
            else:
                mf = UserProfileForm(request.POST,instance=request.user)
            if mf.is_valid():
                mf.save()
        else:
            if request.user.is_superuser == True:
                mf = AdminProfileForm(instance=request.user)
            else:
                mf = UserProfileForm(instance=request.user)
        return render(request,'profile.html',{'name':request.user,'mf':mf})
    else:                                               
        return redirect('login')

def log_out(request):
    logout(request)
    return redirect('home')


def changepassword(request):                                                      
    if request.user.is_authenticated:                              
        if request.method == 'POST':                               
            mf =ChangePasswordForm(request.user,request.POST)
            if mf.is_valid():
                mf.save()
                update_session_auth_hash(request,mf.user)
                return redirect('profile')
        else:
            mf = ChangePasswordForm(request.user)
        return render(request,'changepassword.html',{'mf':mf})
    else:
        return redirect('login')


