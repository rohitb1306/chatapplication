from django.shortcuts import render,redirect
from django.views.generic import RedirectView,View,CreateView
from django.contrib.auth.models import auth
from .forms import signupform
from django.contrib import messages

# Create your views here.

class Profile(RedirectView):
    url="/"

class Signout(View):
    def get(self,request):
        auth.logout(request)
        return redirect("login")

class Signup(CreateView):
    form_class = signupform
    template_name = "account/register.html"
    success_url='login'

    def form_valid(self, form):
        messages.success(self.request,'User signed up')
        
        return super().form_valid(form)