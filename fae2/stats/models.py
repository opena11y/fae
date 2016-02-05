from django.db import models

from django.core.urlresolvers import reverse

from websiteResultGroups.models import WebsiteReportGroup


# ---------------------------------------------------------------
#
# StatsYear
#
# ---------------------------------------------------------------

class StatsYear(models.Model):
	id   = models.AutoField(primary_key=True)
	year = models.IntegerField(default=2016)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)


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

 
# ---------------------------------------------------------------
#
# StatsWeek
#
# ---------------------------------------------------------------

class StatsWeek(models.Model):
	id   = models.AutoField(primary_key=True)

	stats_year  = models.ForeignKey(StatsYear,  blank=False)
    date        = models.DateField(auto_now=True, editable=False)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

 
# ---------------------------------------------------------------
#
# StatsDay
#
# ---------------------------------------------------------------

class StatsDay(models.Model):
	id   = models.AutoField(primary_key=True)

    date  = models.DateField(auto_now=True, editable=False)

	stats_week  = models.ForeignKey(StatsWeek,  blank=False)
	stats_month = models.ForeignKey(StatsMonth, blank=False)

    ws_report_group = models.OneToOneField(WebsiteReportGroup)

