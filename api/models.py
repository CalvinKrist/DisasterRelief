from django.db import models

class GeoLocation(models.Model):
    latitude  = models.FloatField()
    longitude = models.FloatField()

# An alert of a disaster of some kind generated from a social media post
class MediaAlert(models.Model):
    # Required fields
    source_type       = models.CharField(max_length=255)
    url               = models.URLField()
    disaster_type     = models.CharField(max_length=255) # cannot be blank: label 'unknown' if not known

    # Optional fields (not guarunteed to exist)
    date_created      = models.DateTimeField(blank=True)
    location_name     = models.CharField(max_length=255, blank=True)
    geo_location      = models.OneToOneField(GeoLocation, on_delete=models.SET_NULL, blank=True,
                                             related_name='geo_location', null=True)
    disaster_severity = models.CharField(max_length=255, blank=True) # low, medium, high -- we ignore 'none' as best we can
    tags              = models.TextField(blank=True)