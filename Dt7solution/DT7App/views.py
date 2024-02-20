from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import FormsData,BlogPost,Category
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages
# Create your views here.

def Home(request):
    return render(request, 'uifiles/home.html',{'navbar':'Home'})

def About(request):
    return render(request, 'uifiles/about.html',{'navbar':'About'})
def Blog(request):
    blog = BlogPost.objects.filter().order_by('-Id')
    
    # allposts = BlogPost.objects.all()
    paginator = Paginator(blog, 9) 
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'uifiles/blog.html',{'blog':posts,'posts':posts,'page':page})
def Blogdetails(request,slug):
    selectpost = BlogPost.objects.get(Sluglink=slug)
    
    # previous_post = BlogPost.objects.filter(id__lt=selectpost.id).order_by('-id').first()
    
    
    # next_post = BlogPost.objects.filter(id__gt=selectpost.id).first()
    return render(request, 'uifiles/blogdetails.html',{'selectpost':selectpost})    
def Solutions(request):
    return render(request, 'uifiles/service.html',{'navbar':'Solutions'})   
def Projects(request):
    return render(request, 'uifiles/projects.html' ,{'navbar':'Projects'})
def Projectdetails(request):
    return render(request, 'uifiles/projects-details.html' ,{'navbar':'Projects'})
# def Contact(request):
#     if request.method == "POST":
#         first_name = request.POST.get('firstName',"")
#         last_name = request.POST.get('lastName',"")
#         email = request.POST.get('email',"")
#         services_interested = request.POST.getlist('servicesInterestedIn',"")
#         message = request.POST.get('message',"")
#         terms_and_conditions = request.POST.get('termsAndConditions',"")

      
#         form_data = FormsData.objects.create(
#             first_name=first_name,
#             last_name=last_name,
#             Name = first_name + last_name,
#             email=email,
#             services_interested=', '.join(services_interested),
#             message=message,
#             terms_and_conditions=terms_and_conditions
#         )
#         form_data.save()
#         return render(request, 'uifiles/contact.html')  
        
#     else:
#        return render(request, 'uifiles/contact.html')  
def Contact(request):
    if request.method == "POST":
        first_name = request.POST.get('firstName', "")
        last_name = request.POST.get('lastName', "")
        email = request.POST.get('email', "")
        services_interested = request.POST.getlist('servicesInterestedIn', [])
        message = request.POST.get('message', "")
        terms_and_conditions = request.POST.get('termsAndConditions', "")

        # Save form data to the model
        form_data = FormsData.objects.create(
            Name=first_name + ' ' + last_name,
            email=email,
            services_interested=', '.join(services_interested),
            message=message,
            terms_and_conditions=terms_and_conditions
        )
        form_data.save()

        # Send email
        try:
            send_mail(
                'New Contact Form Submission',  # Subject
                f'Email : {email}\nMessage: {message}\nServices Interested In: {", ".join(services_interested)}',  # Message
                'noreplaybadugudinesh94@gmail.com',  # Sender's email
                ['manideep723@gmail.com'],  # Recipient list
                fail_silently=False,  # Raise exception if sending fails
            )
            messages.success(request, 'Message has been successfully sent.')
           
        except Exception as e:
            messages.error(request, f'Failed to send message. Error: {e}')
            print("Error")

        return render(request, 'uifiles/contact.html',{'navbar':'Contact'})  

    else:
        return render(request, 'uifiles/contact.html',{'navbar':'Contact'})