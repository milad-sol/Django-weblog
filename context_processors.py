from posts.models import Post, Category


def categories_context(request):
    categories = Category.objects.all()
    return {'categories': categories}
