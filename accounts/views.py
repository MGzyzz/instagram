from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import views, login, get_user_model
from accounts.forms import LoginForm, RegisterForm
from django.views.generic import CreateView, DetailView
from accounts.models import User, Profile
from instagram.models import Publication, Subscription

class AuthSuccessUrlMixin:
    def get_success_url(self):

        next_url = self.request.GET.get('next')

        if not next_url:
            next_url = self.request.POST.get('next')

        if not next_url:
            next_url = reverse('home')

        return next_url


class Logout(views.LogoutView):
    def get_next_page(self):
        return self.request.META.get('HTTP_REFERER')


class LoginView(AuthSuccessUrlMixin, views.LoginView):
    template_name = 'login.html'
    form_class = LoginForm



class RegisterView(AuthSuccessUrlMixin, CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegisterForm

    def form_valid(self, form):

        avatar_file = self.request.FILES.get('avatar')
        user_information = form.cleaned_data['user_information']
        phone_number = form.cleaned_data['phone_number']
        gender = form.cleaned_data['gender']

        user = form.save()

        profile, created = Profile.objects.get_or_create(user=user)
        profile.user_information = user_information
        profile.phone_number = phone_number
        profile.gender = gender
        profile.avatar = avatar_file



        if avatar_file:
            profile.avatar = avatar_file
        profile.save()

        login(self.request, user)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        return redirect('register')


class Detail(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user/detail.html'
    context_object_name =  'user'
    pk_url_kwarg = 'id'
    paginate_related_by = 5
    paginate_related_orphans = 0



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        user_two = self.request.user
        publication = Publication.objects.filter(user=user)
        context['publications'] = publication
        subscribe = Subscription.objects.filter(subscriber=user_two, followed_user=user)
        context['subscribe'] = subscribe.exists()
        return context