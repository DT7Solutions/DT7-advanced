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

    class Meta:
        ordering = ['-Create_at']

    def __str__(self):
            return self.Title
    