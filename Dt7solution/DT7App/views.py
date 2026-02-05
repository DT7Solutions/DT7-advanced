import json
import requests
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import *
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages
from django.db import models
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from .context_processors import location_data
from .location_utils import get_nearest_city

@csrf_exempt
def Home(request):
    # location_data(request)
        latest_blogs = BlogPost.objects.filter().order_by('-Id')[:2]
        return render(request, 'uifiles/home.html',{'navbar':'Home','latest_blogs':latest_blogs})
        # If the request method is not POST, return an error response
    
def City_About(request, city=None):
    return render(request, 'uifiles/about.html',{'navbar':'About'})

def About(request):
    return render(request, 'uifiles/about.html',{'navbar':'About'})

def logos(request):
    return render(request, 'uifiles/logos.html')

def hyd_About(request):
    return render(request, 'uifiles/hyd-about.html',{'navbar':'About'})

def web_designing_in_guntur(request):
    return render(request, 'uifiles/web-designing-company-in-guntur.html')

def  web_development_in_hyderabad(request):
    return render(request, 'uifiles/web-development-company-in-hyderabad.html')

def web_designing_in_vijayawada(request):
    return render(request, 'uifiles/web-designing-company-in-vijayawada.html')

def brandmaterials(request):
    return render(request, 'uifiles/brandmaterials.html',{'navbar':'About'})

def Blog(request):
    blog = BlogPost.objects.filter().order_by('-Id')
    
    # allposts = BlogPost.objects.all()
    paginator = Paginator(blog, 10) 
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'uifiles/blog.html',{'blog':posts,'posts':posts,'page':page,'navbar':'Blog'})

def Blogdetails(request,slug):
    blog_list = BlogPost.objects.filter().order_by('-Id')[:3]
    selectpost = BlogPost.objects.get(Sluglink=slug)
    totalcategories = Category.objects.all()
    all_posts = BlogPost.objects.order_by('Id')
    faqs = selectpost.faqs.all()  # Get related FAQs

    selected_index = None
    for i, post in enumerate(all_posts):
        if post == selectpost:
            selected_index = i
            break

    # Initialize previous and next posts
    previous_post = None
    next_post = None

    if selected_index is not None:
        # Find the previous post
        if selected_index > 0:
            previous_post = all_posts[selected_index - 1]
        else:
            # If the selected post is the first post, set previous post to the last post
            previous_post = all_posts.last()

        # Find the next post
        if selected_index < len(all_posts) - 1:
            next_post = all_posts[selected_index + 1]
        else:
            # If the selected post is the last post, set next post to the first post
            next_post = all_posts.first()
    
    context =  {'selectpost':selectpost,'totalcategories':totalcategories,'blog_list':blog_list, 'meta_title': selectpost.MetaTitle,
        'meta_description': selectpost.MetaDescription,
        'meta_tags': selectpost.MetaKeywords,'previous_post': previous_post,'canonical_url':selectpost.Sluglink,
        'next_post': next_post,'navbar':'Blog', 'faqs': faqs}
    print(selectpost.MetaKeywords)

    return render(request, 'uifiles/blogdetails.html',context)   
 
def Solutions(request):
    return render(request, 'uifiles/service.html',{'navbar':'Solutions'})   

def Solutiondetails(request):
    return render(request, 'uifiles/services-details.html',{'navbar':'Solutions'}) 
  
def Projects(request):
    return render(request, 'uifiles/projects.html' ,{'navbar':'Projects'})

def Projectdetails(request):
    return render(request, 'uifiles/projects-details.html' ,{'navbar':'Projects'})

def Digitalmarketing(request):
    return render(request, 'uifiles/digital-marketing-services-in-guntur.html' ,{'navbar':'Solutions'})

def websitedesign(request):
    return render(request, 'uifiles/webdesgin.html' ,{'navbar':'Solutions'})

def Brandidentity(request):
    return render(request, 'uifiles/brandidentity.html' ,{'navbar':'Solutions'})

