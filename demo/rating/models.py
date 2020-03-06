from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length = 16,unique = True)
    password = models.CharField(max_length = 16)
    u_id = models.IntegerField(primary_key = True)

    def __str__(self):
        return self.username

class Professor(models.Model):
    firstname = models.CharField(max_length = 10)
    lastname = models.CharField(max_length = 10)
    prof_id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.firstname

class Module(models.Model):
    module_name = models.CharField(max_length=20)
    description = models.TextField()
    module_id = models.IntegerField(primary_key=True)
    prof = models.ManyToManyField(Professor)

    def __str__(self):
        return self.module_name