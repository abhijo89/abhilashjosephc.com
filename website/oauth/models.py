from django.conf import settings
from django.db import models


class OAuthUser(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                               on_delete=models.CASCADE)
    openid = models.CharField(max_length=50)
    nikename = models.CharField(max_length=50, )
    token = models.CharField(max_length=150, null=True, blank=True)
    picture = models.CharField(max_length=350, blank=True, null=True)
    type = models.CharField(blank=False, null=False, max_length=50)
    email = models.CharField(max_length=50, null=True, blank=True)
    matedata = models.CharField(max_length=2000, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_mod_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nikename

    class Meta:
        verbose_name = 'OAuthUser'
        verbose_name_plural = verbose_name
