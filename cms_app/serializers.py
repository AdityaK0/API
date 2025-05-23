from rest_framework import serializers
from .models import  Post, Like
from user_auth.models import Profile
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['fullname', 'city']  


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'is_active','profile')
        read_only_fields = ('id', 'created_at')
        
      
        
    

class UserUpdateSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        super().update(instance, validated_data)

        if profile_data:
            user_profile = Profile.objects.get(user=instance)
            user_profile.fullname = profile_data["fullname"]
            user_profile.phonenumber  = profile_data["city"]
            user_profile.save()
            

        return instance

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ('id', 'user', 'created_at')



class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.ReadOnlyField()
    is_liked = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'content', 'creation_date', 
                 'updated_at', 'author', 'visibility', 'likes', 'likes_count', 'is_liked')
        read_only_fields = ('id', 'creation_date', 'updated_at', 'author')
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Like.objects.filter(post=obj, user=request.user).exists()
        return False
    


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'visibility')