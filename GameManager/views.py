from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import model_to_dict
from django.http import HttpResponseRedirect

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, UpdateView, DetailView, ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.list import MultipleObjectMixin

from GameManager.forms import LoginForm, GameManagerRegistrationForm, GameCreationForm, UpdateProfileForm, GameCreateForm
from GameManager.models import Game, Profile

from BlackJack import settings

User = get_user_model()


class GameListView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'game_list/games.html'
    context_object_name = "games"
    paginate_by = settings.GAMES_PER_PAGE_LIMIT

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user'] = self.request.user
        data['form_create'] = GameCreateForm(self.request.user)
        return data

    def get_queryset(self):
        if self.kwargs['whose'] == 'my':
            return self.model.objects.filter(owner=self.request.user.id).order_by('id')
        if self.kwargs['whose'] == 'all':
            return self.model.objects.all().order_by('id')


class GameView(LoginRequiredMixin, TemplateView):
    template_name = 'game_list/game/game.html'

    def get_context_data(self, id, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        data['is_owner'] = False
        data['last_owner'] = False
        game_exec = Game.objects.get(id=id).owner
        cur_user = game_exec.filter(id=user.id)
        if cur_user.exists():
            data['is_owner'] = True
            if game_exec.all().count() == 1:
                data['last_owner'] = True
        data['game'] = Game.objects.get(id=id)
        return data


class GameJoinView(LoginRequiredMixin, UpdateView):
    def get(self, request, id, **kwargs):
        game = Game.objects.get(id=id)
        game.owner.add(request.user)
        return HttpResponseRedirect(reverse('game_list', kwargs={'whose': 'my'}))


class GameManagerLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_action'] = reverse('login')
        return data

    def get_success_url(self):
        return reverse('game_list',  kwargs={'whose': 'my'})


class GameManagerLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return HttpResponseRedirect(reverse('login'))


class GameManagerRegistrationView(CreateView):
    form_class = GameManagerRegistrationForm
    template_name = 'registration.html'

    def get_success_url(self):
        return reverse('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GameCreateView(LoginRequiredMixin, CreateView):
    form_class = GameCreationForm
    template_name = 'game_creation.html'
    model = Game
    #fields = ['name', 'description', 'game_image']

    def get_success_url(self):
        return reverse('game_list', kwargs={'whose': 'my'})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FastGameCreateView(LoginRequiredMixin, CreateView):
    form_class = GameCreationForm
    template_name = 'game_list/game_element.html'
    model = Game
    #fields = ['name', 'description', 'game_image']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['element'] = Game.objects.order_by('-id')[0]
        return data

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GameRemoveView(LoginRequiredMixin, DeleteView):
    def get(self, request, id, **kwargs):
        Game.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('game_list', kwargs={'whose': 'my'}))


class GameLeaveView(LoginRequiredMixin, UpdateView):
    def get(self, request, id, **kwargs):
        game = Game.objects.get(id=id)
        cur_exec = game.owner.get(id=request.user.id)
        game.owner.remove(cur_exec)
        return HttpResponseRedirect(reverse('game_list', kwargs={'whose': 'my'}))


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        user = self.request.user
        data['profile'] = Profile.objects.get(id=user.id)
        return data


class UpdateProfileView(LoginRequiredMixin, View):
    form_class = UpdateProfileForm
    template_name = 'update_profile.html'

    def get(self, request):
        user = request.user
        form = UpdateProfileForm(initial=model_to_dict(
            user, fields=['avatar', 'description', 'username']))
        return render(request, 'update_profile.html', {'user': user, 'form': form})

    def post(self, request):
        form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('P:profile'))

    def get_success_url(self):
        return reverse('P: profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class GameListPageView(ListView):
    model = Game
    template_name = 'game_list/page.html'
    context_object_name = "games"
    paginate_by = settings.GAMES_PER_PAGE_LIMIT

    def get_queryset(self):
        if self.kwargs['whose'] == 'my':
            return Game.objects.filter(owner=self.request.user.id).order_by('id')
        if self.kwargs['whose'] == 'all':
            return Game.objects.all().order_by('id')
