from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=300, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class META:
        db_table = 'Category'
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('main:hackathonCategory', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)

class List(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    registered = models.DecimalField(max_digits=7, decimal_places=0)
    image = models.ImageField(upload_to='product', blank=True)
    daysLeft = models.NullBooleanField(default=True)
    noofdays = models.DecimalField(max_digits=3, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'List'
        ordering = ('name',)
        verbose_name = 'list'
        verbose_name_plural = 'lists'

    def get_url(self):
        return reverse('main:hackathonList', args=[self.category.slug, self.slug])

    def __str__(self):
        return '{}'.format(self.name)
