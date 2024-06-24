from django.urls import path
from .views import Home,About,Blog,Solutions,Projects,Contact,Blogdetails,Privacypolicy,Projectdetails,Digitalmarketing,Webdesgin,PaidAdvertising,Brandidentity,WhatsAppPromotion,EmailMarketing,EcommerceListing,Privacypolicy,Mobileprivacypolicy,Termsandconditions,Seo





urlpatterns = [
    path('', Home , name='home'),
    path('about/', About , name='about'),
    path('blog/', Blog , name='blog'),
    path('solutions/', Solutions , name='solutions'),
    path('digital-marketing-services-in-guntur/', Digitalmarketing , name='digital-marketing-services-in-guntur'),
    path('unbeatable-local-seo-services-in-guntur-best-provider/',Seo, name='seo'),
    path('website-services-in-guntur/', Webdesgin , name='website-services-in-guntur'),
    path('brandidentity/', Brandidentity , name='brandidentity'),
    path('paidadvertising/', PaidAdvertising , name='paidadvertising'),
    path('whatsAppPromotion/',WhatsAppPromotion , name='whatsApp Promotion'),
    path('emailMarketing/', EmailMarketing , name='emailMarketing'),
    path('ecommerceListing/', EcommerceListing , name='ecommerceListing'),
    path('projects/', Projects , name='projects'),
    path('projectdetails/', Projectdetails , name='projectdetails'),
    path('contact/', Contact , name='contact'),
    path('blog/<str:slug>', Blogdetails , name='blog'),
    path('privacypolicy', Privacypolicy , name='privacypolicy'),
    path('termsandconditions/', Termsandconditions , name='termsandconditions'),
    path('Privacypolicy/', Privacypolicy , name='Privacypolicy'),
    path('mobileprivacypolicy/', Mobileprivacypolicy , name='Mobileprivacypolicy'),
]

