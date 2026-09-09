from django.contrib import admin

from .models import Comment, Issue, Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project_type', 'author', 'created_time')
    list_filter = ('project_type',)
    search_fields = ('name', 'author__username')
    list_select_related = ('author',)
    readonly_fields = ('created_time',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'project', 'status', 'priority', 'issue_type',
        'author', 'assigned_to', 'created_time',
    )
    list_filter = ('status', 'priority', 'issue_type')
    search_fields = ('title', 'project__name', 'author__username')
    list_select_related = ('project', 'author', 'assigned_to')
    readonly_fields = ('created_time',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_label', 'author', 'issue', 'project')
    search_fields = (
        'description', 'issue__title', 'issue__project__name', 'author__username',
    )
    list_select_related = ('issue__project', 'author')
    readonly_fields = ('id', 'project', 'created_time')
    fields = ('id', 'description', 'issue', 'project', 'author', 'created_time')

    @admin.display(description='Commentaire')
    def comment_label(self, obj: Comment) -> str:
        return str(obj)

    @admin.display(description='Projet', ordering='issue__project__name')
    def project(self, obj: Comment) -> str:
        if not obj or not obj.issue_id:
            return '-'
        return obj.issue.project.name
