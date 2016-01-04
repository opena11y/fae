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

	wsr_group    = models.ForeignKey(WebsiteReportGroup, related_name="stats_years")


# ---------------------------------------------------------------
#
# StatsMonth
#
# ---------------------------------------------------------------

class StatsMonth(models.Model):
	id    = models.AutoField(primary_key=True)

	stats_year = models.ForeignKey(StatsYear, blank=False)
	month      = models.IntegerField(default=1)

	wsr_group    = models.ForeignKey(WebsiteReportGroup, related_name="stats_months")


# ---------------------------------------------------------------
#
# StatsWeek
#
# ---------------------------------------------------------------

class StatsWeek(models.Model):
	id   = models.AutoField(primary_key=True)

	stats_year  = models.ForeignKey(StatsYear,  blank=False)
    date        = models.DateField(auto_now=True, editable=False)

	wsr_group    = models.ForeignKey(WebsiteReportGroup, related_name="stats_weeks")

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

	wsr_group    = models.ForeignKey(WebsiteReportGroup, related_name="stats_days")