def WhatsAppPromotion(request):
    return render(request, 'uifiles/whatsapppromotion.html' ,{'navbar':'Solutions'})

def EmailMarketing(request):
    return render(request, 'uifiles/emailmarketing.html' ,{'navbar':'Solutions'})

def EcommerceListing(request):
    return render(request, 'uifiles/ecommercelisting.html' ,{'navbar':'Solutions'})

def PaidAdvertising(request):
    return render(request, 'uifiles/paidmarketing.html' ,{'navbar':'Solutions'})

def Seo(request):
    return render(request, 'uifiles/seo.html' ,{'navbar':'Solutions'})

def Privacypolicy(request):
    return render(request, 'uifiles/privacy-policy.html' ,{'navbar':'Home'})

def MobilePrivacypolicy(request):
    return render(request, 'uifiles/mobile-privacy-policy.html' ,{'navbar':'Home'})

def Termsandconditions(request):
    return render(request, 'uifiles/termsconditions.html')

# def Privacypolicy(request):
#     return render(request, 'uifiles/Privacypolicy.html')

def Mobileprivacypolicy(request):
    return render(request, 'uifiles/mobile-privacy-policy.html')

def productshoot(request):
    return render(request, 'uifiles/Product-shoot.html',{'navbar':'Solutions'})

# Carrer page views 
def Carrers(request):
    jobpost = JobPost.objects.filter(status=1).order_by('-Id')
    # allposts = BlogPost.objects.all()
    for post in jobpost:
        post.skills_list = [skill.strip() for skill in (post.Requirements or "").split(",") if skill.strip()]
    paginator = Paginator(jobpost, 6) 
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'uifiles/carrers.html',{'jobs':posts,'posts':posts,'page':page,'navbar':'Carrers'})

def Carrerdetails(request,id):
    job_item = JobPost.objects.filter(Id=id).first()

    if not job_item:
        return HttpResponse("Job Not Found", status=404)

    context = {
        "job_item": job_item,
        "meta_title": job_item.MetaTitle,
        "meta_description": job_item.MetaDescription,
        "meta_tags": job_item.MetaKeywords,
        "canonical_url": f"career/{job_item.Id}/"
    }

    return render(request, "uifiles/carrer-details.html", context)

@csrf_exempt
def apply_job_ajax(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        job_title = request.POST.get("job_title")
        resume = request.FILES.get("resume")

        if not resume:
            return JsonResponse({"status": "error", "message": "Resume is required"}, status=400)

        JobApplication.objects.create(
            full_name=full_name,
            email=email,
            message=message,
            job_title=job_title,
            resume=resume
        )

        return JsonResponse({"status": "success", "message": "Application submitted successfully!"})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)

def rss(request):
    return render(request, 'uifiles/rss.html')

def page_not_found_view(request, exception):
    return render(request, 'uifiles/404.html', status=404)
    
# @csrf_exempt
# def Contact(request):
#     if request.method == "POST":
#         first_name = request.POST.get('FirstName', "")
#         last_name = request.POST.get('LastName', "")
#         email = request.POST.get('Email', "")
#         services_interested = request.POST.getlist('ServicesInterestedIn', [])
#         message = request.POST.get('Message', "")
#         terms_and_conditions = request.POST.get('TermsAndConditions', "")
        

       
#         form_data = FormsData.objects.create(
#             Name=first_name + ' ' + last_name,
#             email=email,
#             services_interested=', '.join(services_interested),
#             message=message,
#             terms_and_conditions=terms_and_conditions
#         )
#         form_data.save()

      
#         try:
#             send_mail(
#                 'New Contact Form Submission', 
#                 f'Email : {email}\nMessage: {message}\nServices Interested In: {", ".join(services_interested)}',  
#                 'noreplaybadugudinesh94@gmail.com',  
#                 ['manideep723@gmail.com'],  
#                 fail_silently=False,  
#             )
#             messages.success(request, 'Message has been successfully sent.')
           
#         except Exception as e:
#             messages.error(request, f'Failed to send message. Error: {e}')
#             print("Error")

