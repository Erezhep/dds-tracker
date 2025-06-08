from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from .forms import TransactionForm, TransactionTypeForm, StatusForm, CategoryForm, SubcategoryForm
from django.http import JsonResponse
from .models import Transaction, Status, TransactionType, Category, Subcategory

# Create your views here.
class TransactionListView(ListView):
    model = Transaction
    template_name = "html/transaction_list.html"
    context_object_name = "transactions"
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        #Filtering
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        status = self.request.GET.get("status")
        type_id = self.request.GET.get("type")
        category = self.request.GET.get("category")
        subcategory = self.request.GET.get("subcategory")
        
        if date_from:
            queryset = queryset.filter(custom_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(custom_date__lte=date_to)
        if status:
            queryset = queryset.filter(status_id=status)
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        if category:
            queryset = queryset.filter(category_id=category)
        if subcategory:
            queryset = queryset.filter(subcategory_id=subcategory)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['types'] = TransactionType.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()
        return context
    
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "html/transaction_form.html"
    success_url = reverse_lazy('transaction_list')
    
class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'html/transaction_form.html'
    success_url = reverse_lazy('transaction_list')

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = 'html/transaction_confirm_delete.html'
    success_url = reverse_lazy('transaction_list')

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(subcategories), safe=False)

def reference_data(request):
    # Initialize forms
    status_form = StatusForm(request.POST or None, prefix='status')
    type_form = TransactionTypeForm(request.POST or None, prefix='type')
    category_form = CategoryForm(request.POST or None, prefix='category')
    subcategory_form = SubcategoryForm(request.POST or None, prefix='subcategory')

    # Handle form submissions
    if request.method == 'POST':
        if 'status_submit' in request.POST and status_form.is_valid():
            status_form.save()
            return redirect('reference_data')
        elif 'type_submit' in request.POST and type_form.is_valid():
            type_form.save()
            return redirect('reference_data')
        elif 'category_submit' in request.POST and category_form.is_valid():
            category_form.save()
            return redirect('reference_data')
        elif 'subcategory_submit' in request.POST and subcategory_form.is_valid():
            subcategory_form.save()
            return redirect('reference_data')

    # Handle delete requests
    if request.method == 'POST' and 'delete' in request.POST:
        model = request.POST.get('model')
        pk = request.POST.get('pk')
        if model == 'status':
            get_object_or_404(Status, pk=pk).delete()
        elif model == 'type':
            get_object_or_404(TransactionType, pk=pk).delete()
        elif model == 'category':
            get_object_or_404(Category, pk=pk).delete()
        elif model == 'subcategory':
            get_object_or_404(Subcategory, pk=pk).delete()
        return redirect('reference_data')

    # Context for rendering
    context = {
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'statuses': Status.objects.all(),
        'types': TransactionType.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'html/reference_data.html', context)