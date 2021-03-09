from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField
from django.db.models.signals import post_save, pre_save
from model_utils import Choices
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField(
    #     max_length=70, unique=True)
    city = models.CharField(max_length=255, default='')

    STATUS = Choices('Singer', 'Baglama-Player', 'Guitar-Player',
                     'Violin-Player', 'Acordion-Player', 'Chor-Chef')
    status = models.CharField(
        choices=STATUS, default=STATUS.Singer, max_length=20)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    image = models.ImageField(default='post_list/profile_images/default.jpg',
                              upload_to='post_list/profile_images')

    def __str_(self):
        return self.user


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.userprofile.save()


# post_save.connect(created_profile, sender=User)
