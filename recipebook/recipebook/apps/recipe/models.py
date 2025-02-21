import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.user.username} Profile"
    
    
class Category(models.Model):
    """Категория рецепта"""
    category = models.CharField(max_length=100, verbose_name='Категория', null=False, blank=False)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.category   


class Recipe(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    recipe_title = models.CharField('Название рецепта', max_length = 200)
    recipe_foto = models.ImageField('Фото рецепта', upload_to='recipebook/apps/recipe/photos/')
    recipe_ingredients = models.TextField('Ингридиенты рецепта')
    recipe_text = models.TextField('Описание рецепта')
    recipe_time = models.TimeField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации')
    category = models.ForeignKey(Category, verbose_name='Категория рецепта', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.recipe_title
    
    def was_published_recent(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    author_name = models.CharField('Имя автора', max_length = 50)
    author_text = models.CharField('Текст комментария', max_length = 200)
    
    def __str__(self) -> str:
        return self.author_name
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        
