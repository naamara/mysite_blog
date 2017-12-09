from django.conf.urls import  url, include
from register.models import UserProfile
from . import views



urlpatterns = [
			   url(r'^register/$', views.register, name="register"),
			   url(r'^login/$', views.user_login, name="user_login"),
			   url(r'^restricted/$', views.restricted, name ="restricted"),
			   url(r'^logout/$', views.user_logout, name="user_logout")
			   ] 
					

		
    
