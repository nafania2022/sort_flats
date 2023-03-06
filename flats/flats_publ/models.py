from django.db import models

class Flats(models.Model):
    link = models.CharField(unique=True, max_length=300)
    reference = models.CharField(max_length=30, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=3000, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    photo_links = models.TextField(blank=True, null=True)
    is_tg_posted = models.BooleanField(blank=True, null=True)
    is_archive = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'flats'