from django.db import models
from djongo.models import ArrayModelField

# Create your models here.
class Person(models.Model):
    fullname = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=120)
    def __str__(self):
        return self.fullname
    
class Like(models.Model):
    user = models.ForeignKey(Person, default=1, on_delete=models.SET_DEFAULT)

class Comment(models.Model):
    user = models.ForeignKey(Person, default=1, on_delete=models.SET_DEFAULT)
    comment = models.CharField(max_length=120)

class Post(models.Model):
    user = models.ForeignKey(Person, default=1, on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=500)
    likes = ArrayModelField(null=False,model_container=Like)
    comments = ArrayModelField(null=False, model_container=Comment)
    def __str__(self):
        return self.user.fullname
