from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            # For posts, check visibility
            if hasattr(obj, 'visibility'):
                if obj.visibility == 'private':
                    return obj.author == request.user
                return True
            return True
        
        # Write permissions only to the owner
        return obj.author == request.user if hasattr(obj, 'author') else obj == request.user
