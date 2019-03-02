from django.db import models

class GeoLocation(models.Model):
    latitude  = models.FloatField()
    longitude = models.FloatField()

class MediaAlert(models.Model):
    source_type       = models.CharField(max_length=255)
    url               = models.URLField()
    date_created      = models.DateTimeField(blank=True)
    location_name     = models.CharField(max_length=255, blank=True)
    geo_location      = models.OneToOneField(GeoLocation, on_delete=models.SET_NULL, blank=True,
                                             related_name='geo_location')
    disaster_type     = models.CharField() # cannot be blank: label 'unknown' if not known
    disaster_severity = models.CharField() # low, medium, high -- we ignore 'none' as best we can