"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# contact/models.py
from __future__ import absolute_import
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
    user     = models.ForeignKey(User, on_delete=models.CASCADE, editable=True, related_name="contacts")
    topic    = models.CharField(max_length=1024)
    message  = models.TextField()
    status   = models.CharField(max_length=128, choices=CONTACT_STATUS, default="NR")
    comments = models.TextField(blank=True, default="")

    class Meta:
        verbose_name        = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['-date']


    def show_status(self):
        for shortp, longp in CONTACT_STATUS:
            if shortp == self.status:
                return longp