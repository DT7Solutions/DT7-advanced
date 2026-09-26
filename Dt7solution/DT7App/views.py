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
from Dt7solution.settings import DEBUG



@csrf_exempt
def Home(request):
    # location_data(request)
        latest_blogs = BlogPost.objects.filter().order_by('-Id')[:2]
        return render(request, 'uifiles/home.html',{'navbar':'Home','latest_blogs':latest_blogs})
        # If the request method is not POST, return an error response
    
def City_About(request, city):
    city_slug = city.lower()
    city_name = city_slug.replace("-", " ").title()
    return render(request, 'uifiles/city-about.html',{'navbar':'About','city': city_slug, 'city_name': city_name})

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
    return render(request, 'uifiles/service.html',{'navbar':'Solutions'})
 
  
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
    if DEBUG:
        host_url = "http://127.0.0.1:8000"
        print("DEBUG is False: Using local host URL")
    else:
        host_url = "https://dt7.agency"
        print("DEBUG is True: Using production host URL")

    return render(request, 'uifiles/carrers.html',{'jobs':posts,'posts':posts,'page':page,'navbar':'Carrers','host_url': host_url})

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

from .anti_spam import is_spam_submission

@csrf_exempt
def apply_job_ajax(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()
        job_title = request.POST.get("job_title", "").strip()
        resume = request.FILES.get("resume")

        # Anti-spam protection check
        is_spam, reason = is_spam_submission(request, form_name="Job Application", name=full_name, email=email, message=message)
        if is_spam:
            # Silently discard spam without alerting bots
            return JsonResponse({"status": "success", "message": "Application submitted successfully!"})

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

        # -------- Anti-spam protection check --------
        full_name = f"{first_name} {last_name}".strip()
        is_spam, reason = is_spam_submission(request, form_name=form_type, name=full_name, email=email, message=message)
        if is_spam:
            # Silently discard spam without alerting bots
            return JsonResponse({"status": "success"})

        # -------- Join services --------
        services_value = form_type
        if services:
            services_value = form_type + " | " + ", ".join(services)

        # -------- Save to DB --------
        FormsData.objects.create(
            Name=full_name,
            email=email,
            services_interested=services_value,
            message=message,
            terms_and_conditions=""
        )
        return JsonResponse({"status": "success"})
    return render(request, "uifiles/contact.html", {"navbar": "Contact"})


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
    response = JsonResponse({"city": "guntur"})
    response.set_cookie("user_city", "guntur", max_age=60 * 60 * 24 * 30, path="/")
    return response

import uuid

import datetime
from django.utils import timezone

@csrf_exempt
def track_visitor_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            data = {}

        visitor_id = data.get("visitor_id") or request.COOKIES.get("visitor_id") or str(uuid.uuid4())
        current_page = data.get("current_page") or request.META.get("HTTP_REFERER", "/") or "/"
        page_title = (data.get("page_title") or "")[:250]
        
        try:
            scroll_depth = int(data.get("scroll_depth", 0))
        except (ValueError, TypeError):
            scroll_depth = 0

        try:
            time_spent = int(data.get("time_spent", 0))
        except (ValueError, TypeError):
            time_spent = 0

        history_id = data.get("history_id")
        referrer = data.get("referrer") or request.META.get("HTTP_REFERER", "")

        # Device Type Detection
        user_agent = request.META.get("HTTP_USER_AGENT", "").lower()
        if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
            device_type = "Mobile"
        elif "ipad" in user_agent or "tablet" in user_agent:
            device_type = "Tablet"
        else:
            device_type = "Desktop"

        # Traffic Source Detection
        traffic_source = "Direct"
        if referrer:
            if "google." in referrer:
                traffic_source = "Google Organic"
            elif "bing." in referrer:
                traffic_source = "Bing Organic"
            elif "facebook." in referrer or "instagram." in referrer or "linkedin." in referrer:
                traffic_source = "Social Media"
            elif "dt7.agency" not in referrer:
                traffic_source = referrer[:250]

        # IP Address
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = x_forwarded_for.split(",")[0].strip() if x_forwarded_for else request.META.get("REMOTE_ADDR")

        # Get or create Visitor Record
        visitor, created = VisitorTracking.objects.get_or_create(
            visitor_id=visitor_id,
            defaults={
                "device_type": device_type,
                "traffic_source": traffic_source,
                "pages_viewed": [current_page],
                "exit_page": current_page,
                "scroll_depth": min(max(scroll_depth, 0), 100),
                "ip_address": ip,
                "visit_count": 1,
            }
        )

        if not created:
            pages = list(visitor.pages_viewed or [])
            if not pages or pages[-1] != current_page:
                pages.append(current_page)
                visitor.pages_viewed = pages
                visitor.visit_count += 1

            visitor.exit_page = current_page
            if scroll_depth > visitor.scroll_depth:
                visitor.scroll_depth = min(scroll_depth, 100)

            visitor.device_type = device_type
            if traffic_source != "Direct" and visitor.traffic_source == "Direct":
                visitor.traffic_source = traffic_source
            visitor.ip_address = ip
            visitor.save()

        # Page-wise Tracking History record
        history_record = None
        if history_id:
            try:
                history_record = VisitorPageHistory.objects.get(id=history_id, visitor=visitor)
            except VisitorPageHistory.DoesNotExist:
                history_record = None

        if not history_record:
            fifteen_mins_ago = timezone.now() - datetime.timedelta(minutes=15)
            history_record = VisitorPageHistory.objects.filter(
                visitor=visitor,
                page_url=current_page,
                timestamp__gte=fifteen_mins_ago
            ).order_by('-timestamp').first()

        if history_record:
            history_record.scroll_depth = max(history_record.scroll_depth, min(max(scroll_depth, 0), 100))
            if time_spent > history_record.time_spent:
                history_record.time_spent = time_spent
            if page_title and not history_record.page_title:
                history_record.page_title = page_title
            history_record.save()
        else:
            history_record = VisitorPageHistory.objects.create(
                visitor=visitor,
                page_url=current_page,
                page_title=page_title,
                scroll_depth=min(max(scroll_depth, 0), 100),
                time_spent=time_spent,
                ip_address=ip
            )

        response = JsonResponse({
            "status": "success",
            "visitor_id": visitor_id,
            "visit_count": visitor.visit_count,
            "history_id": history_record.id if history_record else None
        })

        # Set persistent cookies
        response.set_cookie("visitor_id", visitor_id, max_age=60 * 60 * 24 * 365, path="/")
        response.set_cookie("cookieConsent", "true", max_age=60 * 60 * 24 * 365, path="/")
        return response

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)