#         return render(request, 'uifiles/contact.html',{'navbar':'Contact'})  

#     else:
#         return render(request, 'uifiles/contact.html',{'navbar':'Contact'})

# @csrf_exempt
# def Contact(request):
#     if request.method == "POST":
#         try:
#             first_name = request.POST.get('FirstName', "").strip()
#             last_name = request.POST.get('LastName', "").strip()
#             email = request.POST.get('Email', "").strip()
#             services_interested = request.POST.getlist('ServicesInterestedIncontact', [])
#             message = request.POST.get('Message', "").strip()
#             terms_and_conditions = request.POST.get('TermsAndConditions', "").strip()

#             # Save form data
#             form_data = FormsData.objects.create(
#                 Name=f"{first_name} {last_name}",
#                 email=email,
#                 services_interested=', '.join(services_interested),
#                 message=message,
#                 terms_and_conditions=terms_and_conditions
#             )
#             print(f"Form saved successfully with ID {form_data.id}")

#             # Send email
#             send_mail(
#                 'New Contact Form Submission', 
#                 f'Email : {email}\nMessage: {message}\nServices Interested In: {", ".join(services_interested)}',  
#                 'noreplaybadugudinesh94@gmail.com',  
#                 ['dt7solutions@gmail.com'],  
#                 fail_silently=False,  
#             )
#             messages.success(request, 'Message has been successfully sent.')

#         except Exception as e:
#             print(f"Error: {e}")
#             messages.error(request, 'An error occurred. Please try again.')

#         return render(request, 'uifiles/contact.html', {'navbar': 'Contact'})
#     else:
#         return render(request, 'uifiles/contact.html', {'navbar': 'Contact'})

@csrf_exempt
def Contact(request):
    if request.method == "POST":
        # -------- Detect which form --------
        if request.POST.get("FirstName"):
            form_type = "CONTACT_FORM"
            first_name = request.POST.get("FirstName", "").strip()
            last_name = request.POST.get("LastName", "").strip()
            email = request.POST.get("Email", "").strip()
            message = request.POST.get("Message", "").strip()
            services = request.POST.getlist("ServicesInterestedIncontact")
        else:
            form_type = "ENQUIRY_FORM"
            first_name = request.POST.get("exampleInputName", "").strip()
            last_name = ""   # enquiry form has no last name
            email = request.POST.get("exampleInputEmail", "").strip()
            message = request.POST.get("exampleInputMessageinfo", "").strip()
            services = request.POST.getlist("servicesInterestedIn")

        # -------- Join services --------
        services_value = form_type
        if services:
            services_value = form_type + " | " + ", ".join(services)

        # -------- Save to DB --------
        FormsData.objects.create(
            Name=f"{first_name} {last_name}".strip(),
            email=email,
            services_interested=services_value,
            message=message,
            terms_and_conditions=""
        )
        return JsonResponse({"status": "success"})
    return render(request, "uifiles/contact.html", {"navbar": "Contact"})
    
#     # views.py
# from django.shortcuts import render
# import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# def get_geolocation(ip):
#     url = f'http://ip-api.com/json/{ip}'
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()
#     return None

# def my_view(request):
#     user_ip = get_client_ip(request)
#     location_data = get_geolocation(user_ip)

#     city = 'Unknown'
#     if location_data:
#         city = location_data.get('city', 'Unknown')

#     # Pass the city to the context, which will be inherited by base.html
#     return render(request, 'some_template.html', {'city': city})

@csrf_exempt
def set_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = data.get("lat")
            lng = data.get("lng")
            city = get_nearest_city(lat, lng)
            response = JsonResponse({"city": city})
            response.set_cookie( "user_city", city, max_age=60 * 60 * 24 * 30, ) # 30 days
            return response
        except Exception:
            pass
    # Fallback if geo blocked
    response = JsonResponse({"city": "guntur"})
    response.set_cookie("user_city", "guntur", max_age=60 * 60 * 24 * 30, path="/")
    return response