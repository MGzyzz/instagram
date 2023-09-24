from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.http import urlencode
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .forms import SearchForm, CommentForm, PublicationForm
from instagram.models import Publication, Comment, Subscription

# Create your views here.

class Home(ListView):
    template_name = 'home.html'
    context_object_name = 'publications'
    model = Publication
    ordering = ['-created_at']
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context=  super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form

        context['comments'] = Comment.objects.all().order_by('-created_at')

        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})

        user = self.request.user
        for publication in context['publications']:
            is_liked = publication.user_likes.filter(id=user.id).exists()
            publication.is_liked = is_liked


        return context


    def get_queryset(self):
        qs = super().get_queryset()
        if self.search_value:
            query = Q(user__username__icontains=self.search_value) | Q(user__email__icontains=self.search_value) | Q(user__first_name__icontains=self.search_value)

            qs = qs.filter(query)

        return qs

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')


class PublicationUserDetail(DetailView):
    template_name = 'detail.html'
    model = Publication
    context_object_name = 'publication'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.object
        comments = Comment.objects.filter(publication=publication).order_by('-created_at')
        context['comments'] = comments
        is_liked = publication.user_likes.filter(id=self.request.user.id).exists()
        context['is_liked'] = is_liked
        return context


class UploadComments(CreateView):
    template_name = 'detail.html'
    model = Comment
    context_object_name = 'comment'
    form_class = CommentForm
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        form.save()
        return redirect('detail_publication', self.kwargs['id'])


class CreatePublication(CreateView):
    template_name = 'create_publication.html'
    model = Publication
    form_class = PublicationForm

    def form_valid(self, form):
        user = self.request.user
        publication = form.save(commit=False)
        publication.user = user
        publication.save()
        profile = user.profile
        profile.post_count += 1
        profile.save()

        return redirect('detail_publication', publication.id)



class Subscribe(UpdateView):
    model = Subscription
    pk_url_kwarg = 'id'
    success_url = 'home'
    fields = []

    def post(self, request, *args, **kwargs):
        users = kwargs['id']
        subscribe_user = self.request.user

        subscription, created  = Subscription.objects.get_or_create(subscriber=subscribe_user, followed_user_id=users)
        profile_to_follow = get_user_model().objects.get(id=users).profile

        if created:
            profile_to_follow.followers_count += 1
            subscribe_user.profile.following_count += 1
        else:
            subscription.delete()
            profile_to_follow.followers_count -= 1
            subscribe_user.profile.following_count -= 1

        profile_to_follow.save()
        subscribe_user.profile.save()

        return redirect('profile', users)