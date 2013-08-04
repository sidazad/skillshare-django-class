from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Note(models.Model):
    owner=models.ForeignKey(User)
    title=models.CharField(max_length=100)
    text=models.CharField(max_length=500)
    createTime=models.DateTimeField()
    

from django.forms import ModelForm,Textarea

class NoteForm(ModelForm):
    class Meta:
        model=Note
        exclude=["owner"]
        widgets = {
            'text': Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        
        
        
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource


class NoteResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()
        resource_name = 'note'
        authorization= Authorization()
