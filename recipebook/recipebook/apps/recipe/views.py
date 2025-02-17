from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Recipe
from .forms import RecipeForm, EditRecipeForm, LoginForm
from django.contrib.auth import authenticate, login

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


def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('recipe/book.html')
    else:
        form = RecipeForm()
    return render(request, 'recipe/add_recipe.html', {'form': form})


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
        return redirect('recipe/book.html')
    else:
        return HttpResponseForbidden()
    
# Функция для входа пользователя
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('recipe/book.html')
    return render(request, 'login.html', {'form': LoginForm()})