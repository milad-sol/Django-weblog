from posts.models import Post, Category
from about.models import About


def categories_context(request):
    categories = Category.objects.all()
    abouts = About.objects.first()
    return {'categories': categories, 'abouts': abouts}
