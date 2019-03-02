from django.db import models

class GeoLocation(models.Model):
    latitude  = models.FloatField()
    longitude = models.FloatField()

class MediaAlert(models.Model):
    source_type   = models.CharField(max_length=255)
    url           = models.URLField()
    date_created  = models.DateTimeField(blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    geo_location  = GeoLocation()