from django.db import models

class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    bank_account = models.CharField(max_length=20)

    def __str__(self):
        return self.company_name

class Material(models.Model):
    material_name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.material_name

class Delivery(models.Model):
    delivery_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    delivery_days = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'Delivery {self.pk}'
