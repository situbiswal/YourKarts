from django.db import models
from django.contrib.auth.models import User

# Create your models here.

state_choice=(
    ('odisha','odisha'),
    ('karntak','karntak'),
    ('delhi','delhi'),
    ('west_bengle','west_bengle'),
    ('goa','goa'),
    ('punjab','punjab'),
)


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=100)
    state=models.CharField(choices=state_choice,max_length=50)
    zipcode=models.IntegerField()



    def __str__(self):
        return str(self.id)
Ctc=(
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
)        

class Product(models.Model):
    
    title=models.CharField(max_length=200)
    selling_price=models.FloatField()
    discount_price=models.FloatField()
    brand=models.CharField(max_length=50)
    description=models.TextField()
    category=models.CharField(max_length=2,choices=Ctc)
    product_img=models.ImageField(upload_to='productimg')



    def __str__(self):
        return str(self.id)


class Cart (models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price    


Status=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On_the_way','On_the_way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(choices=Status,default='pending',max_length=50)


    @property
    def total_cost(self):
        return self.quantity*self.product.discount_price    

