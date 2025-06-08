from django.db import models

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class TransactionType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name="categories")
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"
    
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
class Transaction(models.Model):
    created_at = models.DateField(auto_now_add=True)
    custom_date = models.DateField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(TransactionType, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.custom_date or self.created_at} — {self.amount}₽"
    