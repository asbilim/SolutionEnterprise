from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ImageGallery, Testimonial, Contact, Request
from unfold.admin import ModelAdmin
from django.contrib.admin import actions
from django.contrib.admin.actions import delete_selected as django_delete_selected

class BaseModelAdmin(ModelAdmin):
    def delete_selected(self, request, queryset):
        return django_delete_selected(self, request, queryset)
    delete_selected.short_description = "Delete selected items"

@admin.register(Product)
class ProductAdmin(BaseModelAdmin):
    list_display = ('name', 'price', 'quantity', 'created_at', 'sizable', 'downloadable', 'image_preview')
    list_filter = ('sizable', 'downloadable', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('gallery',)
    list_per_page = 25
    readonly_fields = ('created_at',)
    
    # Unfold specific configurations
    actions = ['delete_selected']
    actions_row = []  # Empty list if you don't want row actions
    list_display_links = ('name',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('name', 'slug'),
                ('price', 'quantity'),
                'description'
            ),
            'classes': ('grid-col-2',)
        }),
        ('Product Options', {
            'fields': (('sizable', 'downloadable'),),
            'classes': ('grid-col-2',)
        }),
        ('Media', {
            'fields': ('image', 'gallery'),
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

@admin.register(ImageGallery)
class ImageGalleryAdmin(BaseModelAdmin):
    list_display = ('name', 'image_preview')
    search_fields = ('name',)
    list_per_page = 25
    
    # Unfold specific configurations
    actions = ['delete_selected']
    actions_row = []
    
    fieldsets = (
        (None, {
            'fields': ('name', 'image'),
            'classes': ('grid-col-2',)
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

@admin.register(Testimonial)
class TestimonialAdmin(BaseModelAdmin):
    list_display = ('author', 'position', 'image_preview', 'message_preview')
    search_fields = ('author', 'message', 'position')
    list_per_page = 25
    
    # Unfold specific configurations
    actions = ['delete_selected']
    actions_row = []
    
    fieldsets = (
        ('Author Information', {
            'fields': (('author', 'position'),),
            'classes': ('grid-col-2',)
        }),
        ('Content', {
            'fields': ('message',),
            'classes': ('full-width',)
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
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    
    image_preview.short_description = 'Image'
    message_preview.short_description = 'Message Preview'

@admin.register(Contact)
class ContactAdmin(BaseModelAdmin):
    list_display = ('subject', 'email', 'message_preview', 'created_at')
    search_fields = ('subject', 'email', 'message')
    readonly_fields = ('subject', 'email', 'message', 'created_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': (('subject', 'email'),),
            'classes': ('grid-col-2',)
        }),
        ('Message', {
            'fields': ('message',),
            'classes': ('full-width',)
        }),
    )
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message Preview'

@admin.register(Request)
class RequestAdmin(BaseModelAdmin):
    list_display = ('email', 'phone_number', 'product', 'created_at')
    list_filter = ('product', 'created_at')
    search_fields = ('email', 'phone_number')
    readonly_fields = ('email', 'phone_number', 'product', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Request Information', {
            'fields': (
                ('email', 'phone_number'),
                'product',
            ),
            'classes': ('grid-col-2',)
        }),
    )