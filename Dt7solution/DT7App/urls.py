from django.urls import path
from .views import Home,About,Blog,Solutions,Projects,Contact,Blogdetails,Projectdetails,Solutiondetails



urlpatterns = [
    path('', Home , name='home'),
    path('about/', About , name='about'),
    path('blog/', Blog , name='blog'),
    path('solutions/', Solutions , name='solutions'),
    path('solutiondetails/', Solutiondetails , name='solutiondetails'),
    path('projects/', Projects , name='projects'),
    path('projectdetails/', Projectdetails , name='projectdetails'),
    path('contact/', Contact , name='contact'),
    path('blog/<str:slug>', Blogdetails , name='blog'),
]
