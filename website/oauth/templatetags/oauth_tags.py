#!/usr/bin/env python
# encoding: utf-8

from django import template
from django.urls import reverse

from oauth.manager import get_oauth_apps

register = template.Library()


@register.inclusion_tag('oauth/oauth_applications.html')
def load_oauth_applications(request):
    applications = get_oauth_apps()
    baseurl = reverse('oauth:oauthlogin')
    path = request.get_full_path()

    apps = list(map(lambda x: (x.ICON_NAME,
                               '{baseurl}?type={type}&next_url={next}'
                               .format(baseurl=baseurl, type=x.ICON_NAME, next=path)), applications))
    return {
        'apps': apps
    }
