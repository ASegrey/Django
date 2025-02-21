import datetime
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Recipe, UserProfile
from .forms import RecipeForm, EditRecipeForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages


def index(request):
    latest_recipes_list = Recipe.objects.order_by('-pub_date')[:10]
    return render(request, 'recipe/book.html',{'latest_recipes_list': latest_recipes_list})


def detail(request, recipe_id):
    try:
        r = Recipe.objects.get(id = recipe_id)
    except:
        raise Http404("!Рецепт не найден!")
    latest_comments_list = r.comment_set.order_by("-id")[:5]
    context = {
        'recipes': r,
        'latest_comments_list':latest_comments_list
    }
    return render(request,'recipe/detail.html', context)


def leave_comment(request, recipe_id):
    try:
        r = Recipe.objects.get(id = recipe_id)
    except:
        raise Http404("!Рецепт не найден!")
    r.comment_set.create(author_name = request.POST['name'], author_text = request.POST['text'])
    return HttpResponseRedirect(reverse('recipes:detail',args=(r.id,)))


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            recipe.author = profile
            recipe.pub_date = datetime.datetime.now()
            recipe.save()
            messages.success(request, 'Рецепт успешно добавлен!')
            return HttpResponseRedirect(reverse_lazy('recipes:index'))
    else:
        form = RecipeForm()
    return render(request, 'recipe/add_recipe.html', {'form': form})
# def add_recipe(request):
#     if request.method == 'POST':
#         form = RecipeForm(request.POST, request.FILES)
#         if form.is_valid():
#             recipe = form.save(commit=False)
#             recipe.author = request.user.profile
#             recipe.save()
#             return redirect('recipe/book.html')
#     else:
#         form = RecipeForm()
#     return render(request, 'recipe/add_recipe.html', {'form': form})


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    if recipe.author == request.user:
        form = EditRecipeForm(instance=recipe)
        return render(request, 'recipe/edit_recipe.html', {'recipe': recipe, 'form': form})
    else:
        return HttpResponseForbidden()

    
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    if recipe.author == request.user:
        recipe.delete()
        return HttpResponseRedirect(reverse_lazy('recipes:index'))
    else:
        return HttpResponseForbidden()
    
# Регистрация пользователя
class RegisterUser(CreateView):
    form_class = SignUpForm
    template_name = 'recipe/registration.html'
    success_url = reverse_lazy('recipes:index')

    def form_valid(self, form):
        valid = super(RegisterUser, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return valid

# Авторизация пользователя
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse_lazy('recipes:index'))
    else:
        form = AuthenticationForm()
    return render(request, 'recipe/login.html', {'form': form})

# Выход пользователя
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('recipes:index'))