from django.db import models

class District(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    photo = models.URLField(blank=True)
    district_map = models.URLField(blank=True)

    def __str__(self):
        return '%s' % (self.name)

class Business(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Date added.')
    name = models.CharField(max_length=200)
    district = models.ForeignKey('District')
    link = models.URLField(max_length=500)
    description = models.TextField(default=None, blank=True, null=True)
    latitude = models.IntegerField(default=None, blank=True, null=True, verbose_name='Latitude')
    longitude = models.IntegerField(default=None, blank=True, null=True, verbose_name='Longitude')
    has_outdoor_seating = models.BooleanField(verbose_name='Outdoor Seating?')
    is_temp_closed = models.BooleanField(verbose_name='Temporarily closed?')
    is_eats = models.BooleanField(verbose_name='Eats')
    is_drinks = models.BooleanField(verbose_name='Drinks')
    is_coffee = models.BooleanField(verbose_name='Coffees')
    not_local = models.BooleanField(verbose_name='Not local?')
    open_date = models.DateField()
    close_date = models.DateField(null=True, blank=True, verbose_name='First closed date')

    class Meta:
        verbose_name = 'Business'
        verbose_name_plural = 'Businesses'

    def __str__(self):
        return '%s' % (self.name)

class snapshot(models.Model):
    date = models.DateField(auto_now_add=True)
    local_business_count = models.IntegerField()
    not_local_business_count = models.IntegerField()
    businesses = models.ManyToManyField(Business)

    def __str__(self):
        return 'Snapshot on %s' % (self.date)

class reference_link(models.Model):
    url_link = models.URLField(max_length=500)
    description = models.CharField(max_length=500, default=None, blank=True, null=True)

    class Meta:
        verbose_name = 'Reference Link'
        verbose_name_plural = 'Reference Links'

    def __str__(self):
        return '%s' % (self.link)

class tip(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Date added.')
    name = models.CharField(max_length=200)
    district = models.ForeignKey('District')
    link = models.URLField(max_length=500, default=None, blank=True, null=True)
    references = models.ManyToManyField('reference_link')
    description = models.TextField(default=None, blank=True, null=True)
    has_outdoor_seating = models.BooleanField(verbose_name='Outdoor Seating?')
    is_temp_closed = models.BooleanField(verbose_name='Temporarily closed?')
    is_eats = models.BooleanField(verbose_name='Eats')
    is_drinks = models.BooleanField(verbose_name='Drinks')
    is_coffee = models.BooleanField(verbose_name='Coffees')
    not_local = models.BooleanField(verbose_name='Not local?')
    open_date = models.DateField(null=True, blank=True)
    added = models.BooleanField(verbose_name='Added to Eats?')

    def __str__(self):
        return '%s' % (self.name)
