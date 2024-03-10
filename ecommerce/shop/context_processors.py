# shop/context_processors.py

from shop.models import Category

def menu_links(request):
    categories = Category.objects.all()
    return {'links': categories}
