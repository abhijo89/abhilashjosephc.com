from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class BlogUser(AbstractUser):
    nickname = models.CharField(max_length=100, blank=True)
    mugshot = models.ImageField(upload_to='upload/mugshots', blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_mod_time = models.DateTimeField(auto_now=True)

    # objects = BlogUserManager()

    def get_absolute_url(self):
        return reverse('blog:author_detail', kwargs={'author_name': self.username})

    def __str__(self):
        return self.email

        # def get_full_url(self):
        #     site = Site.objects.get_current().domain
        #     url = "https://{site}{path}".format(site=site, path=self.get_absolute_url())
        #     return url
