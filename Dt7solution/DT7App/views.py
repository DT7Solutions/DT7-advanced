from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import FormsData,BlogPost,Category
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail,EmailMessage
from django.contrib import messages
from django.db import models
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Home(request):
    
    if request.method == 'POST':
       
        name = request.POST.get('exampleInputName', "")
        email = request.POST.get('exampleInputEmail', "")
        phone = request.POST.get('exampleInputPhone', "")
        services_interested = request.POST.getlist('servicesInterestedIn', [])
        message = request.POST.get('exampleInputMessageinfo', "")

        

        # Here you can process the data as needed, such as saving it to a database
        
        # For example, you could print the data to the console
        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)
        print("Service:", services_interested)
        print("Message:", message)


        try:

            send_mail(
                'New Contact Form Submission',  # Subject
                f'Email : {email}\nMessage: {message}\nPhone:{phone}\nServices Interested In: {", ".join(services_interested)}',  # Message
                'manideepmadhuri456@gmail.com',  # Sender's email
                ['manideep723@gmail.com'],  # Recipient list
                fail_silently=False,  # Raise exception if sending fails
            )
            messages.success(request, 'Message has been successfully sent.')
           
        except Exception as e:
            messages.error(request, f'Failed to send message. Error: {e}')
            print("Error")
        latest_blogs = BlogPost.objects.filter().order_by('-Id')[:2]
        return render(request, 'uifiles/home.html',{'navbar':'Home','latest_blogs':latest_blogs})  

    else:
        latest_blogs = BlogPost.objects.filter().order_by('-Id')[:2]
        return render(request, 'uifiles/home.html',{'navbar':'Home','latest_blogs':latest_blogs})
   
        # If the request method is not POST, return an error response
        
    

def About(request):
    return render(request, 'uifiles/about.html',{'navbar':'About'})
def Blog(request):
    blog = BlogPost.objects.filter().order_by('-Id')
    
    # allposts = BlogPost.objects.all()
    paginator = Paginator(blog, 9) 
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'uifiles/blog.html',{'blog':posts,'posts':posts,'page':page,'navbar':'Blog'})
def Blogdetails(request,slug):
    blog_list = BlogPost.objects.filter().order_by('-Id')[:3]
    selectpost = BlogPost.objects.get(Sluglink=slug)
    totalcategories = Category.objects.all()
    all_posts = BlogPost.objects.order_by('Id')

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
        'meta_tags': selectpost.MetaKeywords,'previous_post': previous_post,
        'next_post': next_post,'navbar':'Blog'}
    print(next_post,previous_post)

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
def Webdesgin(request):
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
def Privacypolicy(request):
    return render(request, 'uifiles/privacy-policy.html')
def Mobileprivacypolicy(request):
    return render(request, 'uifiles/mobile-privacy-policy.html')



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
                ['hello@dt7.agency'],  # Recipient list
                fail_silently=False,  # Raise exception if sending fails
            )
            messages.success(request, 'Message has been successfully sent.')
           
        except Exception as e:
            messages.error(request, f'Failed to send message. Error: {e}')
            print("Error")

        return render(request, 'uifiles/contact.html',{'navbar':'Contact'})  

    else:
        return render(request, 'uifiles/contact.html',{'navbar':'Contact'})