from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.utils import timezone


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    register = models.ManyToManyField(User, related_name='likes', blank=True)
    image = models.ImageField(upload_to='product', blank=True)
    daysLeft = models.BooleanField(default=True)
    noofdays = models.DecimalField(max_digits=3, decimal_places=0)
    WhoIsConducting = models.CharField(max_length=250)
    question = models.FileField(upload_to='questions', blank=True)
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

    def total_registered(self):
        return self.register.count()


class Comment(models.Model):
    post = models.ForeignKey(List, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=150, default='', blank=True)
    institute_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=100)
    Address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    images = models.ImageField(upload_to='profileImage', blank=True, null=True)

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])
        user_profile.save()
    post_save.connect(create_profile(sender=User))
