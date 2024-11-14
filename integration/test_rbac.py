import pytest

from integration.conftest import ClientFactory
from weaviate.auth import Auth
from weaviate.rbac.models import (
    RBAC,
    Role,
    CollectionsPermission,
    RolesPermission,
    TenantsPermission,
)


RBAC_PORTS = (8092, 50063)
RBAC_AUTH_CREDS = Auth.api_key("existing-key")


@pytest.mark.parametrize(
    "permissions,expected",
    [
        (
            RBAC.permissions.collections(actions=RBAC.actions.collection.CREATE),
            Role(
                name="CreateAllCollections",
                cluster_actions=None,
                collections_permissions=[
                    CollectionsPermission(collection="*", action=RBAC.actions.collection.CREATE)
                ],
                roles_permissions=None,
                tenants_permissions=None,
            ),
        ),
        (
            RBAC.permissions.roles(actions=RBAC.actions.roles.MANAGE),
            Role(
                name="ManageAllRoles",
                cluster_actions=None,
                collections_permissions=None,
                roles_permissions=[RolesPermission(role="*", action=RBAC.actions.roles.MANAGE)],
                tenants_permissions=None,
            ),
        ),
        (
            RBAC.permissions.tenants(collection="foo", actions=RBAC.actions.tenants.READ),
            Role(
                name="ReadAllTenantsInFoo",
                cluster_actions=None,
                collections_permissions=None,
                roles_permissions=None,
                tenants_permissions=[
                    TenantsPermission(
                        collection="foo", tenant="*", action=RBAC.actions.tenants.READ
                    )
                ],
            ),
        ),
    ],
)
def test_create_role(client_factory: ClientFactory, permissions, expected) -> None:
    with client_factory(ports=RBAC_PORTS, auth_credentials=RBAC_AUTH_CREDS) as client:
        if client._connection._weaviate_version.is_lower_than(1, 28, 0):
            pytest.skip("This test requires Weaviate 1.28.0 or higher")
        try:
            client.roles.create(
                name=expected.name,
                permissions=permissions,
            )
            role = client.roles.by_name(expected.name)
            assert role == expected
        finally:
            client.roles.delete(expected.name)
