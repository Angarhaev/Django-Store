from django.contrib import admin
from .models import Author, Article, Tag, Category


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio')
    ordering = 'pk',
    search_fields = ('name', 'bio')
    fieldsets = [
        (None, {'fields': ['name', 'bio']}),
    ]


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    ordering = 'pk',
    search_fields = ('title', 'author')
    fieldsets = [
        (None, {'fields': ['title', 'content', 'author', 'category', 'tags']}),
    ]

    def get_queryset(self, request):
        return Article.objects.defer('content').select_related('author', 'category').prefetch_related('tags')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

    fieldsets = [
        (None, {'fields': ['name']}),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    fieldsets = [
        (None, {'fields': ['name']}),
    ]
