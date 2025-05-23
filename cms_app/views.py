from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes,renderer_classes
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Like
from .serializers import  PostSerializer, PostCreateUpdateSerializer ,UserSerializer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


User = get_user_model()


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def api_root(request):
    return Response({"message":"CMS Blog API's"})
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def api_root(request):
    """
    API Root - Shows all available endpoints
    """
    base_url = f"{request.scheme}://{request.get_host()}/api"
    
    return Response({
        'message': 'Welcome to Django CMS API',
        'endpoints': {
            'authentication': {
                'register': f"{base_url}/accounts/",
                'login': f"{base_url}/accounts/login/",
                'profile': f"{base_url}/me/",
                'update_profile': f"{base_url}/accounts/update/",
                'delete_account': f"{base_url}/accounts/delete/",
            },
            'blog': {
                'list_create': f"{base_url}/blog/",
                'detail': f"{base_url}/blog/{{id}}/",
                'my_posts': f"{base_url}/my-posts/",
                'my_likes': f"{base_url}/my-likes/",
            },
            'likes': {
                'like_post': f"{base_url}/like/{{blog_id}}/",
                'unlike_post': f"{base_url}/like/{{blog_id}}/",
                'post_likes': f"{base_url}/blog/{{blog_id}}/likes/",
            }
        },
        'documentation': {
            'authentication': 'Use JWT tokens in Authorization header: Bearer <token>',
            'permissions': 'Most endpoints require authentication',
            'formats': 'API supports both JSON and browsable HTML interface',
            'example_usage': {
                'register': {
                    'method': 'POST',
                    'url': f"{base_url}/accounts/",
                    'data': {
                        'email': 'user@example.com',
                        'username': 'username',
                        'name': 'Full Name',
                        'password': 'password123',
                        'password_confirm': 'password123'
                    }
                },
                'login': {
                    'method': 'POST',
                    'url': f"{base_url}/accounts/login/",
                    'data': {
                        'email': 'user@example.com',
                        'password': 'password123'
                    }
                },
                'create_blog': {
                    'method': 'POST',
                    'url': f"{base_url}/blog/",
                    'headers': {
                        'Authorization': 'Bearer <your_access_token>'
                    },
                    'data': {
                        'title': 'My Blog Post',
                        'description': 'Short description',
                        'content': 'Full blog content here',
                        'visibility': 'public'
                    }
                }
            }
        }
    })    




@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def blog_list_create(request):

    if request.method == 'GET':
        queryset = Post.objects.filter(is_active=True).filter(
            Q(visibility='public') | Q(author=request.user)
        ).order_by('-creation_date')
        
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            post = Post.objects.get(id=serializer.instance.id)
            response_serializer = PostSerializer(post, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def blog_detail(request, pk):

    try:
        post = Post.objects.get(pk=pk, is_active=True)
    except Post.DoesNotExist:
        return Response({
            'error': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        if post.visibility == 'private' and post.author != request.user:
            return Response({
                'error': 'Post not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if post.author != request.user:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    if request.method in ['PUT', 'PATCH']:
        serializer = PostCreateUpdateSerializer(post, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            response_serializer = PostSerializer(post, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response({
            'message': 'Post deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, permissions
from rest_framework.response import Response
from cms_app.models import Post, Like

@api_view(['POST', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def toggle_like(request, blog_id):

    try:
        post = Post.objects.get(pk=blog_id, is_active=True)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if post.visibility == 'private' and post.author != request.user:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            return Response({'message': 'Post liked successfully', 'liked': True}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Post already liked', 'liked': True}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            return Response({'message': 'Post unliked successfully', 'liked': False}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'error': 'You have not liked this post', 'liked': False}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_posts(request):

    posts = Post.objects.filter(author=request.user, is_active=True).order_by('-creation_date')
    serializer = PostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_likes(request):

    liked_posts = Post.objects.filter(
        likes__user=request.user,
        is_active=True
    ).filter(
        Q(visibility='public') | Q(author=request.user)
    ).order_by('-likes__created_at')
    
    serializer = PostSerializer(liked_posts, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_post_likes(request, blog_id):

    try:
        post = Post.objects.get(pk=blog_id, is_active=True)
    except Post.DoesNotExist:
        return Response({
            'error': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    if post.visibility == 'private' and post.author != request.user:
        return Response({
            'error': 'Post not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    likes = Like.objects.filter(post=post).select_related('user')
    users_who_liked = [like.user for like in likes]
    
    serializer = UserSerializer(users_who_liked, many=True)
    return Response({
        'post_id': blog_id,
        'likes_count': len(users_who_liked),
        'users_who_liked': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, blog_id):
    post = get_object_or_404(Post, pk=blog_id, is_active=True)
    
    if post.visibility == 'private' and post.author != request.user:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        like = Like.objects.get(post=post, user=request.user)
        like.delete()
        return Response({'message': 'Post unliked successfully'}, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response({'error': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)