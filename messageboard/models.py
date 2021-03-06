from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Message(models.Model):
    author = models.ForeignKey(User)
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="img/", blank=True, null=True)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return  "Message %s" % self.pk
