from typing import Any

from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(
        self,
        request: Any,
        view: Any,
        obj: Any,
    ) -> bool:
        return request.user == obj


class IsNotAuthenticated(BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        return not request.user.is_authenticated
