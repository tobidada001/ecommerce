from ecommerce.models import Cart

def processor(request):
    cart = Cart.objects.filter(owner = request.user.id).last()
    
    return {'cart': cart}