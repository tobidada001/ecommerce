from ecommerce.models import Cart
import uuid



def processor(request):
    print(request.session.keys())
    sid = str(uuid.uuid4())
    
    try:
        cart = Cart.objects.get(session_id = request.session['anonymoususer'])
    except:
        request.session['anonymoususer'] = sid
        request.session.save()
        cart, created = Cart.objects.get_or_create(session_id = request.session['anonymoususer'])

    return {'cart': cart}