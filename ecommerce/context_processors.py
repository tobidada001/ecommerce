from ecommerce.models import Cart

def processor(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(owner = request.user.id).last()
    else:
        cart = None
    return {'cart': cart}