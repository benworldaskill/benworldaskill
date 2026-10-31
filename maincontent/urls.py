from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("post/<uuid:pk>/", views.post_detail, name="post_detail"),
    path("contact/", views.contact_me, name="contact"),
    path('projects/', views.projects, name='projects'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search')
]
