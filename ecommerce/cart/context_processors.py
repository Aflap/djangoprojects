

from cart.models import Cart

def productcount(request):
  item_count=0
  if request.user.is_authenticated:
    u=request.user
    try:
        cart=Cart.objects.filter(user=u)
        for i in cart:
            item_count=item_count+i.quantity

    except:
        item_count=0
  return {'count':item_count}