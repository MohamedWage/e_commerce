from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView , FormView
from e_commerce import settings
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import views ,login
from .models import UserRole
import random
from django.core.mail import send_mail
# Create your views here.


def send_verification_email(user, subject="Verification Code"):
    code = str(random.randint(100000, 999999))
    user.verify_code = code
    user.save()
    
    message = f"Your verification code is: {code}"
    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
    except Exception as e:
        print(f"Error: {e}")
    return code


class SignUpView(UserPassesTestMixin, CreateView): 
    form_class = SignUpForm
    template_name = 'signup.html'
    
    def test_func(self):
        return not self.request.user.is_authenticated

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_role, _ = UserRole.objects.get_or_create(name='User')
        user.save()
        
        send_verification_email(user, "Welcome to e-commerce" )
        self.request.session['user_verification_email'] = user.email
        return redirect('verify_page')
class Login(views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_verified:
            send_verification_email(user, "Welcome to e-commerce" )
            self.request.session['user_verification_email'] = user.email
            return redirect('verify_page')
        return super().form_valid(form)
    
    def get_success_url(self):
        user = self.request.user
        
        if user.user_role and user.user_role.name == 'Admin':
            return reverse_lazy('admin:index') 
        else:
            return reverse_lazy('home')
    
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'my_account.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user


class VerifyEmailView(FormView):
    template_name = 'verify_page.html'
    form_class = VerifyForm

    def get(self, request, *args, **kwargs):
        email = request.session.get('user_verification_email')
        if not email: return redirect('login')
        
        user = get_object_or_404(User, email=email)
        if not user.verify_code:
            send_verification_email(user)
            
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        email = self.request.session.get('user_verification_email')
        user = get_object_or_404(User, email=email)
        
        if user.verify_code == form.cleaned_data.get('code'):
            if self.request.session.get('is_reset_password'):
                return redirect('newpass')
            
            user.is_verified = True
            user.verify_code = None
            user.save()
            self.request.session.pop('user_verification_email', None)
            self.request.session.pop('is_reset_password', None)
            login(self.request, user)
            return redirect('home')
        
        form.add_error('code', 'the code is wrong')
        return self.form_invalid(form)

class ForgetPassView(FormView):
    template_name = 'forgetpass.html'
    form_class = ForgetPassForm

    def form_valid(self, form):
        user = User.objects.filter(email=form.cleaned_data.get('email')).first()
        if user:
            send_verification_email(user, "Reset Your Password")
            self.request.session['user_verification_email'] = user.email
            self.request.session['is_reset_password'] = True 
            return redirect('verify_page')
        
        form.add_error('email', 'This email does not exist.')
        return self.form_invalid(form)

class ResendVerifyCodeView(FormView):
    def get(self, request, *args, **kwargs):
        email = request.session.get('user_verification_email')
        if email:
            user = get_object_or_404(User, email=email)
            send_verification_email(user, "New Verification Code")
        return redirect('verify_page')        
        
class NewPassView(FormView):
    template_name = "newpass.html"
    form_class = NewPassForm
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        email = self.request.session.get('user_verification_email')
        if not email:
            return redirect('forget_pass')
        user = get_object_or_404(User, email=email)
        new_password = form.cleaned_data.get('new_password')
        user.set_password(new_password)
        
        user.save()
        del self.request.session['user_verification_email']
        del self.request.session['is_reset_password']
        login(self.request, user)

        return redirect('home')
    