from shop.models import Category

def links(request):
    c=Category.objects.all()
    return {'links':c}    #we can use this key name