from django.contrib import admin

from . models import Product, Customer,Cart,Payment,OrderPlaced,Wishlist

#Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']

@admin.register(Customer)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state','zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'order_id', 'payment_status', 'payment_id','paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'ordered_date','status']

@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin): 
    list_display = ['id','user','product']