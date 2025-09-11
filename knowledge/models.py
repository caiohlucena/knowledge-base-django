from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name']

    def __str__(self):
        return self.name


class Process(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='processes')
    title = models.CharField('Título', max_length=160)
    slug = models.SlugField(unique=True)
    description = models.TextField('Descrição')
    steps_md = RichTextField('Passo a passo (Rich Text)', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Processo'
        verbose_name_plural = 'Processos'
        indexes = [models.Index(fields=['title', 'description'])]
        ordering = ['-updated_at']

    def __str__(self):
        return self.title


class Step(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField("Ordem", default=1)
    text = models.TextField("Instrução / Texto")
    is_required = models.BooleanField(default=False, help_text="Se marcado, este passo é obrigatório")
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order} - {self.text[:30]}"


class Attachment(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y/%m/')
    label = models.CharField(max_length=120, blank=True)


class UsefulLink(models.Model):
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()
    label = models.CharField(max_length=120)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'process')
        ordering = ['-created_at']
