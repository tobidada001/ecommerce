from django.contrib import admin
from ecommerce.models import Product, ProductCategory, Brand, ProductSize, CustomerReview, Cart
from ecommerce.models import CartItems, Color, ProductVariation, Order
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1




@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code', 'color_tag')
    
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'product', 'color', 'size', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_id', 'first_name', 'last_name', 'email')
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (ProductVariationInline,)
    list_display = ['id', 'name']

admin.site.register(ProductCategory)
admin.site.register(Brand)
admin.site.register(ProductSize)
admin.site.register(CustomerReview)
admin.site.register(Cart)

admin.site.register(CartItems)
