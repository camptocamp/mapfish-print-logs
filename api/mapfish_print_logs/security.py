from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPFound


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        key = request.key
        if key is not None:
            return key
        else:
            raise HTTPFound(location="/logs/login?back=" + request.current_route_path())


def get_key(request):
    if request.unauthenticated_userid is not None:
        return request.unauthenticated_userid
    return request.headers.get('X-API-Key')


def includeme(config):
    settings = config.get_settings()
    authn_policy = MyAuthenticationPolicy(
        secret=settings['auth.secret'],
        timeout=7*24*60*60,
        reissue_time=1*60*60,
        max_age=7*24*60*60,
        http_only=True,
        wild_domain=False  # Chrome doesn't like True with localhost
    )
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_key, 'key', reify=True)
