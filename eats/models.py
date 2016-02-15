from django.db import models

class District(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    link = models.URLField(blank=True)
    photo = models.URLField(blank=True)
    district_map = models.URLField(blank=True)

    def __str__(self):
        return '%s' % (self.name)

class Business(models.Model):
    name = models.CharField(max_length=200, unique=True)
    district = models.ForeignKey('District')
    link = models.URLField()
    description = models.TextField(default=None, blank=True, null=True)
    latitude = models.IntegerField(default=None, blank=True, null=True, verbose_name='Latitude')
    longitude = models.IntegerField(default=None, blank=True, null=True, verbose_name='Longitude')
    has_outdoor_seating = models.BooleanField(verbose_name='Outdoor Seating?')
    is_temp_closed = models.BooleanField(verbose_name='Temporarily closed?')
    display_on_site = models.BooleanField(verbose_name='Display on Site?')
    is_eats = models.BooleanField(verbose_name='Eats')
    is_drinks = models.BooleanField(verbose_name='Drinks')
    is_coffee = models.BooleanField(verbose_name='Coffees')
    not_local = models.BooleanField(verbose_name='Not local?')

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return '%s' % (self.name)
