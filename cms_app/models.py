from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-creation_date']
    
    def __str__(self):
        return self.title
    
    @property
    def likes_count(self):
        return self.likes.count()

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
