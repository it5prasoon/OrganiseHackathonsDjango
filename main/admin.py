from django.contrib import admin

from .models import Category, List, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'registered', 'daysLeft', 'created', 'updated', 'noofdays']
    list_editable = ['daysLeft', 'noofdays']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_per_page = 10


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['subject', 'text', 'created_date']
    randomly_fields = ['subject', 'text']


admin.site.register(List, ListAdmin)
admin.site.register(Comment, CommentAdmin)
