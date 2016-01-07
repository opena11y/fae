from django.contrib import admin

from userProfiles.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'acct_type', 'org', 'max_archive', 'max_saved')
    list_filter  = ('acct_type', 'org')

admin.site.register(UserProfile, UserProfileAdmin)
