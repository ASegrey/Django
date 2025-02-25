from django.contrib import admin
from .models import Recipe, Comment, Category

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = (
        'author',
        'recipe_title',
        'recipe_foto',
        'recipe_ingredients',
        'recipe_text',
        'recipe_time',
        'pub_date',
        'category',
    )
    search_fields = (
        'recipe_title',
        'author',
        'pub_date',
    )
    date_hierarchy = 'pub_date'
    save_on_top = True
    
@admin.register(Comment)
class CategoryComment(admin.ModelAdmin):
    model = Comment
    list_display = (
        'author_name',
        'author_text',
    )
    search_fields = (
        'author_name',
    )
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = (
        'title',
    )
    search_fields = (
        'title',
    )
