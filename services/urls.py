from django.urls import path
from . import views


urlpatterns = [

    path('',views.index, name='index'),
    path('productentry',views.productentry, name='productentry'),
    path('productlist/<search>/',views.productlist,name='productlist'),
    path('downloaddata/',views.download_data,name='download_data'),
]