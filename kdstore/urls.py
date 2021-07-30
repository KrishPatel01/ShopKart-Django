from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.userLogin, name="userLogin"),
    path('logout/', views.userLogout, name="userLogout"),
    path('signup/', views.signUp, name="signUp"),
    path('signUpPage/', views.signUpPage, name="signUpPage"),
    path('loginPage/', views.loginPage,  name="loginPage"),
    path('userProfile/', views.userProfile, name="userProfile"),
    path('editProfilePage/', views.editProfilePage, name="editProfilePage"),
    path('editProfile/', views.editProfile, name="editProfile"),
    path('categoryProduct/<str:category>', views.categoryProduct, name="categoryProduct"),
    path('contactUs/', views.contactUs, name="contactUs"),
    path('products/', views.products, name="products"),
    path('offers/', views.offers, name="offers"),
    path('about/', views.about, name='about'),
    path('product/<int:myid>', views.productInfo, name="productInfo"),
    path('productComment/', views.productComment, name="productComment"),
    path('moreComments/<int:myid>', views.moreComments, name="moreComments"),
    path('productRating/', views.productRating, name="productRating"),
    path('search/', views.search, name="search"),
    path('cart/',views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order/', views.order, name='order'),
    path('payment-request/', views.paymentRequest, name='paymentRequest')
]
