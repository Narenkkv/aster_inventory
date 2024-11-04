import os
from services.models import Usermaster
from django.contrib import messages

def inital_data(request):
    try:
        name = None
        isdownload = None
        if 'username' in request.session:
            session_username = request.session['username']
            data =  Usermaster.objects.filter(name=session_username).get()
            name = data.name
            isdownload = data.isdownload
        return dict(
        name = name,
        isdownload = isdownload,
    ) 
    except Exception as e:
        print(f"Error in onload function: {e}")
        messages.info(request, "Please sign out and sign in again to view the changes.")
        return {'Error': True}