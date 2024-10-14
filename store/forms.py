from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from store.models import UserProfile ,Book,Reviews


class SignupForm(UserCreationForm):  #registration

    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':"bg-gray-100 w-full text-sm text-gray-800 px-4 py-4 focus:bg-transparent outline-orange-300 transition-all", 'placeholder':"Enter password"}))

    password2=forms.CharField(widget=forms.TextInput(attrs={'class':'bg-gray-100 w-full text-sm text-gray-800 px-4 py-4 focus:bg-transparent outline-orange-300 transition-all','placeholder':'confirm password'}))

    class Meta:

        model=User

        fields=['username','email','password1','password2']

        widgets={

            'username':forms.TextInput(attrs={'class':"bg-gray-100 w-full text-sm text-gray-800 px-4 py-4 focus:bg-transparent outline-orange-300 transition-all","placeholder":"enter name"}),

            'email':forms.EmailInput(attrs={'class':"bg-gray-100 w-full text-sm text-gray-800 px-4 py-4 focus:bg-transparent outline-orange-300 transition-all",'placeholder':'enter email'})
        }


#signin

class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={'class':"w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"}))

    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':"w-full border border-gray-300 rounded-md py-2 px-3 focus:outline-none focus:border-blue-500"}))


#user profile

class UserProfileForm(forms.ModelForm):

    class Meta:

        model=UserProfile

        fields=['bio','profile_pic']

        widgets={

            'bio':forms.TextInput(attrs={'class':'w-medium border p-2 my-3'}),

            'profile_pic':forms.FileInput(attrs={'class':'w-full border p-2 my-3'})
        }



class BookForm(forms.ModelForm): 

   

    class Meta:

        model=Book

        exclude=('owner','created_date','updated_date','is_active')

        widgets={

            'title':forms.TextInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            'author':forms.TextInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            'description':forms.Textarea(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2 h-12'}),

            'thumbnail':forms.FileInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            'price':forms.NumberInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            'files':forms.FileInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            'published_date':forms.DateInput(attrs={'class':'w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2'}),

            
            "category":forms.Select(attrs={"class":"w-full rounded-md border bg-white py-2 px-2 outline-none ring-yellow-500 focus:ring-2"}) 

        
            
        }


# reviews

class ReviewForm(forms.ModelForm):

    class Meta:

        model=Reviews

        fields= ['comment','rating']

        widgets={
            "comment":forms.Textarea(attrs={"class":"form-control mb-2 ","rows":5}),
            "rating":forms.NumberInput(attrs={"class":"form-control mb-2 "})
        }


