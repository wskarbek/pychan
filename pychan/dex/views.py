from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse

from .forms import CreateWalletForm, SendForm
# Create your views here.

class CreateWalletView(FormView):
    template_name = "dex/index.html"
    form_class = CreateWalletForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, form.get_keys())
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('createWalletView')

class SendView(FormView):
    template_name = "dex/index.html"
    form_class = SendForm

    def form_valid(self, form):
        form.send_crypto(**form.data)
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'form submission success')
        return reverse('sendView')