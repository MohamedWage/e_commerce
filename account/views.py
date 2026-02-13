from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import views , login
from .models import UserRole

# Create your views here.

class SignUpView(UserPassesTestMixin, CreateView): 
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'signup.html'
    
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        user = self.request.user
        
        if user.user_role and user.user_role.name == 'Admin':
            return redirect('admin:index') 
        else:
            return redirect('home')
    
    def form_valid(self, form):
        # 1. حفظ اليوزر في الداتابيز
        user = form.save(commit=False)
        customer_role, created = UserRole.objects.get_or_create(name='User')
        user.user_role = customer_role
        user.is_active = True
        user.save()
        
        self.object = user
        
      
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return redirect('home')
    

class Login(views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    def get_success_url(self):
        user = self.request.user
        
        if user.user_role and user.user_role.name == 'Admin':
            return reverse_lazy('admin:index') 
        else:
            return reverse_lazy('home')
    
    
