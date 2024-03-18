from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from . models import Customer,Store,Order,Cart
from . forms import RegistrationForm,AuthenticateForm,ChangePasswordForm,UserProfileForm,AdminProfileForm,CustomerForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.db.models import F
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph , Table
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

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

def viewcart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total =0
    delhivery_charge =150
    gst_rate =0.05
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity 
        total += item.product.price_and_quantity_total
        final_price= delhivery_charge + total 
        final_price_with_gst= final_price * (1 + gst_rate)    # cart_items will fetch product of current user, and show product available in the cart of the current user.
    return render(request, 'viewcart.html', {'cart_items': cart_items , 'total':total,'final_price':final_price , 'final_price_with_gst':final_price_with_gst})

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


def delete_cart(request,id):
    if request.method == 'POST':
        de = Cart.objects.get(pk=id)
        de.delete()
    return redirect('viewcart')



def checkout(request):
    pass

#===================================== Address ============================================
def address(request):
    if request.method == 'POST':
            print(request.user)
            mf =CustomerForm(request.POST)
            print('mf',mf)
            if mf.is_valid():
                user=request.user                # user variable store the current user i.e steveroger
                name= mf.cleaned_data['name']
                address= mf.cleaned_data['address']
                city= mf.cleaned_data['city']
                state= mf.cleaned_data['state']
                pincode= mf.cleaned_data['pincode']
                print(state)
                print(city)
                print(name)
                Customer(user=user,name=name,address=address,city=city,state=state,pincode=pincode).save()
                return redirect('address')           
    else:
        mf =CustomerForm()
        address = Customer.objects.filter(user=request.user)
        print(address)
    return render(request,'address.html',{'mf':mf,'address':address})

    

def delete_address(request,id):
    if request.method == 'POST':
        de = Customer.objects.get(pk=id)
        de.delete()
    return redirect('address')


def generate_pdf(request):
    # Retrieve cart items and calculate total, delivery charges, and final price with GST
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity
        total += item.product.price_and_quantity_total
    delivery_charge = 150
    final_price = total + delivery_charge
    gst_rate = 0.05
    final_price_with_gst = final_price * (1 + gst_rate)

    # Create a buffer to store PDF data
    buffer = BytesIO()

    # Create a PDF object
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    # Sample stylesheet for formatting
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    # PDF content
    
    content = []
    content.append(Paragraph("Shopping Summary", normal_style))
    

    # Add table
    table_data = [["Product Name", "Product Price", "Product Quantity", "Total"]]
    for item in cart_items:
        table_data.append([
            item.product.name,
            f"{item.product.discounted_price}",
            item.quantity,
            f"{item.product.price_and_quantity_total}"
        ])
    table_data.extend([
        ["", "", "Order Price", f"{total}"],
        ["", "", "Delivery Charges", f"{delivery_charge}"],
        ["", "", "Subtotal", f"{final_price}"],
        ["", "", "GST", f"+ {gst_rate * 100}%"],
        ["", "", "Total Price", f"{final_price_with_gst}"]
    ])

    content.append(Table(table_data))

    # Build PDF
    pdf.build(content)

    # Get PDF data from buffer
    pdf_data = buffer.getvalue()
    buffer.close()

    # Create HTTP response with PDF as attachment
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="shopping_summary.pdf"'
    return response


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total =0
    delhivery_charge =150
    gst_rate =0.05
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity 
        total += item.product.price_and_quantity_total
        final_price= delhivery_charge + total 
    final_price_with_gst= final_price * (1 + gst_rate)


    address = Customer.objects.filter(user=request.user)

    
    return render(request, 'checkout.html', {'cart_items': cart_items,'total':total,'final_price':final_price ,'final_price_with_gst':final_price_with_gst,'address':address})

def payment(request):

    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')

    host = request.get_host()   # Will fecth the domain site is currently hosted on.
    cart_items = Cart.objects.filter(user=request.user)
    total =0
    delhivery_charge =150
    gst_rate =0.05
    for item in cart_items:
        item.product.price_and_quantity_total = item.product.discounted_price * item.quantity 
        total += item.product.price_and_quantity_total
        final_price= delhivery_charge + total 
    final_price_with_gst= final_price * (1 + gst_rate)

    
    address = Customer.objects.filter(user=request.user)

#=============================== Paypal Code ===============================================
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': final_price,
        'item_name': 'store',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}",
        'cancel_url': f"http://{host}{reverse('paymentfailed')}",
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

#==========================================================================================================
    return render(request, 'payment.html', {'cart_items': cart_items,'total':total,'final_price':final_price,'final_price_with_gst':final_price_with_gst,'address':address,'paypal':paypal_payment})

#===================================== Payment Success ============================================

def payment_success(request,selected_address_id):
    print('payment sucess',selected_address_id)   # we have fetch this id from return_url': f"http://{host}{reverse('paymentsuccess', args=[selected_address_id])}
                                                  # This id contain address detail of particular customer
    user =request.user
    customer_data = Customer.objects.get(pk=selected_address_id,)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        Order(user=user,customer=customer_data,Store=c.product,quantity=c.quantity).save()
        c.delete()
    return render(request,'paymentsuccess.html')


#===================================== Payment Failed ============================================


def payment_failed(request):
    return render(request,'paymentfailed.html')

#===================================== Order ====================================================

def order(request):
    ord=Order.objects.filter(user=request.user)
    return render(request,'order.html',{'ord':ord})


        
        
        
    

 
    