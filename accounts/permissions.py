from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    # Allow user to update his own profile, preventing other users to do it
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        # Checking, if id of user profile is the same with id of currently logged in user
        return obj.id == request.user.id
