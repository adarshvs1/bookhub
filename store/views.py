from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from store.forms import SignupForm , SignInForm ,UserProfileForm , BookForm ,ReviewForm

from django.views.generic import View ,TemplateView , UpdateView ,CreateView,DetailView,ListView,FormView

from django.contrib.auth import authenticate ,login,logout #security

from store.models import UserProfile  , Book , WishListItems,OrderSummary , Reviews #model,

from django.urls import reverse_lazy

from django.utils.decorators import method_decorator
from store.decorators import signin_required



class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignupForm()

        return render(request,'store/signup.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignupForm(request.POST)

        if form_instance.is_valid():

            form_instance.save()

            return redirect('signin')
        
        return render(request,'store/signup.html',{'form':form_instance})
    
#login

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form_instance=SignInForm()

        return render(request,'store/login.html',{'form':form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=SignInForm(request.POST)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            user_object=authenticate(request,**data)

            if user_object:

                login(request,user_object)

                return redirect('index')
            
        return render(request,'store/login.html',{'form':form_instance})


#Index View
@method_decorator(signin_required,name='dispatch')
class IndexView(View):

    template_name='store/index.html'

    def get(self,request,*args,**kwargs):

        qs=Book.objects.all()

        return render(request,self.template_name,{'books':qs})

#user profile update
@method_decorator(signin_required,name='dispatch')
class UserProfileUpdateView(UpdateView):

    model=UserProfile

    form_class=UserProfileForm

    template_name='store/profile_edit.html'

    success_url=reverse_lazy('index')


#book create
@method_decorator(signin_required,name='dispatch')
class BookCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=BookForm()
        return render(request,"store/book_add.html",{"form":form_instance})
    
    def post(self,request,*args,**kwargs):

        form_instance=BookForm(request.POST,files=request.FILES)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.save()

            return redirect("index")
        
        return render(request,"store/book_add.html",{"form":form_instance})

    # model=Book

    # form_class=BookForm

    # template_name='store/book_add.html'

    # success_url=reverse_lazy('index')

    # def form_valid(self,form): #before saving extra adding 

    #     form.instance.owner=self.request.user

    #     return super().form_valid(form)
    
#books list
@method_decorator(signin_required,name='dispatch')
class BookListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.books.all() #logged user added books

        return render(request,'store/mybooks.html',{'books':qs})
    

# book remove
@method_decorator(signin_required,name='dispatch')
class BookDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        Book.objects.get(id=id).delete()

        return redirect('mybooks')
    
#book detail view
@method_decorator(signin_required,name='dispatch')
class BookDetailView(DetailView):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        book=Book.objects.get(id=id)

        review=Reviews.objects.filter(book_object=book)

        print(review)

        return render(request,"store/book_detail.html",{"book":book,"review":review})




    
#Add to wishlist View
@method_decorator(signin_required,name='dispatch')
class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        book_obj=Book.objects.get(id=id)

        WishListItems.objects.create(wishlist_object=request.user.basket,
                                     book_object=book_obj)
        

        return redirect('index')
    
#cart

from django.db.models import Sum  #is used to see tha total amount of your cart items
@method_decorator(signin_required,name='dispatch')
class MyCartview(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)  #user >cart > cartitems

        total=request.user.basket.basket_items.filter(is_order_placed=False).values('book_object__price').aggregate(total= Sum('book_object__price')).get('total')

        return render(request,'store/cart_summary.html',{'cartitems':qs, "total":total})


#wishlist - delete 
@method_decorator(signin_required,name='dispatch')
class WishlistItemDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        WishListItems.objects.get(id=id).delete()

        return redirect('my-cart')
    
    
#chechout  view for getting book details and payment details
KEY_SECRET='qNa5Hxpai2N3y0sDnokqRube'

KEY_ID='rzp_test_CAcdb9Nz43lQUs'

import razorpay #payment
@method_decorator(signin_required,name='dispatch')
class CheckOutView(View):

    def get(self,request,*args,**kwargs):

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))    #site/python/paymentgateway


        total=request.user.basket.basket_items.filter(is_order_placed=False).values('book_object__price').aggregate(total= Sum('book_object__price')).get('total')

        print("==================================",total)
        amount=total*100

        #taking the total amount in the wishlist and converting into rupess

        data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_11" }

        payment = client.order.create(data=data)

        #create order_object

        cart_items=request.user.basket.basket_items.filter(is_order_placed=False)  #taking cart items

        Order_summary_obj=OrderSummary.objects.create(user_object=request.user,order_id=payment.get('id'),total = total ) #taking the total amount in orders)

        #Order_summary_obj.project_objects.add(cart_items.values('project_object'))

        for ci in cart_items: #taking cart items

            Order_summary_obj.book_objects.add(ci.book_object)  #taking the cart items

            Order_summary_obj.save()

        for ci in cart_items:

            ci.is_order_placed=True

            ci.save()
        
        

        # print(payment)  #id

        context={

            'key':KEY_ID,

            'amount':data.get('amount'),

            'currency':data.get('currency'),

            'order_id':payment.get('id')

        }

        return render(request,'store/payment.html',context)


#payment -verification

from django.views.decorators.csrf import csrf_exempt 

from django.utils.decorators import method_decorator #this decrtr is used to avoid csrf token checking

@method_decorator(csrf_exempt,name='dispatch')
@method_decorator(signin_required,name='dispatch')
class PaymentVerificationView(View):

    def post(self,request,*args,**kwargs):

        print(request.POST)

        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET)) #payment authentication

        order_summary_object=OrderSummary.objects.get(order_id=request.POST.get('razorpay_order_id')) #taking the user

        login(request,order_summary_object.user_object) 

        try:

            # error doubtful code
            client.utility.verify_payment_signature(request.POST)
            print('payment success')

            order_id=request.POST.get('razorpay_order_id')    #taking order id

            OrderSummary.objects.filter(order_id=order_id).update(is_paid=True)  #taking order summary and updating is_paid true



        except:

            print('payment failed')

            # handling code

        #return render(request,'store/success.html')

        return redirect('index')


