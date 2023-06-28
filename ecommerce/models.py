from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import datetime
import uuid
from django.contrib.auth.models import AbstractUser
# Create your models here.
class ProductCategory(models.Model):
    
    category_name = models.CharField( max_length=50)
    def __str__(self):
        return self.category_name

class Brand(models.Model):
    name = models.CharField(verbose_name = "Brand", max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.username
    


class ProductSize(models.Model):
    size = models.CharField(max_length=70, blank=True, null=True)
    
    def __str__(self):
        return self.size


class Color(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)
    color_code = models.CharField(max_length=50, blank=True, null=True)

    def color_tag(self):
        if self.color_code is not None:
            return mark_safe('<div style="background-color: {};"> {} </div>'.format(self.color_code, self.name))
        else:
            return ""

    def __str__(self):
        return self.name


class Product(models.Model):
    VARIANTS = (('Color', 'Color'), ('Size', 'Size'), ('Size-Color', 'Size-Color'), ('None', 'None'))
    name = models.CharField(verbose_name = "Product Name", max_length=100)
    price = models.FloatField(verbose_name = "Price")
    description = RichTextUploadingField(verbose_name = "Description")
    image = models.ImageField(verbose_name = "Product image", upload_to='product_image/')
    is_new = models.BooleanField(default = True)
    sales = models.PositiveIntegerField(default = 0)
    variant = models.CharField(max_length=15, choices = VARIANTS, default = 'None')
    
    category = models.ForeignKey("ProductCategory", related_name = 'products', verbose_name="Category", blank=True, null=True, on_delete=models.CASCADE)
    brand = models.ForeignKey("ecommerce.Brand", related_name = 'brand_products', verbose_name=("Brand"), blank=True, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(verbose_name="Date Added", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Last Updated", auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_added',)


class ProductImage(models.Model):
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null = True)
    image = models.ImageField(upload_to='product_image/')
    def __str__(self):
        return 'Image: ' +self.product.name


class ProductVariation(models.Model):

    title = models.CharField(max_length=100)
    product = models.ForeignKey("ecommerce.Product", related_name ='product_variation', on_delete=models.CASCADE)
    color = models.ForeignKey("ecommerce.Color", on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey("ecommerce.ProductSize", on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default = 1)
    price = models.FloatField(default = 0)
    # image = models.ForeignKey("ecommerce.Images", verbose_name=_(""), on_delete=models.CASCADE)
    def __str__(self):
        return str(self.title)

    def get_sizes(self):
        return self.size
        
    @property
    def return_my_sizes(self):
        sizes = self.objects.all().values_list('size', flat = True).distinct()
        print(sizes)
        return sizes

    class Meta:
        verbose_name = 'ProductVariation'
        verbose_name_plural = 'ProductVariations'



class Cart(models.Model):
    
    # owner = models.ForeignKey(User, verbose_name=("Owner"), on_delete=models.CASCADE)

    @property
    def total_in_cart(self):
        items = self.cart_items.all()
        num_of_products = sum([cart_item.quantity for cart_item in items])
        return num_of_products
        
    @property
    def total_amount_to_pay(self):
        items = self.cart_items.all()
        total_payment = sum([cart_item.total_amount for cart_item in items])

        return float(total_payment)

        
    def __str__(self):
        return self.owner.username
    


class CartItems(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    items = models.ForeignKey(Cart, related_name = "cart_items", blank=True, null=True, verbose_name=("Items"), on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)
    variation = models.ForeignKey(ProductVariation, blank=True, null=True,  on_delete=models.CASCADE)

    @property
    def total_amount(self):
        total_price = self.quantity * self.product.price
        
        return float(total_price)

    def __str__(self):
        return self.product.name


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100)
    customer_review = models.TextField()
    product = models.ForeignKey("ecommerce.Product", related_name = 'product', blank=True, null=True, verbose_name="Product", on_delete=models.CASCADE)

    def __str__(self):
        return self.customer_review


class Order(models.Model):

    STATUS = (('Approved', 'Approved'),
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Canceled', 'Canceled'))
    uid = str(uuid.uuid4())[:8]

    # user = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    order_id = models.CharField(max_length = 10, unique = True, default = uid)
    # cart = models.ForeignKey("Cart", on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    zip = models.CharField( max_length=50, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    total_amount = models.FloatField(default = 0.0)
    status = models.CharField(max_length=50, choices = STATUS, default = 'Pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    

    def __str__(self):
        return self.first_name + ' '+ self.last_name
