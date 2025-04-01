import os
from services.models import Usermaster,StoreMaster
from django.contrib import messages

def inital_data(request):
    try:
        name = None
        isdownload = None
        storeName = None
        if 'username' in request.session:
            session_username = request.session['username']
            data =  Usermaster.objects.filter(name=session_username).get()
            if 'storeid' in request.session:
                getstorename = StoreMaster.objects.get(d_365_store_id = request.session['storeid'])
                storeName = getstorename.d_365_store_id+'_'+getstorename.store_name_as_per_d_365
            name = data.name
            isdownload = data.isdownload
        return dict(
        name = name,
        isdownload = isdownload,
        storeName = storeName
    ) 
    except Exception as e:
        print(f"Error in onload function: {e}")
        messages.info(request, "Please sign out and sign in again to view the changes.")
        return {'Error': True}