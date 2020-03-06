from django.db import models

# Create your models here.

class Professors(models.Model):
    firstname = models.CharField(max_length = 10)
    lastname = models.CharField(max_length = 10)
    prof_id = models.IntegerField()

    def __str__(self):
        return self.firstname
