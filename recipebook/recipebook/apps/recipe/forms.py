from django import forms
from .models import Recipe, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_title', 'recipe_foto', 'recipe_ingredients', 'recipe_text','category', 'recipe_time']
        widgets = {
            'recipe_ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ингредиенты', 'rows': 5}),
            'recipe_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 5}),
            'recipe_time': forms.TimeInput(attrs={'class': 'form-control', 'placeholder': 'Время приготовления'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Получаем текущее значение id рецепта
        recipe_id = instance.id
        # Изменяем имя файла, чтобы оно соответствовало id рецепта
        file = self.cleaned_data.get('recipe_foto')
        if file:
            filename = f'recipe_{recipe_id}.jpg'
            instance.recipe_foto.name = filename
        
        if commit:
            instance.save()
        return instance
        
class EditRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['recipe_ingredients', 'recipe_text', 'recipe_time']
        widgets = {
            'recipe_ingredients': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ингредиенты', 'rows': 5}),
            'recipe_text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание', 'rows': 5})
        }
        
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']