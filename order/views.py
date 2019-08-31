from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from .forms import *
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.template.loader import get_template

import logging
logger = logging.getLogger(__name__)


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_order_list'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(IndexView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        new_context = Order.objects.order_by('-modify_date')
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
    context = {'pk': pk}
    if pk:
        order = get_object_or_404(Order, pk=pk)
        if request.user.is_staff:
            form_class = OrderAdminForm
        elif order.has_person(request.user):
            form_class = OrderEditForm
        else:
            return HttpResponseForbidden()
        context['comments'] = Comment.objects.filter(order=order)
        context['comment_form'] = CommentForm(instance=Comment())
    else:
        order = Order()
        form_class = OrderSimpleForm

    if request.method == "POST":
        old_state = order.state
        form = form_class(data=request.POST, instance=order, owner=request.user)
        if form.is_valid():
            order = form.save()
            messages.add_message(request, messages.SUCCESS, 'Your storage request has been successfully saved.')
            if not pk:
                _notify('created', order, request.get_host() + reverse('order:edit', args=(order.id, )))
            elif pk and old_state != order.state:
                _notify('state-changed', order, request.build_absolute_uri())
            return HttpResponseRedirect(reverse('order:edit', args=(order.id,)))
        else:
            context['error_message'] = "Form is invalid. Please check it."
    else:
        form = form_class(instance=order, owner=request.user)

    context['nfs_aria_expanded'] = "false"
    if order.protocol_nfs:
        context['nfs_aria_expanded'] = "true"

    context['order'] = None
    if pk:
        context['order'] = order

    context['form'] = form
    return render(request, 'edit.html', context)


@login_required
def save_comment(request, pk=None):
    if request.method == "POST":
        comment = Comment()
        comment.person = request.user
        comment.order = get_object_or_404(Order, pk=pk)
        form = CommentForm(data=request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            comment.order.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been successfully saved.')
            _notify('comment-added', comment.order, request.build_absolute_uri(), comment)
    return HttpResponseRedirect(reverse('order:edit', args=(pk,)))


def _notify(template, order, url, comment=None):
    if not hasattr(settings, 'EMAIL_SENDER_ADDRESS'):
        logger.warn('There is no EMAIL_SENDER_ADDRESS. Emails can not be send.')
        return
    context = {'order': order, 'url': url, 'comment': comment, 'persons': order.persons.all().distinct()}
    text_content = get_template('mail/' + template + '.txt').render(context)
    html_content = get_template('mail/' + template + '.html').render(context)
    email = EmailMultiAlternatives(
        _('Your storage request by LSDF'),
        text_content,
        settings.EMAIL_SENDER_ADDRESS,
        [x.email for x in order.persons.all().distinct()],
        _get_bcc()
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def _get_bcc():
    bcc = []
    if hasattr(settings, 'EMAIL_ADMIN_ADDRESS'):
        bcc.append(settings.EMAIL_ADMIN_ADDRESS)
    return bcc