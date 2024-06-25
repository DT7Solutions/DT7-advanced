from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9 
    def items(self):
        return [
            'home',
            'about',
            'blog',
            'solutions',
            'digital-marketing-services-in-guntur',
            'website-services-in-guntur',
            'brandidentity',
            'paidadvertising',
            'whatsApp Promotion',
            'emailMarketing',
            'ecommerceListing',
            'projects',
            'contact',
            'privacypolicy',
            'Mobileprivacypolicy',
            'termsandconditions',
            
        ]
   
    
    def location(self,item):
        return reverse(item)
    