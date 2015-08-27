__author__ = 'amin'

from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=32)
    email    = models.CharField(max_length=32)
    password = models.CharField(max_length=128)

    @staticmethod
    def save_form(form):
        User.objects.create(username=form.username, email=form.email, password=make_password(form.password))

    @staticmethod
    def exists_user(username):
        if User.objects.filter(username=username):
            return True
        return False


class Ann_net_data(models.Model):
    userid = models.IntegerField()
    data   = models.TextField()

class Ann_trainer_data(models.Model):
    userid = models.IntegerField()
    data   = models.CharField(max_length=128)

class Ann_trainer_rp_data(models.Model):
    userid  = models.IntegerField()
    data    = models.CharField(max_length=128)
    nrndata = models.TextField()

class Ann_samples(models.Model):
    userid = models.IntegerField()
    input  = models.TextField()
    output = models.TextField()