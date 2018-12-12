from c2cwsgiutils import services
from pyramid.security import remember, forget

login_service = services.create("login", "/logs/login")
logout_service = services.create("logout", "/logs/logout")


@login_service.get(renderer='../templates/login.html.mako')
def login(request):
    return dict(back=request.params.get('back', ''))


@login_service.post()
def do_login(request):
    key = request.params.get('key')
    back = request.params.get('back', "")
    request.response.headers.update(remember(request, key))
    request.response.status_code = 302
    request.response.headers['Location'] = back if back else "/logs/"
    return request.response


@logout_service.get()
def do_logout(request):
    request.response.headers.update(forget(request))
    request.response.status_code = 302
    request.response.headers['Location'] = "/logs/"
    return request.response
