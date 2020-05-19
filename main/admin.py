from django.contrib import admin

from .models import Category, List, Comment, UserProfile

admin.site.site_header = 'HORG Administration'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'registered', 'daysLeft', 'created', 'updated', 'noofdays', 'WhoIsConducting']
    list_editable = ['daysLeft', 'noofdays', 'registered']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_per_page = 9


admin.site.register(UserProfile)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['subject', 'text', 'created_date']
    randomly_fields = ['subject', 'text']


admin.site.register(List, ListAdmin)
admin.site.register(Comment, CommentAdmin)
