from typing import Dict, List, Optional, Union

from weaviate.rbac.models import (
    _Permission,
    PermissionsOutputType,
    PermissionsInputType,
    Role,
    User,
)
from weaviate.rbac.roles import _RolesBase

class _Roles(_RolesBase):
    def list_all(self) -> Dict[str, Role]: ...
    def of_current_user(self) -> Dict[str, Role]: ...
    def by_name(self, role_name: str) -> Optional[Role]: ...
    def by_user(self, user: str) -> Dict[str, Role]: ...
    def assigned_users(self, role_name: str) -> Dict[str, User]: ...
    def delete(self, role_name: str) -> None: ...
    def create(self, *, role_name: str, permissions: PermissionsInputType) -> Role: ...
    def assign_to_user(self, *, role_names: Union[str, List[str]], user: str) -> None: ...
    def exists(self, *, role_name: str) -> bool: ...
    def revoke_from_user(self, *, role_names: Union[str, List[str]], user: str) -> None: ...
    def add_permissions(self, *, permissions: PermissionsInputType, role_name: str) -> None: ...
    def remove_permissions(self, *, permissions: PermissionsInputType, role_name: str) -> None: ...
    def has_permission(
        self, *, permission: Union[_Permission, PermissionsOutputType], role: str
    ) -> bool: ...