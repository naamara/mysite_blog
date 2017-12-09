# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render, render_to_response, get_object_or_404
from register.forms import UserProfileForm, UserForm

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login,logout
from django. contrib.auth.decorators import login_required

# Create your views here.
def register(request):
	#get the requests context
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful
	# Set to false initially. Code changes value to True when Registration succeds.
	registered = False

	#If its an HTTP POST, we are interested in processing the form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information
		# NOte that we make use of both UserForm and UserProfileForm
		user_form = UserForm(data = request.POST)
		profile_form = UserProfileForm(data = request.POST)

		#If the two formas are valid.....
		if user_form.is_valid() and profile_form.is_valid():
			#Save the user's form to the database.
			user = user_form.save()

			#now we hash the password with the set_password method.
			# ONce hashed, we can update the user OBject
			user.set_password(user.password)
			user.save()

			#Now sort out the UserProfile instance since we need to set the user attribute ourselves,
			# We set commit=False. THis delays saving the model until we're ready to avoid integrity problems
			profile = profile_form.save(commit=False)
			profile.user = user

			#Did the user provide a profile picture?
			#If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

				#Now we save the UserProfile model instance.
				profile.save()

				# Update our variable to tell the template registration was successful.
				registered = True

			#invalid form or forms - mistakes or something else?
			#Print problems to the terminal. they will also be shown to the user.
			else:
				print user_form.errors, profile_form,errors

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form =  UserProfileForm()

	#Render the template depending on the context.
	return render_to_response (
		'register/register.html',{'user_form': user_form, 'profile_form': profile_form, 
		'registered': registered})


def user_login(request):
	#like before, obtain the context for the user's request.
	context = RequestContext(request)

	#if the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		#Gather the username and password provided by the user.
		#This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']

		# Use Django's machinery to attempt to see if the username/password combination is 
		#valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)

		#If we have a User object, the details are correct.
		# if none (Python's way of representing the absence of a value), no answer with
		#Matching credentials were found.
		if user is not None:
			#Is the account active? it could have been disables.
			if user.is_active:
				#if the account is valid and active, we can log the user in.
				# we will send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your Systems account is disabled.")
		else:
			#bad login details were provided. so we cant log in the user
			print "Invalid login credentials: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login credentials supplied.")
	#the request is not an HTTP POST, so display the login form.
	#This scenario would most likely be a HTTP GET.
	else:
		#No context variables to pass to the template system, hence the blanck dictionary object...
		return render_to_response('register/login.html',{},context)

# Restricting Access directly, by examining the request object and check if the 
# user is authenticated, or,
#def some_view(request):
	#if not request.user.is_authenticated():
		#return HttpResponse("You are logged in.")
	#else:
		#return HttpResponse("You are not logged in.")

# Restricting using a convenience decorator function that check if the user is authenticated.
@login_required
def restricted(request):
	return HttpResponse("logged in, thats why you see this!")

@login_required
def user_logout(request):
	#Since we know the user is logged in, we can now just log them out.
	logout(request)

	#take the user back to the homepage.
	return HttpResponseRedirect('/')