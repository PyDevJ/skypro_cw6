from random import sample

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View, UpdateView, ListView, DeleteView

from blog.models import Blog
from message.models import Client, Mailings, Message, Log
from message.forms import MailingsForm, ClientForm, MessageForm


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
    form_class = ClientForm
    template_name = 'message/client_create.html'
    success_url = reverse_lazy('message:client_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'message/update_client.html'
    success_url = reverse_lazy('message:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь создателем этого клиента")
        return self.object

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'message/client_list.html'

    def get_queryset(self, **kwargs):
        if self.request.user.groups.filter().exists():
            return Client.objects.all()
        return Client.objects.filter(user=self.request.user)


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'message/delete_client.html'
    success_url = reverse_lazy('message:client_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.user != self.request.user and not self.request.user.is_staff:
            raise Http404("Вы не являетесь создателем этого клиента")
        return self.object

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MailingsCreateView(LoginRequiredMixin, CreateView):
    """Создание рассылки"""
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy('message:mailings_list')

    def form_valid(self, form):
        """Добавление пользователя к рассылке"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MailingsListView(LoginRequiredMixin, ListView):
    """Просмотр списка рассылок"""
    model = Mailings
    form_class = MailingsForm

    def get_queryset(self):
        """Вывод рассылок пользователя либо всех рассылок для модератора"""
        if self.request.user.has_perm('message.view_mailings'):
            return super().get_queryset()
        return super().get_queryset().filter(user=self.request.user)


class MailingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование рассылки"""
    model = Mailings
    form_class = MailingsForm
    success_url = reverse_lazy('message:mailings_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MailingsDeleteView(LoginRequiredMixin,  UserPassesTestMixin, DeleteView):
    """Удаление рассылки"""
    model = Mailings
    success_url = reverse_lazy('message:mailings_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/message_list.html'

    def get_queryset(self):
        """Вывод сообщений пользователя"""
        return super().get_queryset().filter(user=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/create_message.html'
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        """Добавление пользователя к сообщению"""
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message/update_message.html'
    success_url = reverse_lazy('message:message_list')

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:message_list')
    template_name = 'message/delete_message.html'

    def test_func(self):
        user = self.request.user
        if user == self.get_object().user:
            return True
        return self.handle_no_permission()
