# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from blog.forms import CategoryForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def blog(request):
 	return render(request, "blog/blog.html")	

def add_category(request):
	
	# Get the context from the request.
	# Access the context sorrounding the HTTP Request that allow us determine 
	# the type  being made whether it be HTTP GET or POST
	context =  RequestContext(request)

	# A HTTP POST?
	if request.method == 'POST':

		#showing a new, blank form for adding a category;
		form =  CategoryForm(request.POST)

		# Have we been provided with a valid form?
		if form.is_valid():
			
			# Save the new category to the database.
			form.save(commit=True)

			# Now call the index() view.
			# THe user will be shown the app homepage.
			return index(request)
		else:
			# The supplied form contained errors - just print them to the terminal.
			# if there are errors, redisplay the form with error messages.
			print form.errors
	else:
		
		#if the request was not a POST, display the form to enter details.
		form = CategoryForm()

	# Bad form (or form details), no form supplied...
	# Render the form with error messages (if any).
	return render_to_response('blog/add_category.html', {'form': form}, context)

#display the number of likes and the “Likes” button
def category(request, category_name_url):
	context = RequestContext(request)
	cat_list = get_category_list()
	category_name = decode_url(category_name_url)
	context_dict = {'cat_list': cat_list, 'category_name': category_name}

	try:
		category = Category.objects.get(name=category_name)
		#Add category to the context so that we can access the id and likes
		context_dict['category'] = category

		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
	except Category.DoesNotExist:
		pass

	return render_to_response('blog/category.html',context_dict. context)

#which will examine the request and pick out the
#category_id and then increment the number of likes for that category.

@login_required
def like_category(request):
	context = RequestContext(request)
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
	likes = 0
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		if category:
			likes = category.likes + 1
			category.likes = likes
			category.save()
	return HttpResponse(likes)

#we use a filter to find all the categories that start with the string supplied.
def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__startswith = starts_with)
	else:
		cat_list =  Category.objects.all()
	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]
	for cat in cat_list:
		cat.url =  encode_url(cat.name)
	return cat_list

#create a view that returns the top 8 matching results
def suggest_category(request):
	context = RequestContext(request)
	cat_list = []
	starts_with = ''
	if request.method == 'GET':
		starts_with = request.GET['suggestion']
	else:
		starts_with = request.POST['suggestion']
		cat_list = get_category_list (8, starts_with)
	return render_to_response('register/category_list.html', {'cat_list': cat_list}, context)


@login_required
def auto_add_page(request):
	context = RequestContext(request)
	cat_id = None
	url = None
	title = None
	context_dict = {}
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		url = request.GET['url']
		title = request.GET['title']
	if cat_id:
		category = Category.objects.get(id=int(cat_id))
		p = Page.objects.get_or_create(category=category, title=title, url=url)
		pages = Page.objects.filter(category=category).order_by('-views')
	# Adds our results list to the template context under name pages.
	context_dict['pages'] = pages
	return render_to_response('register/page_list.html', context_dict, context)
