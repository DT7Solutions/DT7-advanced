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


from .models import VisitorTracking, VisitorPageHistory, SpamSubmissionLog


class VisitorPageHistoryInline(admin.TabularInline):
    model = VisitorPageHistory
    extra = 0
    readonly_fields = ('page_url', 'page_title', 'scroll_depth', 'time_spent', 'ip_address', 'timestamp')
    can_delete = False
    ordering = ('-timestamp',)


class VisitorTrackingAdmin(admin.ModelAdmin):
    list_display = (
        'visitor_id',
        'device_type',
        'visit_count',
        'traffic_source',
        'exit_page',
        'scroll_depth',
        'ip_address',
        'updated_at'
    )
    list_filter = ('device_type', 'updated_at', 'created_at')
    search_fields = ('visitor_id', 'traffic_source', 'exit_page', 'ip_address')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [VisitorPageHistoryInline]

admin.site.register(VisitorTracking, VisitorTrackingAdmin)


class VisitorPageHistoryAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'page_url', 'page_title', 'scroll_depth', 'time_spent', 'ip_address', 'timestamp')
    list_filter = ('timestamp', 'scroll_depth')
    search_fields = ('visitor__visitor_id', 'page_url', 'page_title', 'ip_address')
    readonly_fields = ('timestamp',)

admin.site.register(VisitorPageHistory, VisitorPageHistoryAdmin)


class SpamSubmissionLogAdmin(admin.ModelAdmin):
    list_display = ('form_name', 'name', 'email', 'ip_address', 'reason', 'created_at')
    list_filter = ('form_name', 'reason', 'created_at')
    search_fields = ('name', 'email', 'ip_address', 'reason', 'submitted_data')
    readonly_fields = ('created_at',)

admin.site.register(SpamSubmissionLog, SpamSubmissionLogAdmin)

