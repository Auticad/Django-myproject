"""Admin blog — apps/blog/admin.py"""
from django.contrib import admin
from .models import Post, Category, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display        = ['title', 'author', 'category', 'status', 'views', 'created_at']
    list_filter         = ['status', 'category', 'created_at']
    search_fields       = ['title', 'body', 'author__email']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields       = ['author']
    filter_horizontal   = ['tags']
    readonly_fields     = ['views', 'created_at', 'updated_at']
    date_hierarchy      = 'created_at'
    ordering            = ['-created_at']
    list_per_page       = 25

    fieldsets = [
        ('Contenuto',     {'fields': ['title', 'slug', 'body', 'excerpt', 'cover']}),
        ('Relazioni',     {'fields': ['author', 'category', 'tags']}),
        ('Pubblicazione', {'fields': ['status', 'published_at']}),
        ('Statistiche',   {'fields': ['views', 'created_at', 'updated_at'],
                           'classes': ['collapse']}),
    ]

    actions = ['mark_published', 'mark_draft']

    @admin.action(description='Pubblica i post selezionati')
    def mark_published(self, request, queryset):
        count = queryset.update(status='published')
        self.message_user(request, f'{count} post pubblicati.')

    @admin.action(description='Imposta come bozza')
    def mark_draft(self, request, queryset):
        count = queryset.update(status='draft')
        self.message_user(request, f'{count} post impostati come bozza.')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display        = ['name', 'slug']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display        = ['name', 'slug']
