from django.contrib import admin
from .models import *
from django.utils.html import format_html
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

    
class AdminHappyJobPost(admin.ModelAdmin):
    list_display=('Id','Title','Location','Experience','PostedDate','status')
    list_filter = ["PostedDate",'status']
admin.site.register(JobPost,AdminHappyJobPost)

class AdminHappyJobapplication(admin.ModelAdmin):
    list_display = (
        'id',
        'job_title',
        'full_name',
        'email',
        'message',
        'resume_link',  
        'created_at'
    )

    list_filter = ["job_title"]

    def resume_link(self, obj):
        if obj.resume:
            return format_html(
                '<a href="{}" download class="button">Download Resume</a>',
                obj.resume.url
            )
        return "No file"

    resume_link.short_description = "Resume"

admin.site.register(JobApplication, AdminHappyJobapplication)