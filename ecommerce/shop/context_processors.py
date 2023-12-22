
from shop.models import Category

def menu_links(request):
    c=Category.objects.all()
    return {'links':c}