# Create your views here.
import logging

from django.conf import settings
from django.core.cache import cache
from django.views.generic import ListView

from blog.models import Article

logger = logging.getLogger(__name__)


class ArticleListView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    page_type = ''
    paginate_by = settings.PAGINATE_BY
    page_kwarg = 'page'

    def get_view_cache_key(self):
        return self.request.get['pages']

    @property
    def page_number(self):
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        return page

    def get_queryset_cache_key(self):
        raise NotImplementedError()

    def get_queryset_data(self):
        raise NotImplementedError()

    def get_queryset_from_cache(self, cache_key):
        # raise NotImplementedError()
        value = cache.get(cache_key)
        if value:
            logger.info('get view cache.key:{key}'.format(key=cache_key))
            return value
        else:
            article_list = self.get_queryset_data()
            cache.set(cache_key, article_list)
            logger.info('set view cache.key:{key}'.format(key=cache_key))
            return article_list

    def get_queryset(self):
        key = self.get_queryset_cache_key()
        value = self.get_queryset_from_cache(key)
        return value


class IndexView(ArticleListView):
    def get_queryset_data(self):
        article_list = Article.objects.filter(type='a', status='p')
        return article_list

    def get_queryset_cache_key(self):
        cache_key = 'index_{page}'.format(page=self.page_number)
        return cache_key
