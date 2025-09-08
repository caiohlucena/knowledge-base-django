from django.contrib import admin
from .models import Category, Process, Attachment, UsefulLink, Favorite, Step


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1


class UsefulLinkInline(admin.TabularInline):
    model = UsefulLink
    extra = 1


class StepInline(admin.TabularInline):
    model = Step
    extra = 1
    fields = ("order", "text", "is_required", "completed")
    ordering = ("order",)


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'updated_at', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'description', 'steps_md')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [StepInline, AttachmentInline, UsefulLinkInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Favorite)
