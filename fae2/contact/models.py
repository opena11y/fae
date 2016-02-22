import datetime
import sys
import os
import string

from django.db import models

from django.contrib.auth.models import User

CONTACT_STATUS = (
    ('NR',  'No Response'),
    ('FB',  'Filed bug'),
    ('FFR', 'Filed feature enhancment'),
    ('R',   'Responded'),
)

# User Contact (associated with contact form) 
class Contact(models.Model):
    id       = models.AutoField(primary_key=True)
    date     = models.DateTimeField(auto_now_add=True)
    user     = models.ForeignKey(User, editable=True, related_name="contacts")
    topic    = models.CharField(max_length=1024)
    message  = models.TextField()
    status   = models.CharField(max_length=128, choices=CONTACT_STATUS, default="NR")
    comments = models.TextField(blank=True, default="")
    
    def show_status(self):
        for shortp, longp in CONTACT_STATUS:
            if shortp == self.status:
                return longp