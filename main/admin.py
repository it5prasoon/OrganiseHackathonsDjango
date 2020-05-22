from django.contrib import admin

from .models import Category, List, Comment, UserProfile

admin.site.site_header = 'HORG Administration'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated', 'noofdays', 'WhoIsConducting']
    list_editable = ['noofdays']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    list_per_page = 9


admin.site.register(UserProfile)


class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['text', 'created_date']
    randomly_fields = ['text']


admin.site.register(List, ListAdmin)
admin.site.register(Comment, CommentAdmin)
