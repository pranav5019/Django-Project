from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Customer,Store,Order,Cart
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash

# Create your views here.
# def gun(request):
#     return render(request,'army.html')

class HomeView(View):
    def get(self,request):
        return render(request,'home.html')


def contact(request):
    return render(request,'contact.html')


def myorder(request):
    return render(request,'myorder.html')









# def order(request):
#     return render(request,'order.html')



def aei(request):
    return render(request,'aei.html')

class TshirtView(View):
    def get(self,request):
        tshirt = Store.objects.filter(category='TSHIRT')
        return render(request,'tshirt.html',{'tshirt':tshirt})


class PantView(View):
    def get(self,request):
        pant = Store.objects.filter(category='PANT')
        return render(request,'pant.html',{'pant':pant})



class ShoesView(View):
    def get(self,request):
        shoes = Store.objects.filter(category='SHOES')
        return render(request,'shoes.html',{'shoes':shoes})



class WatchView(View):
    def get(self,request):
        watch = Store.objects.filter(category='WATCH')
        return render(request,'watch.html',{'watch':watch})



class JacketView(View):
    def get(self,request):
        jacket = Store.objects.filter(category='JACKET')
        return render(request,'jacket.html',{'jacket':jacket})



class BagsView(View):
    def get(self,request):
        bags = Store.objects.filter(category='BAGS')
        return render(request,'bags.html',{'bags':bags})

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
    

class StoreDetailView(View):
    def get(self,request,id):     # id = It will fetch id of particular Store 
        store = Store.objects.get(pk=id)

        #------ code for caculate percentage -----
        if Store.discounted_price !=0:    # fetch discount price of particular Store
            percentage = int(((store.selling_price-store.discounted_price)/store.selling_price)*100)
        else:
            percentage = 0
        # ------ code end for caculate percentage ---------
            
        return render(request,'storedetails.html',{'store':store,'percentage':percentage})


def add_to_cart(request, id):    # This 'id' is coming from 'Store.id' which hold the id of current Store , which is passing through {% url 'addtocart' Store.id %} from Store_detail.html 
    if request.user.is_authenticated:
        product = Store.objects.get(pk=id) # product variable is holding data of current object which is passed through 'id' from parameter
        user=request.user                # user variable store the current user i.e steveroger
        Cart(user=user,product=product).save()  # In cart model current user i.e steveroger will save in user variable and current Store object will be save in product variable
        return redirect('storedetails', id)       # finally it will redirect to Store_details.html with current object 'id' to display Store after adding to the cart
    else:
        return redirect('login')                # If user is not login it will redirect to login page

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)      # cart_items will fetch product of current user, and show product available in the cart of the current user.
    return render(request, 'army.html', {'cart_items': cart_items})

def add_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)    # If the object is found, it returns the object. If not, it raises an HTTP 404 exception (Http404).
    product.quantity += 1                       # If object found it will be add 1 quantity to the current object   
    product.save()
    return redirect('viewcart')

def delete_quantity(request, id):
    product = get_object_or_404(Cart, pk=id)
    if product.quantity > 1:
        product.quantity -= 1
        product.save()
    return redirect('viewcart')
