from decimal import Decimal
from django.conf import settings
from django.db import models

from django.db.models.signals import pre_save, post_save, m2m_changed

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=45, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.FloatField(blank=False, null=False)
    categories = models.ManyToManyField(Category, related_name="products")
    
    def __str__(self):
        return self.name
    
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        (1, "CASH"),
        (2, "CREDIT"),
        (3, "DEBT")
    )

    payment_number = models.IntegerField(null=False, unique=True)
    value = models.FloatField(blank=False, null=False)
    freight_rate = models.FloatField(blank=False, null=False)
    discount = models.FloatField(blank=False, null=False)
    total_value = models.FloatField(blank=False, null=False)
    payment_method = models.IntegerField(choices=PAYMENT_METHOD_CHOICES, blank=False, null=False)
    number_installments = models.IntegerField(blank=False, null=True)
    
    def __str__(self):
        return str(self.payment_method)

class Address(models.Model):
    UF_CHOICES = (
        ('AC', 'Acre'), 
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranão'),
        ('MG', 'Minas Gerais'),
        ('MS', 'Mato Grosso do Sul'),
        ('MT', 'Mato Grosso'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PE', 'Pernanbuco'),
        ('PI', 'Piauí'),
        ('PR', 'Paraná'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('RS', 'Rio Grande do Sul'),
        ('SC', 'Santa Catarina'),
        ('SE', 'Sergipe'),
        ('SP', 'São Paulo'),
        ('TO', 'Tocantins')
    )
    
    street = models.CharField(max_length=200, blank=False, null=False)
    complement = models.CharField(max_length=200, blank=True, null=True)
    number = models.IntegerField(blank=False, null=False)
    reference = models.CharField(max_length=255, blank=True, null=False)
    neighborhood = models.CharField(max_length=45, blank=False, null=False)
    city = models.CharField(max_length=45, blank=False, null=False)
    state_acronym = models.CharField(max_length=2, choices=UF_CHOICES, blank=False, null=False)
    zip_code = models.CharField(max_length=8, blank=False, null=False)
    
    def __str__(self):
        return "{}, {}, {}, {} - {}. {}".format(self.street, self.number, self.neighborhood, self.city, self.state_acronym, self.zip_code)

class Customer(models.Model):
    SEX_CHOICES = (
        (1, "F"),
        (2, "M"),
        (3, "N")
    )

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    sex = models.IntegerField(choices=SEX_CHOICES, blank=False, null=False)
    phone_number = models.CharField(max_length=12, blank=False, null=False)
    date_birth = models.DateField("date of birth", null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

class Order(models.Model):
    STATUS_CHOICES = (
        (1, "DONE"),
        (2, "PROCESS"),
        (3, "TRANSIT"),
        (4, "DELIVERED"),
        (5, "LATE"),
        (6, "CANCELED")
    )

    order_number = models.IntegerField(blank=False, null=False, unique=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payment')
    date_time = models.DateTimeField("date of order")
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, blank=False, null=False)
    products = models.ManyToManyField(Product, related_name="orders")
    
    def __str__(self):
        return str(self.order_number)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
    products = models.ManyToManyField(Product,  blank = True)
    subtotal = models.DecimalField(default = 0.00, max_digits=100, decimal_places = 2)
    freight = models.DecimalField(default = 0.00, max_digits=100, decimal_places = 2)
    total = models.DecimalField(default = 0.00, max_digits=100, decimal_places = 2)
    updated = models.DateTimeField(auto_now = True)
    timestamp = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)
    
def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
  if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
    products = instance.products.all() 
    total = 0 
    for product in products: 
      total += product.price 
    if instance.subtotal != total:
      instance.subtotal = total
      instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender = Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.freight = Decimal(instance.subtotal) * Decimal(0.10) # considere o 10% como uma taxa de entrega
    
    instance.total = Decimal(instance.subtotal) + Decimal(instance.freight)

pre_save.connect(pre_save_cart_receiver, sender = Cart)