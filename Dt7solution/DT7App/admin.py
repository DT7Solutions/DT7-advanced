from django.contrib import admin
from .models import FormsData,BlogPost,Category,BlogFAQ
# Register your models here.

class AdminHappyContact(admin.ModelAdmin):
    list_display=('Name','email','services_interested','message')
admin.site.register(FormsData,AdminHappyContact)

class BlogFAQInline(admin.TabularInline):  # or admin.StackedInline for bigger form
    model = BlogFAQ
    extra = 1  #
    
class AdminHappyBlogpost(admin.ModelAdmin):
    list_display=('Id','Category','Title','Tags','CreatedName','Create_at','status')
    list_filter = ["CreatedName",'Create_at']
    inlines = [BlogFAQInline]
admin.site.register(BlogPost,AdminHappyBlogpost)


class AdminHappyCategories(admin.ModelAdmin):
    list_display=('Name','Created')
admin.site.register(Category,AdminHappyCategories)



class BlogFAQAdmin(admin.ModelAdmin):
    list_display = ('blog', 'question', 'answer')
admin.site.register(BlogFAQ, BlogFAQAdmin)