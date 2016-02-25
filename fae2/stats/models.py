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

from django.db import models

from django.core.urlresolvers import reverse

from websiteResultGroups.models import WebsiteReportGroup

from django.contrib.auth.models import User

# ---------------------------------------------------------------
#
# StatsYear
#
# ---------------------------------------------------------------

class StatsYear(models.Model):
    id   = models.AutoField(primary_key=True)
    year = models.IntegerField(default=2016)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = "Stats Year"
        verbose_name_plural = "Stats Years"
        ordering = ['-year']

    def __str__(self):
        return str(self.year)

# ---------------------------------------------------------------
#
# StatsMonth
#
# ---------------------------------------------------------------

class StatsMonth(models.Model):
    id    = models.AutoField(primary_key=True)

    stats_year = models.ForeignKey(StatsYear, blank=False)
    month      = models.IntegerField(default=1)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = "Stats Month"
        verbose_name_plural = "Stats Months"
        ordering = ['-stats_year', '-month']

    def __str__(self):
        return str(self.stats_year) + "-" + str(self.month)


# ---------------------------------------------------------------
#
# StatsDay
#
# ---------------------------------------------------------------

class StatsDay(models.Model):
    id   = models.AutoField(primary_key=True)

    date  = models.DateField(auto_now=True, editable=False)

    stats_month = models.ForeignKey(StatsMonth, blank=False)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = "Stats Day"
        verbose_name_plural = "Stats Day"
        ordering = ['-stats_month', '-date']

    def __str__(self):
        return str(self.date)

# ---------------------------------------------------------------
#
# StatsUser
#
# ---------------------------------------------------------------

class StatsUser(models.Model):
    id   = models.AutoField(primary_key=True)

    user  = models.ForeignKey(User, related_name="stats")

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

    class Meta:
        verbose_name        = "Stats User"
        verbose_name_plural = "Stats User"
        ordering = ['user']

    def __str__(self):
        return str(self.user)

