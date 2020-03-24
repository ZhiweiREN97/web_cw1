from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

#Student model
class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    email = models.CharField(max_length=30, unique=True)
    def __str__(self):
        return self.username

#Professor model
class Professor(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)
    p_id = models.CharField(max_length=10,primary_key=True)

    def __str__(self):
        return self.firstname
#Module model
class Module(models.Model):
    module_name = models.CharField(max_length=50)
    year = models.IntegerField(default=2000)
    semester = models.IntegerField(default=1,
                                   validators=[
                                       MaxValueValidator(2),
                                       MinValueValidator(1)
                                   ])
    description = models.TextField()
    module_id = models.CharField(max_length=10)
    prof = models.ManyToManyField(Professor)

    def __str__(self):
        return self.module_name

#Rating model
class Score(models.Model):
    score = models.IntegerField(default=1,validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.score) +" of module " + self.module.module_name + ", professor " + self.professor.lastname