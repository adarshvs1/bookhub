"""
URL configuration for bookhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#image
from django.conf import settings
from django.conf.urls.static import static

from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #registraion

    path('register/',views.SignUpView.as_view(),name='signup'),

    #login

    path('',views.SignInView.as_view(),name='signin'),

    #index

    path('index/',views.IndexView.as_view(),name='index'),

    #profile -edit

    path('profile/<int:pk>/change/',views.UserProfileUpdateView.as_view(),name='profile-update'),

    #book add

    path('books/add/',views.BookCreateView.as_view(),name='book-add'),

    #book-list

    path('books/all/',views.BookListView.as_view(),name='mybooks'),

    #book-delete

    path('book/<int:pk>/remove/',views.BookDeleteView.as_view(),name='book-delete'),

    #book-detail

    path('book/<int:pk>/',views.BookDetailView.as_view(),name='book-detail'),

    #book add wishlist

    path('book/<int:pk>/wishlist-add',views.AddToWishListView.as_view(),name='add-to-wishlistitems'),

    #wishlist

    path('wishlist/summary/',views.MyCartview.as_view(),name='my-cart'),

    #wishlist -delete

    path('wishlist/items/<int:pk>/remove/',views.WishlistItemDeleteView.as_view(),name='cartitem-delete'),

    #checkout-view

    path("checkout/",views.CheckOutView.as_view(),name="book-checkout"),

    #payment-post method of razor pay

    path("payment/verification/",views.PaymentVerificationView.as_view(),name="books-payment"),

    #my-orders

    path('order/summary/',views.MyPurchaseView.as_view(),name='order-summary'),

    #review

    path('book/<int:pk>/review/add/',views.ReviewCreateView.as_view(),name='review-add'),

    #drop down category

    path("drop/down",views.DropDownView.as_view(),name="drop-down"),

    #logout view

    path("signout",views.SignOutView.as_view(),name="logout"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
