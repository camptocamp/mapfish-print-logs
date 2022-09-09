import os
from typing import Optional, Tuple, Union

import c2cwsgiutils.auth
import pyramid.request  # type: ignore
from pyramid.security import Allowed, Denied  # type: ignore

from mapfish_print_logs.configuration import Config, SourceConfig
from mapfish_print_logs.utils import read_shared_config


class User:
    login: Optional[str]
    name: Optional[str]
    url: Optional[str]
    is_auth: bool
    token: Optional[str]
    is_admin: bool
    request: pyramid.request.Request

    def __init__(
        self,
        auth_type: str,
        login: Optional[str],
        name: Optional[str],
        url: Optional[str],
        is_auth: bool,
        token: Optional[str],
        request: pyramid.request.Request,
    ) -> None:
        self.auth_type = auth_type
        self.login = login
        self.name = name
        self.url = url
        self.is_auth = is_auth
        self.token = token
        self.request = request
        self.is_admin = c2cwsgiutils.auth.check_access(self.request)

    def has_access(self, source_config: SourceConfig) -> bool:
        if self.is_admin:
            return True

        auth_config = source_config.get("auth", {})
        if "github_repository" in auth_config:
            return c2cwsgiutils.auth.check_access_config(self.request, auth_config) or self.is_admin

        return False


class SecurityPolicy:
    def identity(self, request: pyramid.request.Request) -> User:
        """Return app-specific user object."""

        if not hasattr(request, "user"):
            if "TEST_USER" in os.environ:
                user = User(
                    auth_type="test_user",
                    login=os.environ["TEST_USER"],
                    name=os.environ["TEST_USER"],
                    url="https://example.com/user",
                    is_auth=True,
                    token=None,
                    request=request,
                )
            else:
                is_auth, c2cuser = c2cwsgiutils.auth.is_auth_user(request)
                user = User(
                    "github_oauth",
                    c2cuser.get("login"),
                    c2cuser.get("name"),
                    c2cuser.get("url"),
                    is_auth,
                    c2cuser.get("token"),
                    request,
                )
            setattr(request, "user", user)
        return request.user  # type: ignore

    def authenticated_userid(self, request: pyramid.request.Request) -> Optional[str]:
        """Return a string ID for the user."""

        identity = self.identity(request)

        if identity is None:
            return None

        return identity.login

    def permits(
        self, request: pyramid.request.Request, context: Config, permission: str
    ) -> Union[Allowed, Denied]:
        """Allow access to everything if signed in."""

        identity = self.identity(request)

        if identity is None:
            return Denied("User is not signed in.")
        if identity.auth_type in ("test_user",):
            return Allowed(f"All access auth type: {identity.auth_type}")
        if identity.is_admin:
            return Allowed("The User is admin.")
        if permission == "all":
            return Denied("Root access is required.")
        if permission not in context.get("sources", {}):
            return Denied(f"No such source '{permission}'.")
        if identity.has_access(context["sources"][permission]):
            return Allowed(f"The User has access to source {permission}.")
        return Denied(f"The User has no access to source {permission}.")


def auth_source(request: pyramid.request.Request, source: Optional[str] = None) -> Tuple[Config, str]:
    source = request.matchdict.get("source") if source is None else source
    if source is None:
        raise pyramid.httpexceptions.HTTPBadRequest("This route has no source segment.")
    config = read_shared_config()
    permission = request.has_permission(source, config)
    if isinstance(permission, Allowed):
        return config, source
    raise pyramid.httpexceptions.HTTPForbidden(permission.msg)
