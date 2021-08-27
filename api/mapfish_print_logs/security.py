from typing import Optional, cast

import pyramid.config  # type: ignore
import pyramid.request  # type: ignore
from pyramid.authentication import AuthTktAuthenticationPolicy  # type: ignore
from pyramid.authorization import ACLAuthorizationPolicy  # type: ignore
from pyramid.httpexceptions import HTTPFound  # type: ignore


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):  # type: ignore
    def authenticated_userid(self, request: pyramid.request.Request) -> str:
        key = request.key
        if key is None:
            raise HTTPFound(location="/logs/login?back=" + request.current_route_path())
        return cast(str, key)


def get_key(request: pyramid.request.Request) -> Optional[str]:
    if request.unauthenticated_userid is not None:
        return cast(str, request.unauthenticated_userid)
    return cast(Optional[str], request.headers.get("X-API-Key"))


def includeme(config: pyramid.config.Configurator) -> None:
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
        secret=settings["auth.secret"],
        timeout=7 * 24 * 60 * 60,
        reissue_time=1 * 60 * 60,
        max_age=7 * 24 * 60 * 60,
        http_only=True,
        wild_domain=False,  # Chrome doesn't like True with localhost
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_key, "key", reify=True)
