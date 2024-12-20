from django.db import models

class Store(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class URL(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField()

    def __str__(self):
        return self.url


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    sku = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class History(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    at = models.DateTimeField(auto_now=True)
    default_price = models.DecimalField(max_digits=15, decimal_places=2)
    offer_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    offer = models.BooleanField()
    category = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Histórico para o produto {self.product.sku} em {self.at.strftime('%Y-%m-%d %H:%M:%S')}"

