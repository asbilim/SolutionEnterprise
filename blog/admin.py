from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category
from unfold.admin import ModelAdmin
from django.contrib.admin import actions
from django.contrib.admin.actions import delete_selected as django_delete_selected

class BaseModelAdmin(ModelAdmin):
    def delete_selected(self, request, queryset):
        return django_delete_selected(self, request, queryset)
    delete_selected.short_description = "Delete selected items"

@admin.register(Category)
class CategoryAdmin(BaseModelAdmin):
    list_display = ('title', 'slug', 'description', 'image_preview')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 25
    ordering = ('title',)
    
    # Unfold specific configurations
    actions = ['delete_selected']
    actions_row = []  # Empty list if you don't want row actions
    list_display_links = ('title',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (('title', 'slug'), 'description'),
            'classes': ('grid-col-2',)  # Unfold's grid system
        }),
        ('Media', {
            'fields': ('image',),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">', 
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #f3f4f6; border-radius: 4px; display: flex; align-items: center; justify-content: center;">No Image</div>'
        )
    image_preview.short_description = 'Image'

@admin.register(Article)
class ArticleAdmin(BaseModelAdmin):
    list_display = ('title', 'category', 'created_at', 'likes', 'shares', 'image_preview')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    readonly_fields = ('likes', 'shares', 'created_at')
    list_per_page = 25
    
    # Unfold specific configurations
    actions = ['delete_selected']
    actions_row = []  # Empty list if you don't want row actions
    list_display_links = ('title',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('title', 'slug'),
                'category',
                'description'
            ),
            'classes': ('grid-col-2',)
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('full-width',)
        }),
        ('Media', {
            'fields': ('image',),
        }),
        ('Engagement', {
            'fields': (('likes', 'shares'),),
            'classes': ('grid-col-2',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;">', 
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #f3f4f6; border-radius: 4px; display: flex; align-items: center; justify-content: center;">No Image</div>'
        )
    image_preview.short_description = 'Image'