from django.contrib import admin
from .models import FormsData,BlogPost,Category
# Register your models here.

class AdminHappyContact(admin.ModelAdmin):
    list_display=('Name','email','services_interested','message')
admin.site.register(FormsData,AdminHappyContact)


class AdminHappyBlogpost(admin.ModelAdmin):
    list_display=('Id','Category','Title','Tags','CreatedName','Create_at','status')
    list_filter = ["CreatedName",'Create_at']
admin.site.register(BlogPost,AdminHappyBlogpost)


class AdminHappyCategories(admin.ModelAdmin):
    list_display=('Name','Created')
admin.site.register(Category,AdminHappyCategories)