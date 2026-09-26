from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.



class FormsData(models.Model):
    
    Name = models.CharField(max_length=100)
    email = models.EmailField()
    services_interested = models.TextField()
    message = models.TextField()
    terms_and_conditions = models.TextField()


    def __str__(self):
        return self.Name


class Category(models.Model):
        Name = models.CharField(max_length=30,default="heading")
        Created = models.DateTimeField(default=datetime.now)
        def __str__(self):
            return self.Name
        
        class Meta:
            verbose_name ='Category'
            verbose_name_plural = 'Categories'

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)




class BlogPost(models.Model):
    Id = models.AutoField(primary_key=True)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='categories')
    Title =  models.CharField(max_length=225,default="title")
    # Description = models.CharField(max_length=2000,blank=True,null=True)
    Image1 = models.ImageField(upload_to='uploads/')
    Body = RichTextField(blank=True,null=True)
    Sluglink = models.CharField(max_length=200 ,blank=True,null=True)
    Tags = models.CharField(max_length=100 )
    CreatedName =  models.CharField(max_length=100)
    Create_at = models.DateTimeField(default=datetime.now)
    status = models.IntegerField(choices=STATUS, default=0)
    MetaTitle = models.CharField(max_length=255, blank=True,default="", null=True)
    MetaDescription = models.CharField(max_length=255, blank=True,default="", null=True)
    MetaKeywords = models.CharField(max_length=255, blank=True,default="", null=True)
   

    class Meta:
        ordering = ['-Create_at']

    def __str__(self):
            return self.Title
    

class BlogFAQ(models.Model):
    blog = models.ForeignKey(
        BlogPost,
        on_delete=models.CASCADE,
        related_name='faqs',
        blank=True,
        null=True
    )
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"{self.blog.Title} - {self.question}"
   

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)
DEPARTMENT_CHOICES = [
    ('Web Design and Development', 'Web Design and Development'),
    ('Designers', 'Designers'),
    ('Mobile App Developer', 'Mobile App Developer'),
    ('Social Media Marketing', 'Social Media Marketing'),
    ('E-commerce', 'E-commerce'),
    ('Email Marketing', 'Email Marketing'),
    ('Ecommerce Listing', 'Ecommerce Listing'),
    ('SEO Optimization', 'SEO Optimization'),
    ('Performance Marketing', 'Performance Marketing'),
    ('Full Stack Developer', 'Full Stack Developer'),
]

class JobPost(models.Model):
    Id = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=225, default="Job Title")
    Department = models.CharField(max_length=100,choices=DEPARTMENT_CHOICES,blank=True,null=True)
    ShortDescription = models.CharField(max_length=255, blank=True, default="", null=True)
    Location = models.CharField(max_length=150, blank=True, null=True)
    Experience = models.CharField(max_length=100, blank=True, null=True)
    Salary = models.CharField(max_length=100, blank=True, null=True)
    JobType = models.CharField(max_length=50, choices=[
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ], default='Full Time')
    Requirements = models.TextField(blank=True, null=True)
    Body = RichTextField(blank=True, null=True) 
    PostedBy = models.CharField(max_length=100, blank=True, null=True)
    PostedDate = models.DateTimeField(default=datetime.now)
    Deadline = models.DateField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    # SEO Fields
    MetaTitle = models.CharField(max_length=255, blank=True, default="", null=True)
    MetaDescription = models.CharField(max_length=255, blank=True, default="", null=True)
    MetaKeywords = models.CharField(max_length=255, blank=True, default="", null=True)

    class Meta:
        ordering = ['-PostedDate']

    def __str__(self):
        return self.Title


class JobApplication(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=13,null=True,default="")
    message = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    job_title = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)   # When record created
    updated_at = models.DateTimeField(auto_now=True)       # When updated

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"


class VisitorTracking(models.Model):
    visitor_id = models.CharField(max_length=100, unique=True, db_index=True, help_text="Unique Visitor ID")
    visit_count = models.IntegerField(default=1, help_text="Total visit count / sessions")
    device_type = models.CharField(max_length=50, default="Desktop", help_text="Mobile, Tablet, or Desktop")
    traffic_source = models.CharField(max_length=255, default="Direct", blank=True, help_text="Referrer domain or campaign source")
    pages_viewed = models.JSONField(default=list, blank=True, help_text="List of pages viewed by visitor")
    exit_page = models.CharField(max_length=255, default="", blank=True, help_text="Last visited page")
    scroll_depth = models.IntegerField(default=0, help_text="Maximum scroll depth percentage (0-100)")
    ip_address = models.CharField(max_length=45, blank=True, null=True, help_text="Visitor IP address")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Visitor Tracking'
        verbose_name_plural = 'Visitor Trackings'

    def __str__(self):
        return f"Visitor {self.visitor_id[:8]}... ({self.device_type}) - {self.visit_count} visits"


class VisitorPageHistory(models.Model):
    visitor = models.ForeignKey(VisitorTracking, on_delete=models.CASCADE, related_name="page_history", help_text="Associated Visitor")
    page_url = models.CharField(max_length=500, db_index=True, help_text="URL or Path visited")
    page_title = models.CharField(max_length=255, blank=True, default="", help_text="Title of the visited page")
    scroll_depth = models.IntegerField(default=0, help_text="Scroll depth percentage achieved on this page (0-100)")
    time_spent = models.IntegerField(default=0, help_text="Time spent on page in seconds")
    ip_address = models.CharField(max_length=45, blank=True, null=True, help_text="IP address at time of visit")
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True, help_text="Visit timestamp")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Visitor Page History'
        verbose_name_plural = 'Visitor Page Histories'

    def __str__(self):
        return f"{self.page_url} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"


class SpamSubmissionLog(models.Model):
    form_name = models.CharField(max_length=100, help_text="Form Name (Contact, Enquiry, Career, etc.)")
    name = models.CharField(max_length=255, blank=True, default="")
    email = models.CharField(max_length=255, blank=True, default="")
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    reason = models.CharField(max_length=255, help_text="Reason why submission was blocked (Honeypot, Time Trap, Keyword Spam, Rate Limit)")
    submitted_data = models.JSONField(default=dict, blank=True, help_text="Raw payload of the blocked spam submission")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Spam Submission Log'
        verbose_name_plural = 'Spam Submission Logs'

    def __str__(self):
        return f"Blocked {self.form_name} from {self.email or self.ip_address} ({self.reason})"

