from django.db import models
from django.utils.text import slugify
# slugify:    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
#     Remove characters that aren't alphanumerics, underscores, or hyphens.
#     Convert to lowercase. Also strip leading and trailing whitespace.
from social import settings
# Create your models here.
import misaka
#misaka maintains structure of description text added....for example refer groups/test.py
from django.urls import  reverse


from django.contrib.auth import  get_user_model
User=get_user_model()



from django import template
register=template.Library()

class Group(models.Model):
    name=models.CharField(max_length=255,unique=True)
    slug=models.SlugField(allow_unicode=True,unique=True)
    description=models.TextField(blank=True,default='')
    description_html=models.TextField(editable=True,default='',blank=True)
    #Field.editable : If False, the field will not be displayed in the admin or any other ModelForm.
    # They are also skipped during model validation. Default is True.
    members=models.ManyToManyField(settings.AUTH_USER_MODEL,through='GroupMember')
    # members=models.ManyToManyField(User,through='GroupMember')


    def __str__(self):
        return self.name
    #A classic use-case for overriding the built-in methods is if you want
    #  something to happen whenever you save an object. For example (see save()
    def save(self,*args,**kwargs):
        self.slug=slugify(self.name)
        self.description_html=misaka.html(self.description)
        super().save(*args,**kwargs)

#This tells Django how to calculate the URL for an object.
    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})

    class Meta:
        ordering=['name']

class GroupMember(models.Model):
   group=models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
   user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user',on_delete=models.CASCADE)
   # user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)


   def __str__(self):
       return self.user.username


   class Meta:
       unique_together=['group','user']
