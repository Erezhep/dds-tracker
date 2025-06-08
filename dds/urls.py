from django.urls import path
from .views import (
    TransactionListView,
    TransactionCreateView,
    TransactionUpdateView,
    TransactionDeleteView,
    get_subcategories,
    reference_data,
)

urlpatterns = [
    path('', TransactionListView.as_view(), name="transaction_list"),
    path('create/', TransactionCreateView.as_view(), name="transaction_create"),
    path('<int:pk>/edit/', TransactionUpdateView.as_view(), name="transaction_edit"),
    path('<int:pk>/delete/', TransactionDeleteView.as_view(), name="transaction_delete"),
    path('get_subcategories/', get_subcategories, name="get_subcategories"),
    path('reference/', reference_data, name='reference_data'),
]