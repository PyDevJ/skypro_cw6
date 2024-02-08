from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, ListView, DeleteView

from blog.models import Blog
from message.models import Client, Mailings, Message


class VerificationMixin:
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь создателем этого клиента")
        return self.object


class HomeListView(ListView):
    model = Blog
    template_name = 'message/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletters = Mailings.objects.all()
        active_newsletters = Mailings.objects.filter(state='start')
        client = Client.objects.all()
        context['count'] = newsletters.count()
        context['client'] = client.count()
        context['active_newsletters'] = active_newsletters.count()
        all_blogs = Blog.objects.all()
        context['random_blogs'] = sample(list(all_blogs), min(3, all_blogs.count()))

        return context


class ContactView(View):
    template_name = 'message/kontact.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(name, phone, message)
        return render(request, self.template_name)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    template_name = 'message/client_create.html'
    success_url = reverse_lazy('message:client_list')
    fields = ('first_name', 'last_name', 'surname', 'email',)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'message/update_client.html'
    success_url = reverse_lazy('message:client_list')
    fields = ('first_name', 'last_name', 'surname', 'email',)

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь создателем этого клиента")
        return self.object


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'message/client_list.html'

    def get_queryset(self, **kwargs):
        if self.request.user.groups.filter().exists():
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'message/delete_client.html'
    success_url = reverse_lazy('message:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь создателем этого клиента")
        return self.object


class MailingsListView(LoginRequiredMixin, ListView):
    model = Mailings
    template_name = 'message/mailings_list.html'
    success_url = reverse_lazy('message:mailings_list')


class MailingsCreateView(LoginRequiredMixin, CreateView):
    model = Mailings
    template_name = 'message/mailings_create.html'
    fields = ('message', 'client', 'state', 'periodicity', 'date',)
    success_url = reverse_lazy('message:mailings_list')


class MailingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailings
    template_name = 'message/update_mailings.html'
    fields = ('message', 'client', 'state', 'periodicity', 'date',)
    success_url = reverse_lazy('message:mailings_list')


class MailingsDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailings
    template_name = 'message/delete_mailings.html'
    success_url = reverse_lazy('message:mailings_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/message_list.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'message/create_message.html'
    success_url = reverse_lazy('message:message_list')
    fields = ('name', 'body',)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'message/update_message.html'
    fields = ('name', 'body',)
    success_url = reverse_lazy('message:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:message_list')
    template_name = 'message/delete_message.html'
