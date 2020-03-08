from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=16, primary_key=True)
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.username
    def verify_password(self,password):
        return self.password == password

class userToken(models.Model):
    username = models.OneToOneField(to='User',on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=60)

    def __str__(self):
        return self.username.username +"'s token"

class Professor(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname


class Module(models.Model):
    module_name = models.CharField(max_length=20)
    year = models.IntegerField(default=2000)
    semester = models.IntegerField(default=1,
                                   validators=[
                                       MaxValueValidator(2),
                                       MinValueValidator(1)
                                   ])
    description = models.TextField()
    module_id = models.IntegerField(primary_key=True)
    prof = models.ManyToManyField(Professor)

    def __str__(self):
        return self.module_name

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