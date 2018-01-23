from website.blog.models import Article
from website.comments.models import Comment


def get_max_articleid_commentid():
    return (Article.objects.latest().pk, Comment.objects.latest().pk)
