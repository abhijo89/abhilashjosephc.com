from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import cache
from django.utils.functional import cached_property


class BaseModel(models.Model):
    slug = models.SlugField(default='no-slug', max_length=160, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_mod_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Article(BaseModel):
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Posted'),
    )
    COMMENT_STATUS = (
        ('o', 'Turn on'),
        ('c', 'Shut down'),
    )
    TYPE = (
        ('a', 'Article'),
        ('p', 'Page'),
    )
    title = models.CharField('Title', max_length=200, unique=True)
    body = models.TextField()
    pub_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField(max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField(max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']
        verbose_name = "Articles"
        verbose_name_plural = verbose_name
        get_latest_by = 'created_time'

    def get_absolute_url(self):
        return reverse('blog:detailbyid', kwargs={
            'article_id': self.id,
            'year': self.created_time.year,
            'month': self.created_time.month,
            'day': self.created_time.day
        })

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        tree = self.category.get_category_tree()
        names = list(map(lambda c: (c.name, c.get_absolute_url()), tree))

        return names

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == 'no-slug' or not self.id:
            # Only set the slug when the object is created.
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    def comment_list(self):
        cache_key = 'article_comments_{id}'.format(id=self.id)
        value = cache.get(cache_key)
        if value:
            logger.info('get article comments:{id}'.format(id=self.id))
            return value
        else:
            comments = self.comment_set.filter(is_enable=True)
            cache.set(cache_key, comments)
            logger.info('set article comments:{id}'.format(id=self.id))
            return comments

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    @cached_property
    def next_article(self):
        return Article.objects.filter(id__gt=self.id, status='p').order_by('id').first()

    @cached_property
    def prev_article(self):
        return Article.objects.filter(id__lt=self.id, status='p').first()


class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    parent_category = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = "Category"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'category_name': self.slug})

    def __str__(self):
        return self.name

    @cache_decorator(60 * 60 * 10)
    def get_category_tree(self):
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys

    @cache_decorator(60 * 60 * 10)
    def get_sub_categorys(self):
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)

        parse(self)
        return categorys


class Tag(BaseModel):
    """Tag Model"""
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_name': self.slug})

    @cache_decorator(60 * 60 * 10)
    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "Tags"
        verbose_name_plural = verbose_name


class Links(models.Model):
    name = models.CharField(max_length=30, unique=True)
    link = models.URLField()
    sequence = models.IntegerField(unique=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_mod_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sequence']
        verbose_name = 'Links'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SideBar(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    sequence = models.IntegerField(unique=True)
    is_enable = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    last_mod_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sequence']
        verbose_name = 'SideBar'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
