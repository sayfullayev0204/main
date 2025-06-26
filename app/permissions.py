from rest_framework import permissions

class IsVillageAdmin(permissions.BasePermission):
    """
    Foydalanuvchi faqat o'ziga tegishli Village ichidagi Citizn-larni boshqarishi mumkin.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.village is not None

    def has_object_permission(self, request, view, obj):
        return obj.Village == request.user.village