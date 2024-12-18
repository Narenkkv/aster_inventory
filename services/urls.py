from django.urls import path
from . import views


urlpatterns = [

    path('',views.index, name='index'),
    path('productentry',views.productentry, name='productentry'),
    path('productlist/<search>/',views.productlist,name='productlist'),
    path('downloaddata/',views.download_data,name='download_data'),
    path('storelist/<search>/',views.storelist,name='storelist'),
    path('logout',views.logout,name='logout'),
    path('scanbarcode/',views.scanbarcode,name='scanbarcode'),
    path('storeexpiryreportdownload/',views.store_expiry_report_download_data,name='store_expiry_report_download_data'),
    path('storeexpiryproductentry/',views.store_expiry_data_entry,name='store_expiry_data_entry'),
]