from django.urls import path
from . import views

urlpatterns = [
    path('',views.signup,name='signup'),#root url

    path('login/',views.loginPage,name='login'),
    path('home/',views.home,name='home'),
    path('logout/',views.logoutPage,name='logout'),  
    path('adminlogin/',views.AdminLogin,name='adminlogin'),   
    path('adminhome/',views.AdminHome,name='adminhome'), 
    #  crud oprations urls, below...
    path('add/',views.add,name='add'),   
    path('edit/',views.edit,name='edit'),   
    path('update/<str:id>',views.update,name='update'),   
    path('delete/<str:id>',views.delete,name='delete'),
    #search impimentation...
    path('search/',views.search,name='search'),
]


