from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_title', 'recipe_foto', 'recipe_ingredients', 'recipe_text', 'recipe_time']
        widgets = {
            'recipe_ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ингредиенты', 'rows': 5}),
            'recipe_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 5}),
            'recipe_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Время приготовления'})
        }
        
class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_ingredients', 'recipe_text', 'recipe_time']
        widgets = {
            'recipe_ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ингредиенты', 'rows': 5}),
            'recipe_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 5})
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=20)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)