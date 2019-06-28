from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from .models.order import Order
from .forms import OrderSimpleForm, PersonForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_order_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        new_context = Order.objects.order_by('-create_date')
        # TODO filter by user if not admin / check if it works
        if self.request.user.is_authenticated:# and not self.request.user.is_superuser:
            new_context = new_context.filter(
           #TODO     Q(owner=self.request.user) | Q(head=self.request.user) | Q(tech=self.request.user)
            )
        return new_context


class DetailView(generic.DetailView):
    model = Order
    template_name = 'detail.html'


@login_required
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
