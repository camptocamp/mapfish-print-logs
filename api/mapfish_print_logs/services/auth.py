from c2cwsgiutils import services
from pyramid.security import remember, forget
from pyramid.renderers import render_to_response

from . import SOURCES_KEY
from .. import utils

login_service = services.create("login", "/logs/login")
logout_service = services.create("logout", "/logs/logout")


@login_service.get(renderer='../templates/login.html.mako')
def login(request):
    return dict(back=request.params.get('back', ''), message="")


@login_service.post()
def do_login(request):
    key = request.params.get('key')
    back = request.params.get('back', "")

    key_ok = key == SOURCES_KEY

    if not key_ok:
        config = utils.read_shared_config()
        for name, config in config['sources'].items():
            if config['key'] == key:
                key_ok = True
                break

    if key_ok:
        response = request.response
        response.headerlist.extend(remember(request, key))
        response.status_code = 302
        response.headers['Location'] = back if back else "/logs/"
        return response
    else:
        return render_to_response('../templates/login.html.mako', dict(back=back, message="Invalid key"),
                                  request=request)


@logout_service.get()
def do_logout(request):
    response = request.response
    response.headerlist.extend(forget(request))
    response.status_code = 302
    response.headers['Location'] = "/logs/"
    return response
