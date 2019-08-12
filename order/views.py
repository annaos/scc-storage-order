from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from .models.order import Order
from .forms import *
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import formset_factory
import logging
logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_order_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if 'shib' in request.session:
            shib_meta = request.session['shib']
            logger.warning('Session: ')
            logger.warning(shib_meta)
        logger.warning('User: ')
        logger.warning(request.user)
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        new_context = Order.objects.order_by('-create_date')
        if not self.request.user.is_staff:
            new_context = new_context.filter(
                persons__email=self.request.user.email
            ).distinct()
        return new_context


class PersonsView(generic.ListView):
    template_name = 'persons.html'
    context_object_name = 'persons_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PersonsView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Person.objects.order_by('-id')


@login_required
def personadmin(request, pk):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    person = get_object_or_404(Person, pk=pk)
    person.is_staff = not person.is_staff
    person.save()
    return HttpResponseRedirect(reverse('order:persons'))


@login_required
def edit(request, pk=None):
    if pk:
        order = get_object_or_404(Order, pk=pk)
        if request.user.is_staff:
            form_class = OrderSimpleForm
        elif order.hasPerson(request.user):
            form_class = OrderEditForm
        else:
            return HttpResponseForbidden()
    else:
        order = Order()
        form_class = OrderSimpleForm

    context = {'pk': pk}
    if request.method == "POST":
        form = form_class(data=request.POST, instance=order, owner=request.user)
        if form.is_valid():
            order = form.save()
            # TODO success flash message
            return HttpResponseRedirect(reverse('order:edit', args=(order.id,)))
        else:
            context['error_message'] = "Form invalid"
    else:
        form = form_class(instance=order, owner=request.user)

    context['nfs_aria_expanded'] = "false"
    if order.protocol_nfs:
        context['nfs_aria_expanded'] = "true"

    context['form'] = form
    return render(request, 'edit.html', context)


def comment(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'detail.html', {'order': order})
