from django.contrib import admin

from contact.models import Contact

class ContactAdmin(admin.ModelAdmin):
  list_display = ('user', 'topic', 'message', 'date','status','comments' )
  list_filter = ('user', 'date', 'topic', 'status')

admin.site.register(Contact, ContactAdmin)