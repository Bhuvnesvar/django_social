from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, )
    slug = models.SlugField()
    friends = models.ManyToManyField("Profile", blank=True)

    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)


def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass


post_save.connect(post_save_user_model_receiver, sender=User)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE, )
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE, )
    timestamp = models.DateTimeField(auto_now_add=True)  # set when created

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)
