from django.contrib import admin
from .models import Post, Category, Contact, Projects, ProjectCategory, ProjectImage

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'created_at', 'title', 'category']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)


admin.site.register(ProjectCategory)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3


@admin.register(Projects)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_published')
    list_filter = ('category', 'is_published')
    inlines = [ProjectImageInline]
