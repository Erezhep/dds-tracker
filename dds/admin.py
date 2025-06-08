from django.contrib import admin
from .models import Status, TransactionType, Category, Subcategory, Transaction

# Register your models here.
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "type"]
    list_filter = ("type",)
    
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    list_filter = ("category",)
    

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "custom_date", "status", "type", "category", "subcategory", "amount"]
    list_filter = ("status", "type", "category", "subcategory")
    search_fields = ("comment", )
    date_hierarchy = "custom_date"