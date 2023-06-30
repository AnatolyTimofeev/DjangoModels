from django.contrib import admin
from .models import Author, Post, Category,Comment

class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = [field.name for field in
                    Comment._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения


admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment,CommentAdmin)