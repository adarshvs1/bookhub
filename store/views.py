from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect

# Create your views here.
from store.forms import SignupForm , SignInForm ,UserProfileForm , BookForm

from django.views.generic import View ,TemplateView , UpdateView ,CreateView,DetailView

from django.contrib.auth import authenticate ,login  #security

from store.models import UserProfile  , Book , WishListItems #model

from django.urls import reverse_lazy

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

class IndexView(View):

    template_name='store/index.html'

    def get(self,request,*args,**kwargs):

        qs=Book.objects.all()

        return render(request,self.template_name,{'books':qs})

#user profile update

class UserProfileUpdateView(UpdateView):

    model=UserProfile

    form_class=UserProfileForm

    template_name='store/profile_edit.html'

    success_url=reverse_lazy('index')


#book create

class BookCreateView(CreateView):

    model=Book

    form_class=BookForm

    template_name='store/book_add.html'

    success_url=reverse_lazy('index')

    def form_valid(self,form): #before saving extra adding 

        form.instance.owner=self.request.user

        return super().form_valid(form)
    
#books list

class BookListView(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.books.all()

        return render(request,'store/mybooks.html',{'books':qs})
    

# book remove

class BookDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        Book.objects.get(id=id).delete()

        return redirect('mybooks')
    
#book detail view

class BookDetailView(DetailView):

    template_name='store/book_detail.html'

    context_object_name='book' #key

    model=Book

#Add to wishlist View

class AddToWishListView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        book_obj=Book.objects.get(id=id)

        WishListItems.objects.create(wishlist_object=request.user.basket,
                                     book_object=book_obj)
        

        return redirect('index')
    
#cart

class MyCartview(View):

    def get(self,request,*args,**kwargs):

        qs=request.user.basket.basket_items.filter(is_order_placed=False)  #user >cart > cartitems

        return render(request,'cart_summary.html',{'cartitems':qs})

        


    

    

    


        







        