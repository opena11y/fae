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


from datetime import datetime, timedelta

from django.db import models

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from websiteResultGroups.models import WebsiteReportGroup
from rulesets.models            import Ruleset



# ---------------------------------------------------------------
#
# StatsAll
#
# ---------------------------------------------------------------

class StatsAll(models.Model):
    id   = models.AutoField(primary_key=True)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats All'
        verbose_name_plural = 'Stats All'

    def __str__(self):
        return "All Years"

# ---------------------------------------------------------------
#
# StatsYear
#
# ---------------------------------------------------------------

class StatsYear(models.Model):
    id    = models.AutoField(primary_key=True)

    stats_all = models.ForeignKey(StatsAll, blank=True, default=None, related_name='years')
    year      = models.IntegerField(default=2016)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats Year'
        verbose_name_plural = 'Stats Years'
        ordering = ['-year']

    def __str__(self):
        return 'Year: ' + str(self.year)

# ---------------------------------------------------------------
#
# StatsMonth
#
# ---------------------------------------------------------------

class StatsMonth(models.Model):
    id    = models.AutoField(primary_key=True)

    stats_year = models.ForeignKey(StatsYear, blank=False, related_name='months')
    month      = models.IntegerField(default=1)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats Month'
        verbose_name_plural = 'Stats Months'
        ordering = ['-stats_year', '-month']

    def __str__(self):
        return 'Month: %d-%02d' % (self.stats_year.year, self.month)


# ---------------------------------------------------------------
#
# StatsDay
#
# ---------------------------------------------------------------

class StatsDay(models.Model):
    id   = models.AutoField(primary_key=True)

    date  = models.DateField(auto_now=True, editable=False)

    stats_month = models.ForeignKey(StatsMonth, blank=False, related_name='days')
    day         = models.IntegerField(default=1)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats Day'
        verbose_name_plural = 'Stats Day'
        ordering = ['-stats_month', '-day']

    def __str__(self):
        return 'Day: %d-%02d-%02d' % (self.stats_month.stats_year.year, self.stats_month.month, self.day)



class UsageInfo:

    def __init__(self):
        self.num_reports = 0
        self.num_pages = 0;            


# ---------------------------------------------------------------
#
# StatsUser
#
# ---------------------------------------------------------------

class StatsUser(models.Model):


    id   = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, related_name="stats")

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats User'
        verbose_name_plural = 'Stats User'
        ordering = ['user']

    def __str__(self):
        return str(self.user)

    def get_last_30_days(self):

        usage = UsageInfo()

        last_month = datetime.today() - timedelta(days=30)
        wsrs = self.ws_report_group.ws_reports.filter(created__gte=last_month)

        for wsr in wsrs:
            usage.num_reports += 1
            usage.num_pages += wsr.page_count

        return usage





# ---------------------------------------------------------------
#
# StatsRegisteredUsers
#
# ---------------------------------------------------------------

class StatsRegisteredUsers(models.Model):
    id   = models.AutoField(primary_key=True)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    user_stats = models.ManyToManyField(StatsUser, blank=True, default=None, related_name="stats_registered_users")

    class Meta:
        verbose_name        = 'Stats Registered Users'
        verbose_name_plural = 'Stats Registered Users'

    def __str__(self):
        return "Stats Registered Users"

# ---------------------------------------------------------------
#
# StatsRuleset
#
# ---------------------------------------------------------------

class StatsRuleset(models.Model):
    id   = models.AutoField(primary_key=True)

    stats_all = models.ForeignKey(StatsAll, related_name='rulesets')

    ruleset = models.ForeignKey(Ruleset, related_name='stats')

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = 'Stats Ruleset'
        verbose_name_plural = 'Stats Rulesets'
        ordering = ['ruleset']

    def __str__(self):
        return str(self.ruleset)
