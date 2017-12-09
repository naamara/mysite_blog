from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from blog.models import Post, Category
from . import views



urlpatterns = [ url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-date")[:25], 
				template_name="blog/blog.html")),
				url(r'^(?P<pk>\d+)$', DetailView.as_view(model = Post, 
				template_name = 'blog/post.html')),
				url(r'^add_category/$', views.add_category, name="add_category"),
				url(r'^category/(?P<category_name_url>\w+)$', views.category, name='category'),
				url(r'^like_category/$', views.like_category, name='like_category'),
				url(r'^suggest_category/$', views.suggest_category, name='suggest_category')

			]
    
