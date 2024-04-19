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
            'digitalpromotions',
            'webdesgin',
            'brandidentity',
            'paidadvertising',
            'whatsApp Promotion',
            'emailMarketing',
            'ecommerceListing',
            'projects',
            'contact',
            'privacypolicy',
            'termsandconditions',
            
        ]
   
    
    def location(self,item):
        return reverse(item)
    