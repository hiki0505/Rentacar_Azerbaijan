from rest_framework import permissions

class PostOwnCar(permissions.BasePermission):
    # Allows User to add or edit only his own car, preventing other users to do it
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Checking, if id of car owner is the same with id of currently logged in user
        return obj.owner.id == request.user.id
