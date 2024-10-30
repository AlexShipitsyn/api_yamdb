from rest_framework import permissions


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):
    pass