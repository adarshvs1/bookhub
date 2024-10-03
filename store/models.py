from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):

    bio=models.CharField(max_length=250,null=True)

    profile_pic=models.ImageField(upload_to="profile_pictures",default='/profile_pictures/default.png')

    user_object=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')  #request.user.profile

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:

        return self.user_object.username
    

class Book(models.Model):

    title=models.CharField(max_length=200)

    author=models.CharField(max_length=200)

    description=models.TextField()

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='books')

    thumbnail=models.ImageField(upload_to='bookimages',default='/bookimages/default.png')

    price=models.PositiveIntegerField()

    files=models.FileField(null=True,upload_to='books')

    published_date=models.DateField()

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class WishList(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name='basket')

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)

class WishListItems(models.Model):

    wishlist_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name='basket_items')

    book_object=models.ForeignKey(Book,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class OrderSummary(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')

    book_objects=models.ManyToManyField(Book)

    order_id=models.CharField(max_length=200,null=True)

    is_paid=models.BooleanField(default=False)
    
    created_date=models.DateTimeField(auto_now_add=True)

    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


from django.db.models.signals import post_save  

#profile creating using signal

def create_profile(sender,instance,created,*args,**kwargs):

    if created:

        UserProfile.objects.create(user_object=instance)

post_save.connect(sender=User,receiver=create_profile)

#create basket

def create_basket(sender,instance,created,*args,**kwargs): #automatically creating

    if created:

        WishList.objects.create(owner=instance)

post_save.connect(sender=User,receiver=create_basket)




