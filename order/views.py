from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Order
from .forms import OrderSimpleForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_order_list'

    def get_queryset(self):
        # TODO filter by user if not admin
        return Order.objects.order_by('-create_date')


class DetailView(generic.DetailView):
    model = Order
    template_name = 'detail.html'


def edit(request, pk=None):
    if pk:
        order = get_object_or_404(Order, pk=pk)
        # TODO check if user has right to edit. if not:
        # return HttpResponseForbidden()
    else:
        order = Order()

    context = {'pk': pk}
    if request.method == "POST":
        form = OrderSimpleForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            # TODO success flash message
            return HttpResponseRedirect(reverse('order:detail', args=(order.id,)))
        else:
            context['error_message'] = "Form invalid"
    else:
        form = OrderSimpleForm(instance=order)
    context['form'] = form
    return render(request, 'edit.html', context)


def comment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'detail.html', {'order': order})
