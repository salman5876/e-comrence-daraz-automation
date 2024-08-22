from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CanceledOrderForm
from .models import CanceledOrder
from django.views.generic import DeleteView
from django.urls import reverse_lazy



def canceled_orders(request):
    if request.method == 'POST':
        form = CanceledOrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order added successfully!')
            return redirect('canceled_orders:canceled_orders')
    else:
        form = CanceledOrderForm()

    status_filter = request.GET.get('status', 'all')
    if status_filter == 'yes':
        canceled_orders_list = CanceledOrder.objects.filter(status=True).order_by('-created_at')
    elif status_filter == 'no':
        canceled_orders_list = CanceledOrder.objects.filter(status=False).order_by('-created_at')
    else:
        canceled_orders_list = CanceledOrder.objects.all().order_by('-created_at')

    return render(request, 'canceled_orders/canceled_orders.html', {'form': form, 'canceled_orders_list': canceled_orders_list})

def edit_order(request, pk):
    order = get_object_or_404(CanceledOrder, pk=pk)
    if request.method == 'POST':
        form = CanceledOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully!')
            return redirect('canceled_orders:canceled_orders')  # Use the app_name namespace here
    else:
        form = CanceledOrderForm(instance=order)
    return render(request, 'canceled_orders/edit_order.html', {'form': form})

class CanceledOrderDeleteView(DeleteView):
    model = CanceledOrder
    template_name = 'canceled_orders/canceled_order_confirm_delete.html'
    success_url = reverse_lazy('canceled_orders:canceled_orders')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)