from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView

from oauth.forms import RequireEmailForm
from website.utils import get_md5
from .manager import get_manager_by_type
from .models import OAuthUser


# Create your views here.


def oauthlogin(request):
    type = request.GET.get('type', None)
    if not type:
        return HttpResponseRedirect('/')
    manager = get_manager_by_type(type)
    if not manager:
        return HttpResponseRedirect('/')
    nexturl = request.GET.get('next_url', None)
    if not nexturl or nexturl == '/login/':
        nexturl = '/'
    authorizeurl = manager.get_authorization_url(nexturl)
    return HttpResponseRedirect(authorizeurl)


def authorize(request):
    type = request.GET.get('type', None)
    if not type:
        return HttpResponseRedirect('/')
    manager = get_manager_by_type(type)
    if not manager:
        return HttpResponseRedirect('/')
    code = request.GET.get('code', None)
    rsp = manager.get_access_token_by_code(code)
    nexturl = request.GET.get('next_url', None)
    if not nexturl:
        nexturl = '/'
    if not rsp:
        return HttpResponseRedirect(manager.get_authorization_url(nexturl))
    user = manager.get_oauth_userinfo()

    if user:
        if not user.nikename:
            import datetime
            user.nikename = "djangoblog" + datetime.datetime.now().strftime('%y%m%d%I%M%S')
        try:
            user = OAuthUser.objects.get(type=type, openid=user.openid)
        except ObjectDoesNotExist:
            pass
        if type == 'facebook':
            user.token = ''
        email = user.email
        if email:
            author = None
            try:
                author = get_user_model().objects.get(id=user.author_id)
            except ObjectDoesNotExist:
                pass
            if not author:
                result = get_user_model().objects.get_or_create(email=user.email)
                author = result[0]
                if result[1]:
                    author.username = user.nikename
                    author.save()

            user.author = author
            user.save()
            login(request, author)
            return HttpResponseRedirect(nexturl)
        if not email:
            user.save()
            url = reverse('oauth:require_email', kwargs={
                'oauthid': user.id
            })

            return HttpResponseRedirect(url)
    else:
        return HttpResponseRedirect(nexturl)


def emailconfirm(request, id, sign):
    if not sign:
        return HttpResponseForbidden()
    if not get_md5(settings.SECRET_KEY + str(id) + settings.SECRET_KEY).upper() == sign.upper():
        return HttpResponseForbidden()
    oauthuser = get_object_or_404(OAuthUser, pk=id)
    if oauthuser.author:
        author = get_user_model().objects.get(pk=oauthuser.author_id)
    else:
        result = get_user_model().objects.get_or_create(email=oauthuser.email)
        author = result[0]
        if result[1]:
            author.username = oauthuser.nikename
            author.save()
    """
    if oauthuser.email and author.email:
        login(request, author)
        return HttpResponseRedirect('/')
    """
    oauthuser.author = author
    oauthuser.save()
    login(request, author)

    site = Site.objects.get_current().domain
    content = '''
     <p>Congratulations, you have successfully bound your email, you can use {type} to log in directly 
     to the site without password. Welcome to our website, the address is</p>

                <a href="{url}" rel="bookmark">{url}</a>

               
                Thank you again!
                <br />
                If the above link does not open, please copy this link to your browser.
                {url}
    '''.format(type=oauthuser.type, url='http://' + site)

    # send_email(emailto=[oauthuser.email, ], title='Congratulations', content=content)
    url = reverse('oauth:bindsuccess', kwargs={
        'oauthid': id
    })
    url = url + '?type=success'
    return HttpResponseRedirect(url)


class RequireEmailView(FormView):
    form_class = RequireEmailForm
    template_name = 'oauth/require_email.html'

    def get(self, request, *args, **kwargs):
        oauthid = self.kwargs['oauthid']
        oauthuser = get_object_or_404(OAuthUser, pk=oauthid)
        if oauthuser.email:
            pass
            # return HttpResponseRedirect('/')

        return super(RequireEmailView, self).get(request, *args, **kwargs)

    def get_initial(self):
        oauthid = self.kwargs['oauthid']
        return {
            'email': '',
            'oauthid': oauthid
        }

    def get_context_data(self, **kwargs):
        oauthid = self.kwargs['oauthid']
        oauthuser = get_object_or_404(OAuthUser, pk=oauthid)
        if oauthuser.picture:
            kwargs['picture'] = oauthuser.picture
        return super(RequireEmailView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        oauthid = form.cleaned_data['oauthid']
        oauthuser = get_object_or_404(OAuthUser, pk=oauthid)
        oauthuser.email = email
        oauthuser.save()
        sign = get_md5(settings.SECRET_KEY + str(oauthuser.id) + settings.SECRET_KEY)
        site = Site.objects.get_current().domain
        if settings.DEBUG:
            site = '127.0.0.1:8000'
        path = reverse('oauth:email_confirm', kwargs={
            'id': oauthid,
            'sign': sign
        })
        url = "http://{site}{path}".format(site=site, path=path)

        content = """
                <p>Please click the link below to bind your email</p>

                <a href="{url}" rel="bookmark">{url}</a>

                再次感谢您！
                <br />
                If the above link does not open, please copy this link to your browser.
                {url}
                """.format(url=url)
        # send_email(emailto=[email, ], title='Congratulations', content=content)
        url = reverse('oauth:bindsuccess', kwargs={
            'oauthid': oauthid
        })
        url = url + '?type=email'
        return HttpResponseRedirect(url)


def bindsuccess(request, oauthid):
    type = request.GET.get('type', None)
    oauthuser = get_object_or_404(OAuthUser, pk=oauthid)
    if type == 'email':
        title = 'success'
        content = "Congratulations, but also one step after the registration success, " \
                  "please log on to your email to view the mail to complete the registration, thank you."
    else:
        title = '绑定成功'
        content = "Congratulations on your registration success, you can later use {type} to log directly to the " \
                  "site without the password, thank you for your registering to the site.".format(type=oauthuser.type)
    return render(request, 'oauth/bindsuccess.html', {
        'title': title,
        'content': content
    })

# Create your views here.
