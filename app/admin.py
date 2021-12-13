from django.contrib import admin
from .models import Customer,Cart,OrderPlaced,Product

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discount_price','description','brand','category','product_img']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity']




@admin.register(OrderPlaced)
class OrderPlacedAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','order_date','status']




