from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import ContactForm
from django.contrib import messages
from django.shortcuts import redirect


# Create your views here.
class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def form_valid(self, form):
        if form.is_valid():
            messages.success(self.request, 'Thank you for your message!', 'success')
            form.save()

        return redirect('contact:contact')
