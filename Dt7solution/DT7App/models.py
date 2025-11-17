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
    message = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    job_title = models.CharField(max_length=250)

    created_at = models.DateTimeField(auto_now_add=True)   # When record created
    updated_at = models.DateTimeField(auto_now=True)       # When updated

    def __str__(self):
        return f"{self.full_name} - {self.job_title}"