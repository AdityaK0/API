from django.contrib import admin
from .models import  Post, Like 





@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visibility', 'creation_date', 'likes_count')
    list_filter = ('visibility', 'creation_date', 'is_active')
    search_fields = ('title', 'description', 'content')
    raw_id_fields = ('author',)
    
    def likes_count(self, obj):
        return obj.likes_count
    likes_count.short_description = 'Likes'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'post')

