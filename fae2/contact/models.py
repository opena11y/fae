import datetime
import sys
import os
import string

from django.db import models

from django.contrib.auth.models import User

# User Contact (associated with contact form) 
class Contact(models.Model):
    id       = models.AutoField(primary_key=True)
    date     = models.DateTimeField(auto_now_add=True)
    user     = models.ForeignKey(User, editable=True)
    topic    = models.CharField(max_length=1024)
    message  = models.TextField()
    status   = models.CharField(max_length=128)
    comments = models.TextField()
    
