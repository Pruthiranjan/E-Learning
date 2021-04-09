from django.urls import path
from PublicApp import views
from django.conf.urls import handler404
urlpatterns = [
    path('', views.Index, name="Home"),
    path('about/', views.About, name="about"),
    path('courses/', views.Courses, name="courses"),
    path('contact/', views.Contact, name="contact"),
    path('event_details/', views.Event_details, name="event_details"),
    path('elements/', views.Elements, name="elements"),
]
handler404 = views.error_404