#purchased
@method_decorator(signin_required,name='dispatch')
class MyPurchaseView(View):

    model=OrderSummary

    context_object_name='orders' #key

    def get(self,request,*args,**kwargs):

        qs=OrderSummary.objects.filter(user_object=request.user,is_paid=True)

        return render(request,'store/order_summary.html',{'orders':qs})


# reviews

#url :lh:8000/book/<int:pk>/review/add
@method_decorator(signin_required,name='dispatch')
class ReviewCreateView(FormView): 

    template_name='store/review.html'

    form_class=ReviewForm

    def post(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        book_obj=Book.objects.get(id=id)

        form_instance=ReviewForm(request.POST)

        if form_instance.is_valid():

            form_instance.instance.owner=request.user

            form_instance.instance.book_object=book_obj

            form_instance.save()

            return redirect('index')
        
        else:

            return render(request,self.template_name,{'form':form_instance})
        

#search -view
@method_decorator(signin_required,name='dispatch')
class SearchView(ListView):
    model = Book
    template_name = 'store/search.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            product = Book.objects.filter(title__contains=query)
            result = product
        else:
            result = None

        return result
    
#category dropdown
@method_decorator(signin_required,name='dispatch')
class DropDownView(View):
     
     def get(self,request,*args,**kwargs):
         
         print("=========================",request)
         form_no = request.GET["Category"]
    
         if form_no:

            book_obj=Book.objects.filter(category=form_no)


            print(book_obj)
            
    

            return render(request,"store/drop_result.html",{"book":book_obj})

     
        


#signout
@method_decorator(signin_required,name='dispatch')
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")





    

    

    


        







        