from django.conf import settings
from django.db import models

from blog.models import Article


class Comment(models.Model):
    body = models.TextField('body', max_length=300)
    created_time = models.DateTimeField('Created Time', auto_now_add=True)
    last_mod_time = models.DateTimeField('Modified', auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Author', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name='Article', on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    is_enable = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        ordering = ['created_time']
        verbose_name = "Comment"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def __str__(self):
        return self.body

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
