import datetime
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Recipe,Category #UserProfile
from django.contrib.auth.models import User
from .forms import RecipeForm, EditRecipeForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def index(request):
#     latest_recipes_list = Recipe.objects.order_by('-pub_date')[:10]
#     return render(request, 'recipe/book.html',{'latest_recipes_list': latest_recipes_list})
def index(request):
    # # Получаем все рецепты, отсортированные по дате публикации
    recipes_list = Recipe.objects.order_by('-pub_date')
    # Создаем объект Paginator с количеством объектов на одной странице
    paginator = Paginator(recipes_list, 10)
    # Получаем номер текущей страницы из GET-запроса
    page_number = request.GET.get('page', 1)
    try:
        # Извлекаем текущую страницу объектов
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является числом, возвращаем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если запрашиваемая страница больше максимального числа страниц, возвращаем последнюю страницу результатов
        page = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    context = {
        'latest_recipes_list': page,
        'paginator': paginator,
        'categories': categories,
        }
    return render(request, 'recipe/book.html', context)


def detail(request, recipe_id):
    # try:
    #     r = Recipe.objects.get(id = recipe_id)
    # except:
    #     raise Http404("!Рецепт не найден!")
    recipe = get_object_or_404(Recipe, id = recipe_id)
    latest_comments_list = recipe.comment_set.order_by("-id")[:5]
    if request.user == recipe.author:
        auth_state = True
    else:
        auth_state = False
    context = {
        'recipes': recipe,
        'latest_comments_list':latest_comments_list,
        'auth_state': auth_state
    }
    return render(request,'recipe/detail.html', context)


def leave_comment(request, recipe_id):
    try:
        r = Recipe.objects.get(id = recipe_id)
    except:
        raise Http404("!Рецепт не найден!")
    r.comment_set.create(author_name = request.user, author_text = request.POST['text'])
    return HttpResponseRedirect(reverse('recipes:detail',args=(r.id,)))


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user            # Связываем автора рецепта с текущим пользователем
            # recipe.pub_date = datetime.datetime.now()
            recipe.save()
            messages.success(request, 'Рецепт успешно добавлен!')
            return HttpResponseRedirect(reverse_lazy('recipes:index'))
    else:
        form = RecipeForm()
    return render(request, 'recipe/add_recipe.html', {'form': form})


def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    if recipe.author == request.user:
        if request.method == 'POST':
            return HttpResponseRedirect(reverse('recipes:detail',args=(recipe.id,)))
        else:
            form = EditRecipeForm(instance=recipe)
            return render(request, 'recipe/edit_recipe.html', {'recipe': recipe, 'form': form})
    else:
        return HttpResponseForbidden()

    
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    if recipe.author == request.user:
        if request.method == 'POST':
            # Удаляем рецепт
            recipe.delete()
            # Django автоматически удалит фотографию, связанную с рецептом
            return HttpResponseRedirect(reverse_lazy('recipes:index'))  # Переадресация на список рецептов
        return render(request, 'recipe/delete_recipe.html', {'recipe': recipe})
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
def check_if_user_exists(username):
    """
    Функция проверяет, существует ли пользователь с указанным именем.
    :param username: имя пользователя для проверки
    :return: True, если пользователь существует, False в противном случае
    """
    return User.objects.filter(username=username).exists()

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            # Получаем имя пользователя из запроса
            username = request.POST.get('username', '')
            if check_if_user_exists(username):
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

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    recipes = Recipe.objects.filter(category=category)
    # Создаем объект Paginator с количеством объектов на одной странице
    paginator = Paginator(recipes, 10)
    # Получаем номер текущей страницы из GET-запроса
    page_number = request.GET.get('page', 1)
    try:
        # Извлекаем текущую страницу объектов
        page = paginator.page(page_number)
    except PageNotAnInteger:
        # Если страница не является числом, возвращаем первую страницу
        page = paginator.page(1)
    except EmptyPage:
        # Если запрашиваемая страница больше максимального числа страниц, возвращаем последнюю страницу результатов
        page = paginator.page(paginator.num_pages)
    categories = Category.objects.all()
    
    context = {
        'category': category, 
        'recipes': recipes,
        'slug':slug,
        'latest_recipes_list': recipes,
        'paginator': paginator,
        'categories': categories,
        }
    return render(request, 'recipe/category_detail.html', context)