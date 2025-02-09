from django.db import models

class Recipe(models.Model):
    recipe_title = models.CharField('Название рецепта', max_length = 200)
    recipe_text = models.TextField('Описание рецепта')
    recipe_time = models.TimeField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации')

class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete = models.CASCADE)
    author_name = models.CharField('Имя автора', max_length = 50)
    author_text = models.CharField('Текст комментария', max_length = 200)
