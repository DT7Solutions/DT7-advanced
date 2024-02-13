from django.urls import path
from .views import Home,About,Blog,Solutions,Projects,Contact,Blogdetails



urlpatterns = [
    path('', Home , name='home'),
    path('about/', About , name='about'),
    path('blog/', Blog , name='blog'),
    path('solutions/', Solutions , name='solutions'),
    path('projects/', Projects , name='projects'),
    path('contact/', Contact , name='contact'),
    path('blog/<str:slug>', Blogdetails , name='blog'),
]
