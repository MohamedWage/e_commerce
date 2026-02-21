from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views import View
from django.shortcuts import get_object_or_404
from account.models import *
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class ProductView(ListView):
    paginate_by = 20
    ordering = ['-created_date']
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class CategoryDetailView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Product.objects.filter(Category=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
    
class AddToCart(LoginRequiredMixin,View):
    def get(self, request, product_id):
        cart = request.session.get('cart',{})
        product_id_str = str(product_id)
        if product_id_str in cart:
            del cart[product_id_str]
            
        else:
            cart[product_id_str]= 1
        
        request.session['cart'] = cart
        return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    
class CartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        product_ids = list(cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        
        grand_total = 0
        cart_items = []

        for product in products:
            quantity = cart.get(str(product.id), 0)
            subtotal = product.selling_price * quantity
            grand_total += subtotal
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
            })

        context = {
            'cart_items': cart_items,
            'grand_total': grand_total,
            'products': products, 
        }
        return render(request, 'cart.html', context)
    
    

class ManageCart(View):
    def get(self,request,product_id,action):
        cart = request.session.get('cart',{})
        product_id_str = str(product_id)
        if action == 'plus':
            cart[product_id_str] = cart.get(product_id_str) + 1
        elif action == 'minus':
            if cart[product_id_str] >1:
                cart[product_id_str] = cart.get(product_id_str) + 1
            else:
                del cart[product_id_str]
        
        request.session['cart'] = cart
        return redirect('cart')
                
