from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Votings(models.Model):
    name = models.TextField(unique=True)
    about = models.TextField()
    author = models.TextField()
    all_votes_quantity = models.IntegerField()
    variants = models.TextField()
    variants_values = models.TextField()
    participants = models.TextField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.TextField()


class Complaints(models.Model):
        author = models.TextField()
        user_id = models.IntegerField(default=None)
        message = models.TextField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
